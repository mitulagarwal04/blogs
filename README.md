# Daily Notes 📝

A **personal log + lightweight portfolio** in the warm-paper neo-brutalist
vibe of `design.md`: cream paper, ink outlines, hard shadows, one yellow,
Source Sans 3 + IBM Plex Mono.

Four streams: **learning** · **building** · **readings** · **tweets**
(tweet-length notes kept here instead of timelines).

**Stack:** Python FastAPI backend · Jinja templates · vanilla JS · Markdown files, no database.

## Run

```bash
uv sync
uv run uvicorn main:app --reload --port 8000
# open http://127.0.0.1:8000
```

## Write a post

1. Add `posts/YYYY-MM-DD-slug.md`:
```markdown
---
title: "My day"
date: "2026-09-27"
tags: ["habits", "code"]
excerpt: "One-line teaser for the card."
---

# My day
...markdown body...
```
2. Reload `/` — done. Slug = filename. Sorted newest-first.

## Routes

| Route | What |
|---|---|
| `/` | card grid + tiles + search + tag chips + sort (`?q=&tag=&sort=newest\|oldest\|shortest`) |
| `/post/{slug}` | full post + 4 stat tiles + prev/next |
| `/api/posts` | JSON list (powers instant client filter) |
| `/static/*` | `style.css`, `app.js` |

## Design tokens (from design.md)

`--bg #E9E6DD` · `--surface #FBF8F1` · `--ink #232323` · `--yellow #FFD21E` ·
`--blue #3B7CF6` · `--red #EF3E36` · `--purple #A855F7` · `--green #3E8E5E` ·
`--orange #FF9D00` · 2px ink borders · `3/4/6px` hard shadows · `999px` pills ·
`12–22px` cards · `Source Sans 3` text / `IBM Plex Mono` labels.
Dark mode flips vars via `data-theme="dark"` + localStorage.

## Hosting (Cloudflare free tier?)

FastAPI needs a real Python server — Cloudflare Workers/Pages (free) can't
run it directly. Three free-friendly options:

1. **API stays elsewhere + Cloudflare in front (recommended):** host FastAPI
   on Render / Fly.io / Railway / HF Spaces free tier, then add your domain
   to Cloudflare (free DNS + proxy + SSL). You still "host over Cloudflare".
2. **Cloudflare Tunnel (free, no deploy):** `cloudflared tunnel` exposes your
   local/VPS `uvicorn` to the internet behind Cloudflare. Good for personal use.
3. **Cloudflare Pages only (static):** freeze posts to plain HTML first, then
   deploy the frozen output to Pages. Loses the live FastAPI server.

## Images

All art lives in `static/` (nothing hotlinked): `hero.png` (SpongeBob hero),
`gary.png` (roadmap snail), `patty.png` (wordmark, favicon, list bullets).
Swap any file to change the look — same filename, no template edits.

## Structure

```
main.py        # FastAPI: parse frontmatter, routes, search/filter/sort
posts/*.md     # your daily notes
templates/     # base.html, index.html, post.html
static/        # style.css, app.js (theme toggle + live filter)
design.md      # vibe reference (not served)
```
