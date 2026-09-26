# Push to GitHub

Short version — the repo already exists locally, so it's just: new empty
GitHub repo → link it → push.

## Steps

1. **Create the repo on GitHub**: github.com → New repository → name it
   `blogs` (or anything) → **don't** tick "Add a README" → Create.
2. **Link and push** (run in this folder):

```bash
git add .
git commit -m "daily notes blog"
git branch -M main
git remote add origin https://github.com/<your-username>/blogs.git
git push -u origin main
```

3. Done. Later updates are just:

```bash
git add .
git commit -m "new post: <title>"
git push
```

## Notes

- `.gitignore` already excludes `.venv/`, caches, `.env`, and logs, so
  `git add .` is safe.
- First push will ask for your GitHub login — use a personal access token
  as the password (GitHub → Settings → Developer settings → Tokens).
- Never commit API keys or passwords. If you need secrets later, put them
  in a `.env` file (already ignored).
