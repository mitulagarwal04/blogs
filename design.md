# Jev Decision Index — Complete Design Breakdown (Lowest-Level Building Blocks)

> Source: `https://huggingface.co/spaces/multimodalart/jev-decision-index`
> Space ID: `multimodalart/jev-decision-index`
> Captured: 2026-09-25 (live edition: **Decision Index 0.2 / release-v2**)
> Type: **Hugging Face Static Space** — 100% static HTML + inline CSS + vanilla JS + static JSON. No backend, no build step, no framework.

This file strips the site to its atoms so you can rebuild something visually and structurally similar with zero guesswork. Every hex, font, size, shadow, radius, breakpoint, page, section, component, interaction, and data field is listed as found in the source.

---

## 1. Site Identity & Hosting (Exact)

- **HF Space:** `multimodalart/jev-decision-index`
- **Title:** `Jev Decision Index`
- **Emoji:** `🔬`
- **Short description:** `Benchmarks and news on various repros of TypeSafe's Jev`
- **SDK:** `static` (`sdk: static` in README frontmatter)
- **Header:** `mini`
- **Pinned:** `false`
- **Space thumbnail:** `https://huggingface.co/spaces/multimodalart/jev-decision-index/resolve/main/og.png`
- **Live host:** `https://multimodalart-jev-decision-index.static.hf.space`
- **Canonical URL (og:url):** `https://huggingface.co/spaces/multimodalart/jev-decision-index`
- **Region:** `us`
- **Likes (at capture):** `213`
- **Author:** `multimodalart` (HF Staff)
- **SHA (at capture):** `e8c3315b96e9a0b0f02cc43dd3cf62a6dc8c4316`
- **Storage used:** ~9.2 MB (`9212630` bytes)
- **Favicon:**
  - Index / Methodology: `huggies/decision-favicon.png`
  - News: `huggies/xray.png`

### 1.1 Complete File Manifest (from HF API `siblings`)

```
.gitattributes
README.md
check.js                    # 601 bytes, Node sanity-check for news.html
data/index-v0.1.json        # archived 0.1 bundle
data/index-v2.json          # 0.2 build output
data/index.json             # 695,885 bytes, LIVE bundle served by index.html
data/methodology-v0.1.json  # archived
data/methodology-v2.json    # 0.2 build output
data/methodology.json       # 244,672 bytes, LIVE bundle served by methodology.html
huggies/catching.png
huggies/curious.png
huggies/decision-favicon.png
huggies/decision.png        # hero mascot on Index + og card lockup
huggies/diffusor.png
huggies/fishing.png         # "Still not in the open" illustration (News)
huggies/greeting.png
huggies/growing.png
huggies/paper.png
huggies/rocket.png          # News footer illustration
huggies/xray.png            # News hero + Jev model page hero
index.html                  # ~58-59 KB, THE Index leaderboard (default page)
methodology.html            # Methodology audit page
news.html                   # ~80-85 KB, News / Tracker page
og-index.html               # 1200×630 stage that renders og.png
og-news.html                # older stage for News tab -> og-news.png
og-news.png
og.png                      # 2400×1260 social thumbnail (rendered at 2x)
refresh.js                  # 2,636 bytes, Node script to refresh X/GitHub/Hub metrics in news.html
style.css                   # 388 bytes, HF DEFAULT PLACEHOLDER ONLY - NOT USED
```

> **Critical no-mistake note:** `style.css` is **not** the site stylesheet. It is the Hugging Face default 404/card boilerplate (`body{padding:2rem;...} .card{max-width:620px;...}`). All real styling is in **inline `<style>` blocks inside each HTML file**. If you copy `style.css` you get nothing.

### 1.2 README Frontmatter (Exact)

```yaml
title: Jev Decision Index
emoji: 🔬
colorFrom: yellow
colorTo: blue
sdk: static
header: mini
pinned: false
short_description: Benchmarks and news on various repros of TypeSafe's Jev
thumbnail: https://huggingface.co/spaces/multimodalart/jev-decision-index/resolve/main/og.png
```

### 1.3 Data Pipeline (How Numbers Get In)

- Builder lives **outside** the Space in `typesafe-diffusion-lab` checkout:
  - `evaluation/reproductions/build_leaderboard.py` → writes `data/index.json` from `capability-indices.json` + `entrant-metadata.json` + per-run `benchmark-summary.json` + Jev release report.
  - `build_methodology.py` → writes `data/methodology.json`.
  - `evaluation/reproductions/answer_gaps.py` → mines refusal messages → `answer-gaps.json` → picked up by build.
  - `evaluation/reproductions/edition.py` → `PANEL_V02` defines 0.2 panel.
- To switch editions: `build_leaderboard.py --suite release-v2` writes `data/index-v2.json`; copy over `data/index.json`. Same for methodology. Site now serves 0.2 this way; 0.1 archived as `data/index-v0.1.json`.
- Static `<title>` and `og:title` in HTML are **no-JS fallbacks** and must be bumped by hand per edition (currently `Decision Index 0.2`).
- JS loads data with cache-buster: `fetch('data/index.json?v='+Math.floor(Date.now()/6e5))` (same for methodology).
- News data lives in **one JS array `ITEMS`** at bottom of `news.html`. Add/edit by PR. Metrics snapshot date: **2026-09-24** (will drift).
- `refresh.js` refreshes metrics: X via `api.fxtwitter.com/status/<id>`, GitHub stars via `gh api repos/<repo> --jq .stargazers_count`, Hub likes via `huggingface.co/api/models/<repo>`.
- `check.js` validates: `CATS` order, `ITEMS` count, orphans, max desc length, top-5 trending per cat.
- `og-index.html` reads live from `data/index.json` and is screenshotted at **2x with headless Chrome** to produce `og.png`.

---

## 2. Global Visual System (Shared Across All Pages)

### 2.1 Design Language

- **Style:** Warm-paper neo-brutalist / "outlined sticker" look (credited: *Visual identity and outlined Huggies from HF Huggiverse (Chunte/HFBA)*).
- **Signature treatments:**
  - 2px–2.5px solid `#232323` ink outlines on every card/panel/button/chip.
  - Hard offset shadows, no blur: `3px 3px 0 #232323` (small), `4px 4px 0` (cards), `5px 5px 0` / `6px 6px 0` / `8px 8px 0` (panels/dialogs).
  - Hover = `translate(-1px,-1px)` + shadow grows by 1px.
  - Active/press = `translate(2px,2px)` + shadow shrinks.
  - Yellow highlighter: headings use `<mark>` with yellow bg + 4px radius; title underline uses `::after` yellow bar rotated -1deg.
  - Fully rounded pills: `border-radius: 999px` for switches, chips, bands, buttons, pills, badges.
  - Cards: `12px–22px` radius; panels: `14px`; missing/callout: `26px`.

### 2.2 Exact Color Palette (`:root` in `index.html` / `methodology.html`)

| Token | Hex | Usage |
|---|---|---|
| `--bg` | `#E9E6DD` | warm cream page background |
| `--surface` | `#FBF8F1` | card/panel surface (warm off-white) |
| `--ink` | `#232323` | charcoal ink: text, outlines, shadows |
| `--soft` | `#55524B` | secondary text (index/methodology) |
| `--muted` | `#8C8C8C` | tertiary text, axis labels |
| `--line` | `#D8D3C8` | hairline borders, table row dividers, chart grid base |
| `--paper` | `#FFF1C6` | pale paper tint (stat accent) |
| `--yellow` | `#FFD21E` | PRIMARY accent: key tile, active switch/chip, table header, highlights, NEW badges |
| `--orange` | `#FF9D00` | GLi family, head/adapter bars, Space badges |
| `--blue` | `#3B7CF6` | autoregressive, inference-technique, links hover |
| `--red` | `#EF3E36` | loss/negative, pareto frontier stroke, ✕ bullets, unanswered bars |
| `--purple` | `#A855F7` | diffusion, full fine-tune, Explainers |
| `--green` | `#3E8E5E` | encoder, gain/positive, NEW badge bg, Diffusion (News) |
| `--ar` | `#3B7CF6` | alias: autoregressive |
| `--diff` | `#A855F7` | alias: diffusion |
| `--enc` | `#3E8E5E` | alias: encoder |
| `--gli` | `#FF9D00` | alias: GLi family |
| `--jev` | `#232323` | alias: Jev (black) |

**`news.html` extras (same + these):**

| Token | Value |
|---|---|
| `--header-bg` | `rgba(233,230,221,.92)` (sticky header) |
| `--muted-2` | `#555555` (body secondary on News) |
| `--border` | `#D8D3C8` (same as `--line`) |
| `--blue-soft` | `#B9C7FF` (demo badges) |
| `--pink` | `#F87171` (Prior-art category + paper badges) |

**`og-index.html` (social card) root:** `--bg:#E9E6DD; --surface:#FBF8F1; --ink:#232323; --soft:#55524B; --yellow:#FFD21E` only.

### 2.3 Semantic Color Maps (Must Match to Look Right)

**Architecture / technique dot (`ARCH` → class → hex):**

| Technique label | Class | Hex |
|---|---|---|
| `autoregressive` | `a-ar` | `#3B7CF6` blue |
| `diffusion` | `a-diff` | `#A855F7` purple |
| `encoder` | `a-enc` | `#3E8E5E` green |
| `GLi family` | `a-gli` | `#FF9D00` orange |
| other / unknown | `a-other` | `#bbbbbb` grey |
| Jev reference | `a-jev` | `#232323` black |

JS: `const ARCH={'autoregressive':'a-ar','diffusion':'a-diff','encoder':'a-enc','GLi family':'a-gli'};` + `ARCHC` map to hex.

**Model kind pills (`KINDC` → class → bg):**

| Kind label | Class | Pill BG |
|---|---|---|
| `inference technique` | `k-tech` | `#DCE7FB` pale blue |
| `full fine-tune` / `fine-tune` | `k-full` | `#F1DDF8` pale purple |
| `LoRA` / `LoRA + head` | `k-lora` | `#DDEFE3` pale green |
| `head / adapter` | `k-head` | `#FFE7BF` pale orange |
| `pre-trained` | `k-pre` | `#ECEAE2` warm grey |
| `Jev (reference)` | `k-jev` | `#232323` black bg, white text |
| other | `k-other` | `#bbbbbb` |

JS: `KINDCOL={'k-tech':'#3B7CF6','k-full':'#A855F7','k-lora':'#3E8E5E','k-head':'#FF9D00','k-pre':'#bbbbbb','k-jev':'#232323','k-other':'#bbbbbb'}`.

**News category colors (`CATS` in `news.html`):**

| ID | Short | Full name | Color var | Text color |
|---|---|---|---|---|
| `decode` | Decoding | Parallel constrained decoding on stock models | `var(--blue)` `#3B7CF6` | `#fff` |
| `diffusion` | Diffusion | Diffusion LMs run in "Jev mode" | `var(--green)` `#3E8E5E` | `#fff` |
| `trained` | Trained | Trained Jev-like heads & fine-tunes | `var(--yellow)` `#FFD21E` | `var(--ink)` |
| `prior` | Prior art | "This already exists" prior-art claims | `var(--pink)` `#F87171` | `var(--ink)` |
| `explain` | Explainers | Architecture speculation, explainers & benchmarks | `var(--purple)` `#A855F7` | `#fff` |

**Index capability areas (5 + games folded):**

| ID | Label | Note |
|---|---|---|
| `knowledge` | Knowledge & Reasoning | includes folded Games |
| `language` | Language Understanding | split from Language in 0.2 |
| `retrieval` | Retrieval & Classification | split from Language in 0.2 |
| `tools` | Tools & Automation | — |
| `arts` | Arts & Human Taste | — |
| `games` | Games & Strategy | weight 0, folded into Knowledge; 6 interactive envs left out (MiniWoB++, Boxoban, RTFM, ScienceWorld, Hanabi, Codenames) |

Area colors come from `data/index.json` `categories[].color` and are applied as `--c` on cards/bars.

**Chart series (radar):** `SERIES=['#3B7CF6','#FF9D00','#A855F7']` (blue, orange, purple) for top-3 models; Jev always `#232323` with `rgba(35,35,35,.10)` fill; random baseline `#8C8C8C` dashed `4 3`.

### 2.4 Typography (Exact)

**Google Fonts link (all pages):**
```
https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=Chewy&display=swap
```
+ `preconnect` to `fonts.googleapis.com` and `fonts.gstatic.com` (crossorigin).

| Role | Stack | Usage |
|---|---|---|
| Display | `'Chewy','Source Sans 3',cursive` (`--display` / `--font-display`) | H1, H2, big numbers (`.tile b`, `.score`, `.rank`), category titles |
| Body | `'Source Sans 3',system-ui,sans-serif` (`--body` / `--font-body`) | paragraphs, base `17px/1.55` (Index) / `line-height:1.5` (News) |
| Mono | `'IBM Plex Mono',ui-monospace,monospace` (`--mono` / `--font-mono`) | nav, chips, labels, table headers, meta, buttons, tooltips, captions |

**Type scale (desktop):**
- Hero H1: `clamp(44px,7vw,82px)` Index; `clamp(2.4rem,8vw,6rem)` News; `clamp(40px,6.5vw,72px)` Methodology; line-height `1`, weight `400` (Chewy has no bold).
- H2 section: `30px` Chewy 400.
- Hero sub: `19px` (Index/Methodology), `clamp(16px,1.9vw,19px)` News, max-width `700px` (Index) / `46rem` (News) / `720px` (Methodology).
- Meta: `12px` mono, `letter-spacing:.03em`, color soft/muted.
- Tile number: `30px` Chewy; tile label: `11px` mono uppercase-ish `letter-spacing:.04em`.
- Table header: `11px` mono uppercase `letter-spacing:.06em`, yellow bg.
- Table body: `15px` (Index), `14.5px` (Methodology).
- Score: `24px` Chewy (`26px` `.big`).
- Buttons/chips: `11–13px` mono.

### 2.5 Layout & Spacing Atoms

- **Max width:** `1180px` (`main`, `.container`), centered `margin:auto`.
- **Page padding:** `0 28px 80px` desktop → `0 16px 60px` mobile (≤640px).
- **Subnav negative bleed:** `margin:0 -28px 22px` (Index) to make sticky bar full-bleed inside `main`.
- **Grids:**
  - `.tiles`: `repeat(5,1fr)` gap `14px`, margin `0 0 46px`; `.tiles.four`: `repeat(4,1fr)` (model pages).
  - `.cats`: `repeat(auto-fit,minmax(360px,1fr))` gap `18px`.
  - `.bgrid` (benchmark cards): `repeat(3,minmax(0,1fr))` gap `16px`.
  - `.grid3`: `repeat(3,1fr)` gap `14px`; `.grid2`: `repeat(2,1fr)`; `.profile`: `repeat(auto-fit,minmax(170px,1fr))`.
  - News `.grid`: `repeat(auto-fill,minmax(300px,1fr))` gap `22px`, margin-top `34px`.
  - `.calgrid`: `1fr 1fr` gap `26px`; `.cat-grid`: `minmax(0,1fr) 300px` gap `18px`.
- **Panel:** `background:surface; border:2px solid ink; radius:14px; shadow:6px 6px 0 ink; overflow:hidden`. `.pad`: `padding:18px 22px 14px/16px`.
- **Card:** `border:2px solid ink; radius:12px; padding:16px 18px; shadow:4px 4px 0 ink`. News card: `2.5px` border, `22px` radius, `16px 16px 14px` padding, `5px 5px 0` shadow, hover `translate(-2px,-2px)` + `7px 7px 0`.
- **Buttons (`.btn`):** mono `13px`, `2px` ink border, `999px` radius, `9px 18px` padding, surface bg, `3px 3px 0` shadow; `.primary`: yellow bg.
- **Chips (`.band`, `.achip`):** mono `12.5px`, `2px` ink border, `999px`, `6px 14px`, white bg, `2px 2px 0` shadow; `.on`: yellow bg + ink text.
- **Pills (`.pill`):** mono `10.5px` uppercase `letter-spacing:.05em`, `1.5px` ink border, `999px`, `1px 8px`, white bg.
- **Table:** `border-collapse:collapse; width:100%`; `th` yellow bg + `2px` ink bottom border; `td` `13px 14px` + `1px` line bottom; row hover `#FFFCEF`; Jev row `#F3EFE3` + `2px` ink bottom border; sorted col highlight `th.on:#FFE26B; td.on:#FFF8D6`.
- **Footer:** `margin-top:54px/60px; border-top:2px/2.5px solid ink; padding-top:16px/30px; mono 12px soft/muted; flex space-between wrap`.

### 2.6 Breakpoints (Exact)

- `980px`: `.tiles`→3col, `.grid3`→1col, `.cat-grid`→1col, `.model-top`→1col (standings static).
- `900px`: `.charts2`→1col; `.hscroll` columns `calc((100%-18px)/1.6)`; `.bgrid`→2col; `.calgrid`→1col; Methodology `.tiles`→3col, `.grid3/.grid2`→1col.
- `700px`: `.cats`→1col.
- `640px`: page padding `0 16px 60px`; `.tiles`→2col gap `10px`; tile `13px 14px`, number `26px` wrap; hero p `16px/17px`; subnav gap `6px 16px` font `11px`; `.hscroll`→`calc((100%-12px)/1.1)`; model hero `clamp(34px,10vw,52px)`; News stats→4col mini-grid with `1px border` + `color-mix(surface 55%, transparent)` bg, no shadow; News cat-head→1col; missing→1col; math block stacks.
- `600px`: `.bgrid`→1col.

### 2.7 Motion & Effects

- Transitions `0.08s–0.12s` on transform/box-shadow/background for chips/buttons/cards.
- Scroll hint nudge: `@keyframes nudge` (X, 1.6s ×3) and `nudgev` (Y); fades on `.scrolled`/`.at-end`/`.no-scroll`.
- Scroll fade gradient: `.scrollwrap::after` 72px right gradient `transparent → surface 85%`; vertical variant 64px bottom.
- News scroll-in tilt (gated): `@supports (animation-timeline: view())` + `prefers-reduced-motion: no-preference` → `.grid>.card {animation:hf-edge linear both; timeline:view(); range:cover 0% cover 100%}` with `perspective(1400px) rotateX(∓6deg) translateZ(-30px) scale(.97)` at edges, `none` on hover.
- Sticky blur: `backdrop-filter:blur(8px)` on subnav/search-header with `rgba(233,230,221,.94/.92)` bg.
- `scroll-behavior:smooth` (Methodology), `scroll-margin-top:52px/16px` for anchors.
- `body:has(dialog[open]){overflow:hidden}` when bench modal open.

---

## 3. Shared Chrome (Every Page)

### 3.1 Top Switch (`News // Index`)

```html
<div class="switch-bar"><nav class="switch" aria-label="Section">
  <a href="news.html">News</a><a href="index.html" class="on" aria-current="page">Index</a>
</nav></div>
```
- Container: flex center, `padding:18px 20px 0`.
- Pill container: surface bg, `2px` ink border, `999px`, `4px` padding, `3px 3px 0` shadow, mono `13px` uppercase `letter-spacing:.04em`.
- Links: `6px 18px`, `999px`, soft color, no underline; `.on`: yellow bg, ink, weight 500.
- News page inverts `.on` to News. Methodology page shows `News | Index(on)` (no Methodology tab; Methodology is linked from Index subnav + footer).

### 3.2 Hero Pattern

- Centered, `margin:34px 0 14px/22px`.
- `.hero-row`: flex center, `gap:22px` (Index) / `18px` (News), wrap.
- Mascot: `.hero-huggy` `width:clamp(110px,13vw,168px)` (Index), `clamp(84px,12vw,150px)` flipped `scaleX(-1)` (News). Sources: `huggies/decision.png` (Index default + og), `huggies/xray.png` (News + Jev page).
- H1 with `<mark>` yellow highlight (`padding:0 .1em; radius:4px`). Index H1: `Decision <mark>Index 0.2[+starburst]</mark>`. News H1: `Jev <span class="hi">Reproductions</span> Tracker` (underline bar variant).
- Sub paragraph + `.meta` mono line: `suite v0.2 · Jev jev-1.13.0 · reproductions run on 1 x NVIDIA RTX PRO 6000 · updated YYYY-MM-DD` (date from `generated_utc.slice(0,10)`).

### 3.3 Footer Pattern

- Index/Methodology: `frozen suite · 121,057 requests · 43 benchmarks · 1 x NVIDIA RTX PRO 6000` left; `Not affiliated with TypeSafe AI · Decision Index 0.2 · news & artifacts` right (links soft, mono 12px).
- News: 4-paragraph explainer (contribute via PR to `news.html` ITEMS / @multimodalart; trending formula; snapshot drift 2026-09-24; Huggiverse credit) + `huggies/rocket.png` 120px right.

---

## 4. Page 1 — `index.html` (Decision Index Leaderboard)

**Head (exact):** `<title>Decision Index 0.2</title>`, meta description mentions *frozen 132,422-decision suite* (static fallback; live JSON is 121,057 requests — see §7), `og:type website`, `og:title Decision Index 0.2`, `og:description Open reproductions of Jev...`, `og:image .../resolve/main/og.png`. Fonts + huge inline `<style>` (§2). Body starts as `<main id="app"><div class="empty">Loading the index…</div></main>` then JS renders.

**Router:** `?model=<engine>` → model page; `?model=jev` → Jev report; `?bench=<id>` → bench modal/page; else overview. Functions: `currentEngine()`, `go()`, `route()`.

### 4.1 Overview Sections (in order)

1. **Hero** (see §3.2) + **What's-New starburst** (`.wn`): 92px rotated -12° badge overlapping `mark` (`top:-52%; right:-22%`; mobile 60px, `top:-100%; right:-12%`), hover/focus scales to -4°/1.07. Popover `.wn-pop` 380px card (title, list, mono links) on hover/focus/`.open`; mobile becomes fixed `left:16px; right:16px`.
2. **Sticky subnav:** `Summary | Head to head | Full results | Calibration | All benchmarks | Methodology(methodology.html)` — sticky `top:0 z:30`, mono `12px` uppercase `letter-spacing:.06em`, gap `6px 26px`, blur bg; hover = ink + yellow underline.
3. **`#summary` panel:** toolbar = `sizebar()` + `#legend`; charts:
   - `Decision Index` bar chart (`#bars`): horizontal? vertical bars per model, Jev black, others by kind color; click → model page; tooltip `.tip`.
   - Horizontally scrollable trio (`.charts2.hscroll`, snap-x): `Model size vs Decision Index (#sizescatter)` + `Calibration error vs Decision Index (#idxcal)` + `Median latency vs Decision Index (#scatter)`, each with **Pareto toggle** (`.pareto-btn` absolute top-right; `aria-pressed`; `.pareto-on` dims non-front `opacity:.3`, front gets 3px stroke, `.pfront` red `2.6px` path + grey leaders). Scroll hint pill `scroll →`.
   - X axes log-scale for latency/size; Y = index; green band `fast and strong · under 100ms, index 55+` (thresholds `LAT_CUT()=100`, `IDX_CUT()=55` raw / `42` skill).
4. **`#headtohead`:** `Jev against the three strongest open models in each capability area. Every spoke is one benchmark.` Grid `.cats` = `overviewCard()` (yellow-tinted `All five areas`, Jev + top-3 radar, 5 spokes = area scores) + 5× `categoryCard(c)` (top border `8px var(--c)`, icon SVG 20px, `category score · Jev and top 3`, radar if ≥3 spokes else lollipop, legend with rank circles, desc note explaining spokes/coverage/ForecastBench/baseline).
5. **`#fullresults`:** `Click a model for its complete benchmark-by-benchmark page. Sort any column.` Panel with second `sizebar()` + `#table` (`tableHTML()`). Columns: `# | model (swatch+link+variant+pills) | Decision Index (or Your index ✦) | 5 area cols | calibration (ECE) | size | answered | median latency`. Sort keys: `score, name, ece, size, coverage, latency, area:<id>`; dir arrows `↑/↓` via `th[data-dir]`. **Gate:** `TABLE_GATE=15` — shows 15 until `Show all N models +M` clicked, unless filtered/sorted (`tableFiltered()`). Tied ranks within `TIE=0.25` shown as `=N`. Row click → `?model=`. Jev row highlighted.
6. **Note under table:** answered = share of 121,057 with valid typed answer; unsupported = wrong; ECE in points lower-better; MMLU/GPQA/BFCL are own-accuracy on answered; Jev latency = hosted HTTP, not comparable.
7. **`#calibration`:** `Every answer comes with a probability...` Panel `.calgrid`: `stated confidence vs accuracy (#calscatter)` + `calibration ladder · ECE (#calladder)`.
8. **`#allbenchmarks`:** filter bar (`.benchbar` + area chips + `✦ index only` toggle) + `.bgrid` of `benchCard(id)`: top border `7px var(--c)`, `dataset` link + `✦ in the index` badge, metric + random, `ol.mini` top-5 (rank, name, bar, value; Jev bold even if rank>5), `Full ranking · N models` link → modal.
9. **Bench modal:** `<dialog id="benchdlg">` 960px max, `2.5px` ink border, `16px` radius, `8px 8px 0` shadow, `rgba(35,35,35,.45)` backdrop; head (H2 + close `38px` circle), lede, refs, meta, wide SVG figure (min-width 640px), full table.
10. **Frontier comparisons** (`frontierHTML()`): currently GPQA Diamond only — Jev first then ranked bars, yellow if `us`.
11. **Model-category deep dives** (below grid, per area): left table (model, score, gain vs Jev rail, base) + right radar-side; `Show more` gating.
12. **Footer + crumbs** (Back to index / prev-next model links).

### 4.2 Controls (Exact Behavior)

- **Size bands:** `SIZE_STOPS=[350M,700M,3B,10B,∞]`, labels `SIZE_TICKS=['<350M','350M–700M','700M–3B','3B–10B','10B+']`. Click band = solo; click again = multi; empty = reset to all; `All sizes` button hidden when all on. Jev always passes; unknown size passes only when all on. Regex `HAS_SIZE=/\d+(\.\d+)?\s*[BM](?![a-z])/i` decides if name already shows size.
- **Area chips (`.achip`):** dot `9px` circle in area color; `.on` yellow; selecting recomputes `scoreOf()` = mean of selected areas (label becomes `Your index · <short names>`), highlights `th/td.on`, filters charts/table.
- **Sorting:** `state={bands:all, areas:Set(), sortKey:'score', sortDir:'desc', expanded:Set(), benchArea:'', benchIndexOnly:false, showAll:false}`.
- **Tooltips:** `.tip` (charts) / `.gtip` fixed 300px / `.stip` fixed min(300px, vw-16px); `.info` 18px circle + `.tipbox` 260px card on hover/focus/`.open`.
- **Scroll hints:** `.scrollwrap` gradient + pill; JS `wireScrollHint()` toggles `.scrolled/.at-end/.no-scroll`.

### 4.3 Model Detail Page (`?model=<engine>`)

- **Crumbs:** `← All models` + prev/next (`← name` / `name →`).
- **Two-col:** `.model-top` = main `1fr` + sticky `standings` 290px (static on mobile).
- **Hero:** Jev gets xray huggy + `Jev <mark>benchmark</mark>`; others `<mark>Long Name</mark>` + `Rank #N of 52 on the Decision Index...` + `.who` pills (kind, ~params, from base+technique dot, variant) + `.cta` buttons (Open on HF primary / GitHub/Code / Base model).
- **Tiles (4):** Decision Index (key yellow, + Jev ref + raw-accuracy note in skill mode) | rank | answered share | median latency (or ECE/calibration variant — see `tile()` calls).
- **Standings sidebar:** yellow head `Standings | Decision Index`, scrollable 226px list (rank, swatch, name ellipsis, value mono); current yellow bold, Jev tinted.
- **Per-category sections (`.cat-sec` + left `.cat-bar` 6px):** head (Chewy 26px + mono count), desc, grid (table + radar-side). Table cols mirror overview + gain rails (`.rail` 118px: grey base + green gain / red loss + ink Jev tick) + `gap` red mono + tracks.
- **Frontier + gaps + provenance** below; footer.

### 4.4 Key JS Constants (Exact)

```js
TIE=0.25; TABLE_GATE=15;
SIZE_STOPS=[3.5e8,7e8,3e9,1e10,Infinity];
SIZE_TICKS=['<350M','350M–700M','700M–3B','3B–10B','10B+'];
SERIES=['#3B7CF6','#FF9D00','#A855F7'];
HK = suite.headline ('balanced_skill' in 0.2, else 'balanced_raw');
IDX_CUT = chance?42:55; LAT_CUT=100;
```

Formatters: `fmt`=toLocaleString, `pct`=100*1dp+`%`, `ms`=≥1000→`s` 2dp else `ms`, `size`=≥1B→`B`, ≥1M→`M`, `one`=1dp.

---

## 5. Page 2 — `news.html` (Jev Reproductions Tracker / News)

**Head:** `<title>Jev Reproductions Tracker</title>`, desc *Tracking open reproductions... ranked by virality on X.* Icon `huggies/xray.png`, og `2400×1260` + Twitter `summary_large_image`. Same fonts. Own inline `<style>` (~CFBA palette comments).

### 5.1 Sections (in order)

1. **Switch** (News `.on`).
2. **Hero `#hero`:** `Jev Reproductions Tracker` (hi underline), sub *Who is rebuilding TypeSafe's Jev... grouped by kind of artifact.*, `.stats` sticker tiles (`#stats` JS-filled: counts, yellows/blues/papers).
3. **Sticky `#search-header`:** hidden `.search-wrap` (pill search w/ icon, `#q`, clear, `/` kbd — `display:none` for now) + `#cat-chips` row (label `Category` + 5 cat chips with dot/img + count) + `#type-chips` row (`Has`: GitHub repo / HF model / HF Space / Blog / Announcement post + `Sort` select: trending / likes / views / stars / Hub likes / newest). Mobile: chips become horizontal scroll; type row becomes 2-col grid.
4. **`#results-bar`** (hidden until filter): count + `Clear filters`.
5. **`#sections`:** 5× `section.cat` (order 1–5): head grid (rank circle `30px` in cat color + `cat-title-pill` mono `18–27px` in cat color + huggy img `110–190px` right) + desc + metrics (`m` pills) + `.grid` of cards.
6. **Card (`.card`):** top row (rank circle + `catpill` + badges right) → `h3` title link (hover underline in cat color) → `.by` mono author → `.desc` → `.quote` (left `3px` cat-color border, `14%` cat tint bg, `0 14px 14px 0` radius) → `.metrics` mono (♥/★/views/Hub + `.tr` trending pill) → `.links` dashed-top pill links (hover ink invert; `.x`/`.hf` variants). `dim` at `opacity:.35` when filtered out. Badges: `gh`(black) `hf`(yellow) `space`(orange) `blog`(paper) `demo`(blue-soft) `post`(grey) `pr`(purple) `paper`(pink) `soon`(orange dashed) `new`(green uppercase).
7. **`Load more`:** `.more-btn` per section with `.cnt` black count pill.
8. **`.missing` (`Still not in the open`):** paper bg `#FFF1C6`, `2.5px` ink, `26px` radius, `6px 6px 0` shadow, 2-col (text + `fishing.png` 120–200px); H2 Chewy `26–38px`; `ul` with red `✕` mono bullets (4 items: weights / RLCD / calibration / Hume promise + Solomon note).
9. **Footer** (§3.3) + **`#no-results`** empty state.
10. **Data:** `CATS[5]` + `ITEMS[...]` (~40+ artifacts at capture; fields: `cat,title,by{name,handle},desc,quote,links{tweet,gh,hf,hf2,space,blog,demo,pr,paper,site},m{likes,rts,views,stars,hfLikes},date,tags`). Trending = `likes + 5*stars + 8*hfLikes + views/500 + recency credit (≤8000 halving daily, scaled by engagement)`; ≤1-day-old gets green NEW. Promised-unreleased sorts last.

---

## 6. Page 3 — `methodology.html` (Audit the Index)

Same root/fonts/switch as Index. Starts `<main id="app"><div class="empty">Loading the methodology…</div></main>`, fetches `data/methodology.json`.

**Rendered order:** Hero (`Methodology · <mark>Index 0.2</mark>` + meta `edition ... · panel ... · Jev ... · reproductions on ...` + TOC pills: What it is / suite / Benchmarks / Formula / Rules / Entrants / Latency / Unanswered / Changelog / Edition notes? / Reproduce) → `#what` (2 paras + formal-note) → `#suite` (5 tiles: requests / scoreable / excluded / source cases·decisions / benchmarks + 3 cards: Reference / Reproductions / Three kinds + excluded-questions tables + Added-in-edition table) → `#benchmarks` (sortable table: # / benchmark+swatch+explainer / area / metric+lower-badge / cases+req / subset rule / random+method / in-index pill; click row expands `dl` detail: asks/kind/origin/adaptation/counts/filtering/scoring/baseline/tracks/Jev/references/sources/licence/index-rule/note/comparability/protocol) → `#formula` (`.math` block: benchmark score → chance-corrected `k_b=clip((s_b−r_b)/(1−r_b))` → area `K_c` → `I=100·⅕ΣK_c` + raw/breadth/lower rules + steps `ol` + area cards + chance table + worked example) → `#rules` (hard-rule cards + complete-run gate + eval rules + interactive) → `#entrants` (principle+naming, kind table, technique table, param precedence, base-model rule, all-entrants table) → `#latency` (2 cards: GPU vs HTTP + methods table) → `#gaps` (answered share + bar + mined reasons; `answer_gaps.py` note) → `#changelog` → `#notes` (lifts/variation/contamination/board changes) → `#reproduce` (GitHub `apolinario/decision-index` + `run.py/report_model.py/answer_gaps.py/compute_indices.py/build_*.py` + sha pins + buttons) → footer.

`.math` styling: surface panel, mono `15px` `line-height:1.9`, `.lab` 150px uppercase grey column (stacks mobile), sub/sup `11px`, code chips `#F3EFE3`.

---

## 7. Data Shapes (Live Numbers — No Mistakes)

**`data/index.json` (695,885 B):** keys `generated_utc, suite, categories, benchmarks, jev, models`.

- `suite`: `requests=121057`, `scoreable=120615`, `benchmarks=43`, `jev_benchmarks=42`, `panel=40`, `panel_full=40`, `categories=5`, `dropped=[6 interactive]`, `hardware='1 x NVIDIA RTX PRO 6000'`, `jev_version='jev-1.13.0'`, `panel_id='decision-index-0.2'`, `edition='release-v2'`, `label='Decision Index 0.2'`, `headline='balanced_skill'`, `corpus_sha256=b2b56df...`, `formulas=[balanced_raw, balanced_skill, breadth...]`, `lower_rules=[ForecastBench clip((0.25−Brier)/0.25)×coverage]`, `chance_levels`, `areas`, `not_in_index=[MMLU, ARC-Easy, ARC-Challenge, SimpleBench + ...]`.
- `models`: **51** entries. Each: `engine,name,long_name,variant,meta{kind,technique,served_params,params_estimated,params_from_name,trained_bytes,model_url,code_url,base_model,base_url,...},completed,counts{ok},lifted,calibration{acc,conf,ece,brier,over95,n,rel[10 bins],areas},gaps{share,reasons},latency{median,p95,mean},results{<bench_id>:{score,jev,metric,requests,answered,unsupported,errors,median_ms}},scores{balanced_raw,balanced_skill,breadth_skill,...},frozen_scores,categories[],benchmarks{},coverage,pending`.
- `categories`: 6 (`knowledge,language,retrieval,tools,arts,games`).
- `benchmarks`: 54 keyed dict; each `id,dataset,short,metric,explainer,baseline{value...},lower,range,cases,group,in_suite,interactive,references`.
- `jev`: `engine,name,version,edition,results,latency{http...},interactive,references,calibration,scores,categories,benchmarks,...`.

> **132,422 vs 121,057:** static `<meta name="description">` still says *132,422-decision suite* (0.1-era fallback). Live 0.2 JSON says **121,057 requests / 120,615 scoreable / 110,313 source cases / 536,776 fields**. Quote the JSON when citing current numbers; note the meta as fallback.

**`data/methodology.json` (244,672 B):** keys `generated_utc,edition,suite,excluded_questions,benchmarks[50],index,rules,entrants,latency,answer_gaps,changelog,added_benchmarks,reproduce,notes`.

- `suite`: `requests=121057, scoreable=120615, excluded=442, source_cases=110313, fields=536776, static_benchmarks=36, jev_static=42, repro=37, seed=20260919, corpus_sha256=b2b56d6f...`, hardware split `{jev, reproductions}`, origins, adaptation classes, licence caveat.
- `index`: `panel_id, panel=40, areas_count=5, shown='balanced_skill', formulas, functions, coverage, failures, uncertainty, steps, clarifications, worked_example, hashes{panel_proposal,corpus,baselines}, chance_paragraph/levels, lower_rules`.
- `entrants`: `principle,naming,kinds[],techniques[],counts{kind,technique,entrants},parameter_count_precedence,base_model_rule,entrants[]`.
- `latency`, `answer_gaps[]`, `changelog[]`, `added_benchmarks[7 in 0.2]`, `reproduce{github}`, `notes{lifts,lifts_not_applied,run_variation,contamination,board_changes,other}`.

**Edition deltas (0.1 → 0.2, from README):** 0.1 = 19-benchmark panel (ChessBench folded, Language split); 0.2 = **40 benchmarks, same 5 equal-weight areas** (`PANEL_V02`), minus stratified ToolRet/BRIGHT cut; ForecastBench vs baseline; entrant needs all 40; iSarcasmEval headline = track A; headline flips `balanced_raw` → `balanced_skill` (`(score−chance)/(1−chance)`, 0=random, 100=perfect); raw kept on model pages, breadth hidden.

---

## 8. Social / OG Stages

**`og-index.html` → `og.png`:** `#stage 1200×630`, `padding:18px 40px 0`; lockup (150px `decision.png` + Chewy `78px` `Decision <mark>Index 0.2</mark>`) + mono `14px` sub (`N open models · 40-benchmark index · 121,057 decisions each`) + panel (`3px` ink, `18px` radius, `8px 8px 0` shadow, `424px` tall): cap row (`12px` uppercase + legend) + bar SVG `W=1110 H=352 L=40 R=6/70 T=22 B=112`, top-20 bars + `+N more`, value labels `10.5px` mono, rotated names -58°, grid at 0–60 + foot (`suite v0.2 · Jev ... · ... · not affiliated`). Bar colors reuse `KINDC` map + `#232323` Jev. Render at **2× → 2400×1260** (`og:image:width 2400 height 1260`).

**`og-news.html` → `og-news.png`:** older News stage (same pattern, category colors).

---

## 9. Micro-Components Cheat Sheet (Copy-Paste Specs)

- **Switch:** `.switch{display:inline-flex;background:#FBF8F1;border:2px solid #232323;border-radius:999px;padding:4px;box-shadow:3px 3px 0 #232323;font:13px 'IBM Plex Mono';letter-spacing:.04em;text-transform:uppercase} a{padding:6px 18px;border-radius:999px;color:#55524B} a.on{background:#FFD21E;color:#232323;font-weight:500}`
- **Primary btn:** `font:13px mono;border:2px solid ink;radius:999px;padding:9px 18px;background:yellow;shadow:3px 3px 0 ink;hover:translate(-1px,-1px)+4px shadow`
- **Band/chip:** `font:12.5px mono;border:2px solid ink;radius:999px;padding:6px 14px;background:#fff;color:soft;shadow:2px 2px 0 ink;.on{background:yellow;color:ink}`
- **Tile:** `background:surface;border:2px solid ink;radius:12px;padding:16px 18px;shadow:4px 4px 0 ink;b{font:30px Chewy} span{font:11px mono soft}`
- **Panel:** `background:surface;border:2px solid ink;radius:14px;shadow:6px 6px 0 ink`
- **Table head:** `font:11px mono uppercase ls:.06em;background:yellow;padding:12px 14px;border-bottom:2px solid ink`
- **Swatch/dot:** `11px (table) / 9px (chip) / 8px (tag)` square `3px` radius or circle, `1.5–2px` ink border.
- **Rail (gain):** `height:9px;border:2px solid ink;radius:5px;background:#fff;width:118px;.base-fill:#B8B2A6;.gain-fill:#3E8E5E;.loss-fill:#EF3E36;u{tick:2px ink / dashed Jev}`
- **Track (model page):** `height:10px;border:2px solid ink;radius:6px`
- **Mini bar (bench card):** `height:8px;border:1.5px solid ink;radius:4px;background:#fff`
- **Unanswered bar (methodology):** `width:110px;height:9px;border:2px solid ink;radius:5px;fill:red width=share%`
- **Starburst:** `92px (60px mobile), rotate(-12deg), hover -4deg scale(1.07), Chewy white w/ text-shadow 1px 1px 0 rgba(0,0,0,.3)`
- **Tooltip:** `background:surface;border:2px solid ink;radius:10px;shadow:4px 4px 0 ink;padding:10px 12px;font-size:13px;min-width:200px`
- **Dialog:** `border:2.5px solid ink;radius:16px;shadow:8px 8px 0 ink;background:bg;width:min(960px,94vw);max-height:90vh;backdrop:rgba(35,35,35,.45)`
- **Standings:** `border:2px solid ink;radius:14px;shadow:5px 5px 0 ink;head{yellow,11px mono uppercase};row{grid:24px 11px 1fr auto;padding:7px 12px;border-bottom:1px line}`

---

## 10. What to Copy to Make Something Similar (Minimal Rebuild List)

1. **Tokens:** the 14 `:root` colors + 3 font stacks above. Page bg `#E9E6DD`, surface `#FBF8F1`, ink `#232323`, accent `#FFD21E`.
2. **Fonts:** load Chewy + Source Sans 3 + IBM Plex Mono from Google Fonts (exact URL §2.4).
3. **Shell:** `1180px` centered `main`, top `.switch-bar`, centered hero with mascot + `<mark>` H1 + mono meta, sticky subnav/filter bar with blur.
4. **Cards/panels/buttons:** ink borders + hard shadows + pill radii per §2.5/§9. Yellow = active/primary/sorted/header.
5. **Mascots:** 1–2 outlined cartoon PNGs (hero left of H1, 110–170px; section huggies 110–190px). Credit Huggiverse if reusing HF style.
6. **Homepage blocks in order:** hero → sticky nav → summary panel (toolbar + 1 bar chart + 3 scatters w/ pareto toggles) → head-to-head radar grid (1 overview + N category cards) → sortable full-results table (gated at 15) → calibration duo → benchmark card grid + modal → footer.
7. **Detail pages:** query-param router (`?model=`, `?bench=`), crumbs + prev/next, 4 key tiles, sticky standings rail, per-category table+radar, CTAs.
8. **News variant:** same shell, 5 color-coded categories, sticker stat tiles, chip filters + sort select, card grid with rank/badge/quote/metrics/links, `Still not in the open` paper callout, tilt-on-scroll (optional).
9. **Methodology variant:** same shell, TOC pills, 5 stat tiles, sortable benchmark table with expandable `dl` rows, mono `.math` formula block, rule/kind/technique tables, latency + gaps tables, changelog, reproduce panel.
10. **Data:** ship `index.json` + `methodology.json` with the exact keys in §7; JS renders everything client-side, no framework. Social card = separate `1200×630` HTML screenshotted at 2×.

---

## 11. Verification Notes (No-Mistake Checklist)

- [x] Hexes copied verbatim from `:root` (not eyedropped): bg `E9E6DD`, surface `FBF8F1`, ink `232323`, yellow `FFD21E`, blue `3B7CF6`, red `EF3E36`, purple `A855F7`, green `3E8E5E`, orange `FF9D00`, soft `55524B`, muted `8C8C8C`, line/border `D8D3C8`, paper `FFF1C6`, blue-soft `B9C7FF`, pink `F87171`.
- [x] `style.css` correctly identified as unused placeholder (388 B).
- [x] File list from live HF API, not guessed (includes `check.js`, `refresh.js`, `og-index.html`, `og-news.html`, 10 huggies, 6 data JSONs).
- [x] Live counts from `static.hf.space` JSON: 51 models, 54 benchmarks dict (index) / 50 rows (methodology), 40 panel, 121,057 requests — with 132,422 noted as stale meta fallback.
- [x] All section names/IDs match source (`#summary,#headtohead,#fullresults,#calibration,#allbenchmarks`, `?model=`, `?bench=`, `TABLE_GATE=15`, `TIE=0.25`).
- [x] Fonts, shadows, radii, breakpoints transcribed from CSS rules, not summarized.
- [x] News `CATS` (5) and Index areas (5+games) kept distinct; kind/arch color maps kept distinct.
- [x] Credits preserved: Huggiverse (Chunte/HFBA), unofficial / not affiliated with TypeSafe AI.

*Unofficial breakdown for rebuilding a similar look. Not affiliated with TypeSafe AI or the Space author.*