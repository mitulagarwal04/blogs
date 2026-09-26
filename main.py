"""Daily Notes — FastAPI backend.

Posts live as Markdown files in posts/*.md with YAML frontmatter:
  title, date (YYYY-MM-DD), tags (list), excerpt
Slug = filename without .md
"""
from __future__ import annotations

import math
import re
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent
POSTS_DIR = BASE_DIR / "posts"

# Tag -> dot color (mirrors design.md ARCH/CATS maps, repurposed for blog tags)
TAG_COLORS = {
    "habits": "#3E8E5E",
    "writing": "#A855F7",
    "code": "#3B7CF6",
    "fastapi": "#3B7CF6",
    "design": "#FF9D00",
    "life": "#EF3E36",
    "learning": "#A855F7",
    "building": "#3B7CF6",
    "readings": "#FF9D00",
    "tweets": "#EF3E36",
    "notes": "#3E8E5E",
}
DEFAULT_TAG_COLOR = "#8C8C8C"

app = FastAPI(title="Daily Notes")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def parse_post_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            _, fm, body = parts
            meta = yaml.safe_load(fm) or {}
    body = split_code_comments(body.strip())
    html = markdown.markdown(
        body,
        extensions=["fenced_code", "tables", "toc", "codehilite"],
        extension_configs={"codehilite": {"guess_lang": False, "css_class": "codehilite"}},
    )
    # plain text for search + reading time
    plain = re.sub(r"<[^>]+>", " ", html)
    words = len(re.findall(r"\w+", plain))
    slug = path.stem
    post_date = str(meta.get("date", slug[:10] if re.match(r"\d{4}-\d{2}-\d{2}", slug) else date.today().isoformat()))
    tags = meta.get("tags", []) or []
    return {
        "slug": slug,
        "title": meta.get("title", slug.replace("-", " ").title()),
        "date": post_date,
        "tags": tags,
        "excerpt": meta.get("excerpt", plain.strip()[:160] + "…"),
        "html": html,
        "words": words,
        "reading_mins": max(1, math.ceil(words / 200)),
    }


def load_posts() -> list[dict]:
    if not POSTS_DIR.exists():
        return []
    posts = [parse_post_file(p) for p in sorted(POSTS_DIR.glob("*.md"), reverse=True)]
    # sort by date desc
    def key(p: dict):
        try:
            return datetime.fromisoformat(p["date"])
        except ValueError:
            return datetime.min
    posts.sort(key=key, reverse=True)
    return posts


def all_tags(posts: list[dict]) -> list[dict]:
    counts: dict[str, int] = {}
    for p in posts:
        for t in p["tags"]:
            counts[t] = counts.get(t, 0) + 1
    return [
        {"name": name, "count": counts[name], "color": TAG_COLORS.get(name, DEFAULT_TAG_COLOR)}
        for name in sorted(counts)
    ]


def tag_color(tag: str) -> str:
    return TAG_COLORS.get(tag, DEFAULT_TAG_COLOR)


def split_code_comments(body: str) -> str:
    """Pull full-line `#` comments out of python fenced blocks.

    Code stays clean for highlighting; the comments reappear as a
    <ul class="code-notes"> bullet list right below their block.
    Only applies when the block keeps real code after stripping.
    """
    import html as _html

    pattern = re.compile(r"```(python|py)\b[^\S\n]*\n(.*?)```", re.DOTALL | re.IGNORECASE)

    def repl(m: re.Match) -> str:
        lang, code = m.group(1), m.group(2)
        notes: list[str] = []
        kept: list[str] = []
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                notes.append(re.sub(r"^#+\s?", "", stripped))
            else:
                kept.append(line)
        if not notes or not any(l.strip() for l in kept):
            return m.group(0)
        items = "\n".join(f"<li>{_html.escape(n)}</li>" for n in notes if n)
        block = f"```{lang}\n" + "\n".join(kept).rstrip() + "\n```"
        if items:
            block += f'\n\n<ul class="code-notes">\n{items}\n</ul>'
        return block

    return pattern.sub(repl, body)


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    q: str = Query(default="", description="search text"),
    tag: str = Query(default="", description="filter by tag"),
    sort: str = Query(default="newest", description="newest|oldest|shortest"),
):
    posts = load_posts()
    tags = all_tags(posts)
    stats = {
        "posts": len(posts),
        "tags": len(tags),
        "words": sum(p["words"] for p in posts),
        "latest": posts[0]["date"] if posts else "—",
    }

    ql = q.strip().lower()
    if ql:
        posts = [p for p in posts if ql in (p["title"] + " " + p["excerpt"] + " " + " ".join(p["tags"])).lower()]
    if tag:
        posts = [p for p in posts if tag in p["tags"]]
    if sort == "oldest":
        posts = list(reversed(posts))
    elif sort == "shortest":
        posts = sorted(posts, key=lambda p: p["words"])
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "posts": posts,
            "tags": tags,
            "stats": stats,
            "q": q,
            "active_tag": tag,
            "sort": sort,
            "tag_color": tag_color,
        },
    )


@app.get("/post/{slug}", response_class=HTMLResponse)
def read_post(request: Request, slug: str):
    posts = load_posts()
    match = next((p for p in posts if p["slug"] == slug), None)
    if not match:
        raise HTTPException(status_code=404, detail="Post not found")
    idx = posts.index(match)
    prev_post = posts[idx + 1] if idx + 1 < len(posts) else None  # older
    next_post = posts[idx - 1] if idx - 1 >= 0 else None  # newer
    return templates.TemplateResponse(
        request,
        "post.html",
        {
            "post": match,
            "prev_post": prev_post,
            "next_post": next_post,
            "tag_color": tag_color,
        },
    )


@app.get("/api/posts", response_class=JSONResponse)
def api_posts():
    return [
        {
            "slug": p["slug"],
            "title": p["title"],
            "date": p["date"],
            "tags": p["tags"],
            "excerpt": p["excerpt"],
            "reading_mins": p["reading_mins"],
            "url": f"/post/{p['slug']}",
        }
        for p in load_posts()
    ]


def main():
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
