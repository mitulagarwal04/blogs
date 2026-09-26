---
title: "Learning LangChain"
date: "2026-09-26"
tags: ["learning", "code", "langchain"]
excerpt: "LLM setup, LCEL chains, custom runnables, and streaming events — my LangChain progress notes."
---

# Learning LangChain

I am learning LangChain now and this is my progress divided in topics.

## Topic 1 – LLM Setup

### `/src/common.py`

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache

load_dotenv()

## make an llm with proper keys, enpoint url's, temperatures, tokens, models, timeout, retries, an other stuff.
## we initialize this inside a dict so that the values for these can be changed/updated if wanted while imports.
## then we return the ChatOpenAI response with proper arguments.
def llm(**kwargs):
    d = dict(model='deepseek-flash', openai_api_key=os.environ['DEEPSEEK_API_KEY'],
             openai_api_base='https://api.deepseek.com', temperature=0, max_tokens=800, timeout=60, max_retries=3)

    d.update(kwargs)
    return ChatOpenAI(**d)

def backup_llm(**kwargs):
    d = dict(openai_api_base='https://integrate.api.nvidia.com/v1/chat/completions', openai_api_key = os.environ['NVIDIA_API_KEY'],
             model='nvidia/nemotron-3-ultra-550b-a55b', temperature=0, max_tokens=800, timeout=60, max_retries=2)

    d.update(**kwargs)
    return ChatOpenAI(**d)

## LRU - least recently used cache - we keep the embedding model in cache to convert text into embeddings quickly.
@lru_cache(maxsize=1)
def embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
```

## Topic 2 – LECL Runnables

### 1. Basic chains and calling

```python
import os
from src.common import llm, embeddings, backup_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## we make chatprompttemplate -- here is what llm recieves along with the variable text which is different for each llm call.
prompt = ChatPromptTemplate.from_template('Summarize in one line: {text}')

## then we chain all things together -- prompt then llm then parser
## we can only chain the runnables together not any functions.
## we can also make custom runnables by wrapping normal functions into Runnables - which we do in /ch02/runnables.py
chain = prompt | llm() | StrOutputParser()

## we can call the llm in 3 different way
## 1. one-shot = this is via chain.invoke then pass the values of keys in there.
print(chain.invoke({'text': 'Langgraph persists graph state as checkpoints per super-step.'})[:120])

## 2. We can stream the tokens or the chunk of tokens -- whichever as llm outputs.
print('STREAM:', end= ' ')
for c in chain.stream({'text': 'stream these tokens visibly'}):
    print(c, end='', flush=True)

print()

## 3. We can create batches for prompts - have many values for the variables as lists.
## assign a concurrency on how many of them to process at a time.

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

## we can have multiple variables assigned in normal prompt, just make the prompts using the ChatPromptTemplate
## we can infact make multiple chains and invoke them together with different values for the variables in different calls.
## we can even have different temperatures for different llm calls here. -- this is possible via the src/common.py file which allows to update model args.
prompt = ChatPromptTemplate.from_template('Summarize in one: {text}')
chain1 = prompt | llm(temperature=0.3) | StrOutputParser()
chain2 = prompt | llm(temperature=0.5) | StrOutputParser()

## here with RunnableParallel we can invoke multiple chains together.
## with runnable parallel we cannot invoke for different texts, single texts get invoked for multiple chains
## runnable parallel does not make the function runnable, runnableLambda does that
parallel = RunnableParallel(ch1=chain1,ch2=chain2, ntok=RunnableLambda(lambda x: len(x['text'].split())))
print('PAR: ', parallel.invoke({'text': 'hello world test case.'}))

## here we are making a function runnable with runnabellambda that we use with invoke
router = RunnableLambda(lambda x: 'rag' if '?' in x['q'] else 'chat')
print('ROUTER: ', router.invoke({'q': 'What is thread'}))

def strip_clean(txt: dict) -> str:
    return txt['text'].strip().lower()

strip_clean = RunnableLambda(strip_clean)
custom_chain1 = strip_clean | prompt | llm(temperature=0.2) | StrOutputParser()
custom_chain2 = strip_clean | prompt | llm(temperature=0.9) | StrOutputParser()

## runnable passthorugh just passes though the input it gets, the input is the chain that invoked the passthough.
## e.g. here when we make the parallel chain then the passthrough recieves the input which in this case is the value against 'text' key.
## and rest of the chains go through.
parallel_with_custom = RunnableParallel(ch1=RunnablePassthrough(), ch2=custom_chain1, ch3 = custom_chain2)
print('CUSTOM CHAIN: ', parallel_with_custom.invoke({'text': '     What is the meaning of langchain in 10 words?      '}))

## backups
primary = backup_llm() ## one llm endpoint
secondary = llm() ## change the url or key or anything
## if one fails then fallsback on to another one.

robust = (prompt | primary | StrOutputParser()).with_fallbacks([(prompt | secondary | StrOutputParser())])
print('FALLBACK: ', robust.invoke({'text':'fallback demo'}))
```

### 3. Events and configs

```python
from src.common import llm, backup_llm, embeddings

import asyncio
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

cfg: RunnableConfig = {'tags': ['ch02', 'prod'],
                       'metadata': {'version': 'v1', 'tenant':'demo'},
                       'run_name':'one-line'}

prompt = ChatPromptTemplate.from_template('Summarize this in one line: {text}')

chain = prompt | llm() | StrOutputParser()

async def main():
    async for ev in chain.astream_events({'text': 'events demo'}, config=cfg, version='v2'):
        if ev['event'] in ('on_chat_model_stream', 'on_chain_end'):
            print(ev['event'], str(ev.get('data', {}))[:80])

asyncio.run(main())
```
