# AGENTS.md

Personal blog (`buhh`, formerly "Daily Notes"). Markdown files in, server-rendered HTML out.
FastAPI + Jinja2 + vanilla JS. No database, no auth, no build step, no tests.

## Session workflow (required)

`PROGRESS.md` instructs every session to **read it at start and update its "Done log"/"Next up" after each change**. Follow that. Treat its Structure/Next-up text as possibly stale — verify against the code.

## Commands

```bash
uv sync                                              # install deps
uv run uvicorn main:app --reload --port 8000         # dev server
uv run python main.py                                # same, via main()
uv run python -c "from starlette.testclient import TestClient; import main; c=TestClient(main.app); print(c.get('/').status_code)"
```

No lint/formatter/typecheck/test config exists. Don't invent one.

## Editing posts (the common task)

- Add/edit `posts/YYYY-MM-DD-slug.md`. Filename minus `.md` == URL slug, so names must be unique.
- Frontmatter: `title`, `date` (YYYY-MM-DD, controls sort), `tags` (list), `excerpt` (optional; falls back to first 160 chars). See `WRITING.md`.
- Posts are parsed on **every request**, so edits show on reload with no server restart.
- Gotcha: `split_code_comments()` in `main.py` strips full-line `#`/`##` comments out of fenced python blocks and re-emits them as `<p class="code-note">` above the block. That is why code samples use `##` comments. Don't "fix" that formatting.
- New tag gets a grey dot until added to `TAG_COLORS` in `main.py`.

## Structure / gotchas

- `main.py` — all routes (`/`, `/post/{slug}`, `/api/posts`) and frontmatter parsing. `BASE_DIR` is resolved from the file, so run from anywhere.
- `templates/` — `base.html`, `index.html` (hero, list, search/tag/sort), `post.html`. `static/style.css` tokens match `design.md` (warm paper + one yellow `#FFD21E`, Source Sans 3 + IBM Plex Mono).
- `design.md` is a visual reference only — never served.
- Python: `pyproject.toml` requires >=3.12; `.python-version` is 3.14. Dependencies are managed by `uv` (`uv.lock`), not pip.
- `GITHUB.md` has the (already-configured) remote/push notes; don't commit secrets.
