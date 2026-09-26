---
title: "I shipped the FastAPI backend in one sitting"
date: "2026-09-25"
tags: ["code", "fastapi"]
excerpt: "Markdown files in, HTML out. No database, no admin panel, just FastAPI + Jinja."
---

# I shipped the FastAPI backend in one sitting

Goal was simple: write `.md` files, get a blog. No CMS, no database to babysit.

How it works now:

1. Drop a file in `posts/` with frontmatter (`title`, `date`, `tags`, `excerpt`)
2. FastAPI parses it with `markdown` + `yaml`
3. Jinja renders it inside the sticker-style shell

```python
@app.get("/post/{slug}")
def read_post(slug: str):
    post = get_post(slug)
    return templates.TemplateResponse("post.html", {"post": post})
```

Things I skipped on purpose:

- Auth / admin editor — VS Code *is* the editor
- Comments — email me instead
- Analytics — server logs are enough for now

Next up: search that actually feels instant. Client-side filter over `/api/posts` should do it.
