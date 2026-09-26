"""Freeze the FastAPI blog to static HTML for GitHub Pages / any static host.

Usage:
  uv run python freeze.py [--out dist] [--base-path /blogs]

  --out:       output directory (default: dist/, gitignored)
  --base-path: URL prefix the site is served under.
               ""       -> served at domain root (custom domain, RPi, Render)
               "/blogs" -> served at https://<user>.github.io/blogs/

Rewrites absolute /static/, /post/ and /api/posts links in the frozen HTML
(and inside style.css) so project pages under a subpath keep working.
No new dependencies: reuses main.py's loaders plus Starlette templates.

What works on the frozen site: full posts, reader + right-list layout,
live search/tag filtering (client-side JS), theme toggle, prev/next links.
What degrades: sort dropdown and search/tag forms do a plain reload
(no server to re-sort); /api/posts becomes a static api/posts.json file.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from starlette.requests import Request

from main import BASE_DIR, all_tags, load_posts, tag_color, templates

OUT_DEFAULT = BASE_DIR / "dist"


def fake_request(path: str = "/") -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "server": ("freeze", 80),
            "path": path,
            "query_string": b"",
            "headers": [],
        }
    )


def stats_for(posts: list[dict]) -> dict:
    return {
        "posts": len(posts),
        "tags": len(all_tags(posts)),
        "words": sum(p["words"] for p in posts),
        "latest": posts[0]["date"] if posts else "—",
    }


def rewrite(html: str, base_path: str) -> str:
    """Prefix absolute site links so the frozen site works under a subpath."""
    if not base_path:
        return html
    bp = base_path.rstrip("/")
    # specific prefixes first, bare "/" last
    html = html.replace('href="/static/', f'href="{bp}/static/')
    html = html.replace('src="/static/', f'src="{bp}/static/')
    html = html.replace("url(/static/", f"url({bp}/static/")
    html = html.replace('href="/post/', f'href="{bp}/post/')
    html = html.replace('href="/api/posts"', f'href="{bp}/api/posts.json"')
    html = html.replace('action="/"', f'action="{bp}/"')
    html = html.replace('href="/"', f'href="{bp}/"')
    return html


def render(name: str, path: str, context: dict) -> str:
    resp = templates.TemplateResponse(fake_request(path), name, context)
    return resp.body.decode("utf-8")


def freeze(out: Path, base_path: str) -> list[str]:
    if out.exists():
        shutil.rmtree(out)
    (out / "post").mkdir(parents=True)
    (out / "api").mkdir(parents=True)

    posts = load_posts()
    tags = all_tags(posts)
    stats = stats_for(posts)

    # index (unfiltered, newest-first — same as GET / with defaults)
    index_html = render(
        "index.html",
        "/",
        {
            "posts": posts,
            "tags": tags,
            "stats": stats,
            "q": "",
            "active_tag": "",
            "sort": "newest",
            "tag_color": tag_color,
        },
    )
    (out / "index.html").write_text(rewrite(index_html, base_path), encoding="utf-8")

    # one pretty-URL page per post: /post/<slug>/
    for i, post in enumerate(posts):
        prev_post = posts[i + 1] if i + 1 < len(posts) else None  # older
        next_post = posts[i - 1] if i - 1 >= 0 else None  # newer
        page = render(
            "post.html",
            f"/post/{post['slug']}",
            {
                "post": post,
                "prev_post": prev_post,
                "next_post": next_post,
                "tag_color": tag_color,
            },
        )
        page_dir = out / "post" / post["slug"]
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(rewrite(page, base_path), encoding="utf-8")

    # JSON snapshot of /api/posts for the footer link
    api = [
        {
            "slug": p["slug"],
            "title": p["title"],
            "date": p["date"],
            "tags": p["tags"],
            "excerpt": p["excerpt"],
            "reading_mins": p["reading_mins"],
            "url": f"{base_path}/post/{p['slug']}",
        }
        for p in posts
    ]
    (out / "api" / "posts.json").write_text(json.dumps(api, indent=2), encoding="utf-8")

    # static assets (style.css gets the same base-path rewrite for url(...))
    shutil.copytree(BASE_DIR / "static", out / "static")
    css = out / "static" / "style.css"
    css.write_text(rewrite(css.read_text(encoding="utf-8"), base_path), encoding="utf-8")

    # tell Pages: no Jekyll processing (serves _-prefixed files as-is)
    (out / ".nojekyll").write_text("", encoding="utf-8")

    return sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())


def main() -> None:
    ap = argparse.ArgumentParser(description="Freeze blog to static HTML.")
    ap.add_argument("--out", default=str(OUT_DEFAULT), help="output directory")
    ap.add_argument(
        "--base-path",
        default="/blogs",
        help='URL prefix, e.g. "/blogs" for project pages, "" for domain root',
    )
    args = ap.parse_args()
    files = freeze(Path(args.out), args.base_path)
    print(f"froze {len(files)} files -> {args.out}  (base-path: {args.base_path!r})")
    for f in files:
        print("  " + f)


if __name__ == "__main__":
    main()
