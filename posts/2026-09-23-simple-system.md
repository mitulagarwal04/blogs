---
title: "A simpler daily system"
date: "2026-09-23"
tags: ["habits", "code"]
excerpt: "One folder, one file per day, one commit. The boring system that finally stuck."
---

# A simpler daily system

Every productivity app failed me. This didn't:

- `posts/YYYY-MM-DD-slug.md` — one file per day, max 300 words
- Frontmatter: `title`, `date`, `tags`, `excerpt`
- Evening commit: `git add . && git commit -m "day: <title>"`

Why it works:

1. **Files beat apps.** Grep-able, backup-able, future-proof.
2. **300-word cap.** Short enough to do tired. Long enough to matter.
3. **Tags, not folders.** A post can be `habits` *and* `code`.

> Boring tools compound. Fancy tools distract.

This blog is just a pretty window over that folder. FastAPI reads, you read.
