# Writing posts

Everything is a Markdown file in `posts/`. No admin panel, no database.

## New post

1. Create `posts/YYYY-MM-DD-slug.md`, e.g. `posts/2026-09-28-fastapi-forms.md`.
   The filename (minus `.md`) is the URL: `/post/2026-09-28-fastapi-forms`.
2. Start the file with this header, then write Markdown below it:

```markdown
---
title: "What I actually did today"
date: "2026-09-28"
tags: ["learning"]
excerpt: "One line shown on the homepage card."
---

# What I actually did today

...write here...
```

3. Reload the homepage. Done.

## The header fields

- `title` — post title. Keep it plain, like you'd say it.
- `date` — `YYYY-MM-DD`. Controls the sort order (newest first).
- `tags` — pick from `learning`, `building`, `readings`, `tweets`
  (old ones still work: `habits`, `writing`, `code`, `fastapi`, `design`, `life`).
  A new tag gets a grey dot until you give it a color in `main.py` → `TAG_COLORS`.
- `excerpt` — one line for the homepage card. If you skip it, the first
  160 characters of the post are used.

## Updating a post

Just edit the file and save. Reload the page — no rebuild step.
To unpublish, delete (or move out) the file.

## Notes

- Filenames must be unique — that's what the URL is built from.
- Keep posts short. If it needs sections, it probably wants to be two posts.
- Markdown supports headings, `code`, code blocks, quotes, tables, links.
  Images: drop the file in `static/` and use `![](/static/name.png)` in the post.
- Preview locally: `uv run uvicorn main:app --reload --port 8000`.
