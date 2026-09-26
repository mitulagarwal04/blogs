---
title: "LangChain"
date: "2026-09-26"
tags: ["learning", "code", "langchain"]
excerpt: "LLM setup, LCEL chains, custom runnables, and streaming events — my LangChain progress notes."
---

Learning LangChain now and this is my progress divided in topics.

## Topic 1 – LLM Setup

### `/src/common.py`

Everything starts with env vars and imports. `load_dotenv()` pulls keys like `DEEPSEEK_API_KEY` out of a `.env` file so they never end up in the code.

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache

load_dotenv()
```

The main LLM is built from a dict of settings — model, key, endpoint url, temperature, tokens, timeout, retries. Because it is a dict, any call can override values through `**kwargs`, and the updated dict goes straight into `ChatOpenAI`.

```python
def llm(**kwargs):
    d = dict(model='deepseek-flash', openai_api_key=os.environ['DEEPSEEK_API_KEY'],
             openai_api_base='https://api.deepseek.com', temperature=0, max_tokens=800, timeout=60, max_retries=3)

    d.update(kwargs)
    return ChatOpenAI(**d)
```

Same idea for a backup, this time on Nvidia's endpoint, so there is somewhere to fall back to.

```python
def backup_llm(**kwargs):
    d = dict(openai_api_base='https://integrate.api.nvidia.com/v1/chat/completions', openai_api_key = os.environ['NVIDIA_API_KEY'],
             model='nvidia/nemotron-3-ultra-550b-a55b', temperature=0, max_tokens=800, timeout=60, max_retries=2)

    d.update(**kwargs)
    return ChatOpenAI(**d)
```

Embeddings stay in memory behind an `lru_cache`, so the model loads once and converts text into embeddings quickly on every later call.

```python
@lru_cache(maxsize=1)
def embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
```

## Topic 2 – LCEL Runnables

### 1. Basic chains and calling

The usual imports, plus the helpers from `src/common.py`:

```python
import os
from src.common import llm, embeddings, backup_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
```

A prompt template is what the LLM receives along with a `{text}` variable that is different on each call:

```python
prompt = ChatPromptTemplate.from_template('Summarize in one line: {text}')
```

Chain the pieces with `|` — prompt, then LLM, then parser. Only runnables can be chained together, not plain functions. (Custom runnables, made by wrapping normal functions, come later in `/ch02/runnables.py`.)

```python
chain = prompt | llm() | StrOutputParser()
```

Three ways to call it. One-shot via `invoke`, passing the variable values in:

```python
print(chain.invoke({'text': 'we have many ways of getting results from a chain - invoke, batch or stream, you can choose anyone and customize accordingly.'})[:120])
```

Or `stream` the output tokens as the LLM produces them:

```python
print('STREAM:', end= ' ')
for c in chain.stream({'text': 'stream these tokens so i can see them'}):
    print(c, end='', flush=True)

print()
```

Or `batch` many inputs at once, with a concurrency limit on how many get processed at a time:

```python
out = chain.batch([{'text':'first input'}, {'text':'second input'}], config={'max_concurrency': 4})
print(out)
print('BATCH: ', len(out))
print('IN-SCHEMA: ', list(chain.input_schema.model_fields.keys()))
```

### 2. Custom Runnables – Parallel Runnables and Fallbacks

```python
import os
from src.common import embeddings, llm, backup_llm
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
```

Prompts can take multiple variables, and separate chains can run at different temperatures — possible because `llm()` accepts per-call overrides via `src/common.py`:

```python
prompt = ChatPromptTemplate.from_template('Summarize in one: {text}')
chain1 = prompt | llm(temperature=0.3) | StrOutputParser()
chain2 = prompt | llm(temperature=0.5) | StrOutputParser()
```

`RunnableParallel` invokes multiple chains together on a single input. Two limits worth knowing: it cannot fan out over different texts (one text, many chains), and it does not make functions runnable — `RunnableLambda` does that:

```python
parallel = RunnableParallel(ch1=chain1,ch2=chain2, ntok=RunnableLambda(lambda x: len(x['text'].split())))
print('PAR: ', parallel.invoke({'text': 'hello world test case.'}))
```

Here a plain function becomes runnable with `RunnableLambda`, and then works with `invoke`:

```python
router = RunnableLambda(lambda x: 'rag' if '?' in x['q'] else 'chat')
print('ROUTER: ', router.invoke({'q': 'What is thread'}))
```

Same trick, wrapped around a real function this time, then chained like anything else:

```python
def strip_clean(txt: dict) -> str:
    return txt['text'].strip().lower()

strip_clean = RunnableLambda(strip_clean)
custom_chain1 = strip_clean | prompt | llm(temperature=0.2) | StrOutputParser()
custom_chain2 = strip_clean | prompt | llm(temperature=0.9) | StrOutputParser()
```

`RunnablePassthrough` just forwards the input it gets — here the `text` value — while the other chains run alongside it:

```python
parallel_with_custom = RunnableParallel(ch1=RunnablePassthrough(), ch2=custom_chain1, ch3 = custom_chain2)
print('CUSTOM CHAIN: ', parallel_with_custom.invoke({'text': '     What is the meaning of langchain in 10 words?      '}))
```

Backups: one LLM per endpoint, and if the primary fails the chain falls back to the secondary:

```python
primary = backup_llm() ## one llm endpoint
secondary = llm() ## change the url or key or anything

robust = (prompt | primary | StrOutputParser()).with_fallbacks([(prompt | secondary | StrOutputParser())])
print('FALLBACK: ', robust.invoke({'text':'fallback demo'}))
```

### 3. Events and configs

A `RunnableConfig` carries tags, metadata, and a run name along with the call:

```python
from src.common import llm, backup_llm, embeddings

import asyncio
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

cfg: RunnableConfig = {'tags': ['ch02', 'prod'],
                       'metadata': {'version': 'v1', 'tenant':'demo'},
                       'run_name':'one-line'}
```

`astream_events` streams the run's lifecycle events — filtered here to token streams and chain-end — so you can watch a run unfold:

```python
prompt = ChatPromptTemplate.from_template('Summarize this in one line: {text}')

chain = prompt | llm() | StrOutputParser()

async def main():
    async for ev in chain.astream_events({'text': 'events demo'}, config=cfg, version='v2'):
        if ev['event'] in ('on_chat_model_stream', 'on_chain_end'):
            print(ev['event'], str(ev.get('data', {}))[:80])

asyncio.run(main())
```
