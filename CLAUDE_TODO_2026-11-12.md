# Crystal Water — Master TODO

Source of detail: `IMPROVEMENTS.md` (full spec), `proposal.md` (client requirements),
`medical-claims-rewrite.md`, `images-mobile-performance-checklist.md`, `blog-structure-decision.md`.
This file is the checklist; the specs hold the "how".

## Status (verified 2026-11-17)
- Legacy site crystalwater.kiev.ua: HTTP 200 (MODX, still live)
- Staging: GitHub Pages, HTTP 200 (static redesign)
- Repo: clean, branch `main`
- Done: server cleanup (error_log, temp/backup folders), bots checked, no duplicates

> Infrastructure access (SSH host/port/user/key path, cPanel URL, internal IPs) was removed from
> this file because the repo is hosted on GitHub. Keep it in a private note (e.g. Obsidian vault).
> Note: it remains in git history of commits 95efb5f and earlier; rotate/ignore accordingly.

## Ground rules (from IMPROVEMENTS.md)
- Static HTML only, no CMS/DB. Don't break what already works (hero, 8-stage schema, price sections, header/footer).
- Every page: unique title (50–60), description (140–160), one H1, canonical, JSON-LD, Direct Answer (50–80 words), FAQ 3–5.
- Medical claims need a disclaimer. Prices visible everywhere. No filler words ("идеальная", "лучшая", "seamless"...).
- Brand colors `#0f5f96` / `#1e88c7` / `#00c2e6`.

## Phases (ordered; each ends with a commit)
Priority: 🔴 blocker · 🟡 important · 🔵 polish

### 🔴 Phase 1 — Audit & blockers
- [ ] Inventory all HTML pages vs. sitemap.xml and legacy site; list missing/duplicate pages (spec says 85+, repo has ~71)
- [x] Real phones/address are in use (only `IMPROVEMENTS.md` has the fake `+38 (067) 123-45-67` example; update it)
- [x] Removed `.bak`/`.backup` files and `.bak-articles/`
- [x] Duplicates merged: `prices`→`uslugi-i-tseny`, `tech`→`tekhnologii-ochistki`, `articles_updated` removed (also `ua/about|prices|tech`)
- [x] `MESSAGE_TO_SEND.txt` removed
- [x] Broken `obezzarazhivanie-vodi.JPG` reference removed (add a real image later)
- [ ] Confirm URL structure decision (`blog-structure-decision.md`) before any renames; set up 301 map from legacy URLs

### 🔴 Phase 2 — Medical claims & content safety
- [x] Home page claims rewritten per `medical-claims-rewrite.md`; disclaimer block added to 63 articles
- [ ] Still to review by hand: `lechenie-vodoj-s-naturalnyimi-otvarami.html`, `butilirovannaya-voda-nuzhna-dlya-poxudeniya.html`, `xolodnaya-voda-i-vliyanie-na-organizm.html` (need sources)

### 🔴 Phase 3 — SEO foundation
- [ ] Unique title/description/H1/canonical on every page (script a check, fail on duplicates/length)
- [x] `sitemap.xml` regenerated (71 URLs, fixed broken `uslugi-i-tseny` URL, added index); `robots.txt` cleaned (invalid `Host:` removed, AI bots allowed); `llms.txt` + `llms-full.txt` added
- [x] Full UA version: 68 pages in `/ua/` (`build_ua.py`), self canonical + hreflang ru/uk/x-default on both sides, `sitemap-ua.xml` has 69 URLs
- [ ] UA translations are machine-made — native-speaker proofreading before launch
- [ ] BreadcrumbList on every page

### 🟡 Phase 4 — Structured data
- [x] LocalBusiness/Organization/Product/Service on home; Article + BreadcrumbList on all articles
- [ ] LocalBusiness on `o-nas.html`, FAQPage on services
- [ ] Validate with Rich Results Test / schema validator

### 🟡 Phase 5 — Design system & blocks
- [x] Inline `<style>` blocks extracted into `css/article-basic.css`, `article-full.css`, `page-core.css`, `page-tech.css`, `css/pages/*`; unused stylesheets removed
- [x] `build_css.py` minifies CSS to `*.min.css` (pages link the .min files; edit sources, then re-run)
- [ ] Unify the two `:root` palettes
- [ ] Blocks: HowItWorks, PriceTable, ServiceCard, OrderForm, FAQBlock, WhyUs, ReviewCarousel, FooterMap
- [ ] Each: hover/focus/active states, works without JS

### 🟡 Phase 6 — Core pages content
- [ ] Home (800+ words), prices, delivery, contacts, coolers, filters, purification tech (500+ each)
- [ ] Concrete facts: TDS, pH, stages, volumes, prices, delivery zones/schedule

### 🟡 Phase 7 — Articles
- [ ] Rewrite/upgrade existing ~63 articles (800+ words, H2/H3, Direct Answer, FAQ, Article JSON-LD, internal links)
- [ ] Add the 8 new topics listed in `IMPROVEMENTS.md` §5

### 🔵 Phase 8 — Performance & images
- [x] lazy-load + width/height on all local images (CLS)
- [ ] AVIF/WebP conversion + srcset (`images-mobile-performance-checklist.md`)
- [ ] Minify CSS, inline critical CSS, no render-blocking JS

### 🔵 Phase 9 — Responsive & accessibility
- [ ] Test 320/375/390/430/768/1024/1440/1920; no horizontal scroll; tap targets ≥ 44px; burger menu; alt text everywhere

### 🔵 Phase 10 — QA
- [ ] Link checker (no 404s, no orphan pages), HTML validation
- [ ] Lighthouse: Perf ≥ 90, SEO 100, A11y ≥ 95; CWV LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1

### 🔵 Phase 11 — Deploy
- [ ] Staging sign-off by client → upload to SherlockHost → 301 redirects live → submit sitemap in Search Console

## Open questions for the owner
1. Real phone numbers / address / working hours for schema and footer?
2. Spec says "85+ pages" but repo has ~71 — which pages are missing?
3. Final URL structure: keep legacy flat URLs or move to `/blog/`, `/katalog-vody/` as in IMPROVEMENTS.md? (Changes need 301s.)
4. Is the GitHub repo public? If so, treat everything committed as public.
