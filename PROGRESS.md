# Project progress — Daily Notes blog

> **OpenCode: read this file at the start of every session on this project,
> and update it (Done log + Next up) after each change you make.**

## What this is

Personal log + lightweight portfolio blog. Markdown files in, sticker-styled
HTML out. Warm-paper neo-brutalist look (tokens from `design.md`):
cream `#E9E6DD`, ink `#232323`, one yellow `#FFD21E`, Source Sans 3 +
IBM Plex Mono (no display font). SpongeBob art in `static/` (hero, Gary,
Krabby Patty bullets).

## Stack & commands

- FastAPI + Jinja2 + vanilla JS. No database, no auth.
- `uv sync` to install. Run: `uv run uvicorn main:app --reload --port 8000`.
- Test without a server: `uv run --with httpx python -c
  "from starlette.testclient import TestClient; import main; ..."`.
- Posts: see `WRITING.md`. GitHub push: see `GITHUB.md`.

## Structure

- `main.py` — routes `/`, `/post/{slug}`, `/api/posts`; frontmatter parsing,
  search (`?q=`), tag filter (`?tag=`), sort (`?sort=`).
- `posts/*.md` — 5 sample posts (frontmatter: title, date, tags, excerpt).
- `templates/` — `base.html` (topbar + dark toggle top-right), `index.html`
  (hero, tiles, search, cards, roadmap panel), `post.html`.
- `static/` — `style.css`, `app.js` (theme persist + live card filter),
  `hero.png`, `gary.png`, `patty.png` (favicon + wordmark + bullets).
- `design.md` — vibe reference only, never served.

## Done log

- 2026-09-26: scaffolded FastAPI + Markdown backend, 4 sample posts.
- 2026-09-26: sticker-style frontend (tiles, cards, tags, search, dark mode).
- 2026-09-26: repositioned to personal log (learning/building/readings/tweets).
- 2026-09-26: removed Chewy font + starburst + About page; toggle top-right;
  local SpongeBob images; roadmap panel ("What's not in the open").
- 2026-09-26: deleted `about.html`, cleaned `main.py`; added `WRITING.md`,
  `GITHUB.md`; extended `.gitignore`.
- 2026-09-26 (v0.2.1): brutal UI/UX audit via Playwright (screenshots:
  desktop/mobile/dark/post). Fixed: hero copy ("T - buhh's" → "buhh's notes"),
  "1 posts" grammar, stale "Daily Notes" brand strings, search focus indicator,
  skip link + branded :focus-visible, mobile reader scroll trap (uncapped
  #reader-body under 900px), no-JS search (input now submits ?q=), post footer
  count, #langchain tag color, dead --muted token, prefers-reduced-motion,
  theme-color metas.

## Next up (also listed on the homepage roadmap panel)

1. RSS feed.
2. `/now` page (updated by hand).
3. Reply-by-email links per post.
4. Reading-list page from `#readings` tag.
5. ~~Search that works without JS.~~ Done in v0.2.1 (search submits `?q=`).
