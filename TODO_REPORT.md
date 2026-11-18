# TODO Report — Crystal Water

Status snapshot of the website refresh. Build instructions: `BUILD.md`. Specs: `IMPROVEMENTS.md`, `proposal.md`, `blog-structure-decision.md`.
Infrastructure access details (SSH, cPanel, internal IPs) are intentionally NOT stored in this repo.

---

## 1. Finished

### Content and languages
- [x] 71 articles (63 existing rewritten + 8 new) in **Russian and Ukrainian**: 800+ words, Direct Answer (50–80 words), FAQ, internal links, Article JSON-LD. Delivery article extended to 840 words.
- [x] Full Ukrainian version: 77 pages in `/ua/` (articles, core pages, home), self-canonical + `hreflang` ru / uk / x-default, reciprocal on both sides, `sitemap-ua.xml`.
- [x] Core pages extended with real, site-sourced facts only: home (~900 words), prices (price table + worked first-order example), technologies, about, contacts (map + FAQ).
- [x] Text sweep (IMPROVEMENTS.md task 4): all unsupported medical/health promises, hype/AI-slop words, unsupported superlatives and clichés removed in RU + UA, including headers/footers. `lint_text.py` reports 0 hits.
- [x] Medical disclaimer block on every article; claims rewritten per `medical-claims-rewrite.md`.

### Structure, duplicates, URLs
- [x] Duplicates merged: `prices` → `uslugi-i-tseny`, `tech` → `tekhnologii-ochistki`, `articles_updated` and 3 duplicate `/ua/` pages removed; all links repointed; backup/junk files removed.
- [x] URL structure decision documented (Variant A: keep existing flat URLs). 301 map for removed pages in `.htaccess` and `_redirects`; `404.html`.
- [x] Article/page **sources moved into the repo** (`content/`), so every page can be rebuilt reproducibly.

### SEO and structured data
- [x] Unique title / description / H1 / canonical on every page (enforced by `check.py`).
- [x] `sitemap.xml` (with hreflang alternates), `sitemap-ua.xml`, `robots.txt` (AI bots allowed, service pages disallowed), `llms.txt`, `llms-full.txt`.
- [x] JSON-LD: LocalBusiness, Organization, Product, Service, Article, FAQPage, BreadcrumbList (every page). Local validator checks required properties per type and that every FAQ question is visible on the page; UA FAQ data rebuilt from the translated text.

### Design system and blocks
- [x] Single palette in `css/tokens.css`; reusable blocks in `css/blocks.css` (HowItWorks, PriceTable, ServiceCard, FAQBlock, WhyUs, ReviewCarousel, FooterMap, OrderForm with noscript fallback), hover / focus / active states, work without JavaScript, demo page `blocks.html` (noindex).
- [x] Blocks used consistently: every article has the FAQ accordion, service cards and ordering steps; core pages use the same blocks.

### Performance
- [x] WebP + AVIF (`<picture>`), real `width`/`height` (stale attributes corrected), `srcset` 480/800 w, lazy-loading, YouTube click-to-load facade (no third-party cookies until click).
- [x] CSS minified and bundled (10 files), critical CSS inlined per bundle (cascade-safe) with non-blocking full bundle, deferred scripts, cache / compression / security headers in `.htaccess`.

### Accessibility and responsive
- [x] Skip links, landmarks, focus-visible, AA contrast, labelled controls, iframe titles, noopener links, reduced-motion, heading order.
- [x] 44 px touch targets for navigation, buttons, footer and contact links; data tables scroll inside wrappers; long headings wrap; no horizontal overflow from 320 to 1920 px (verified on all page types).

### Tooling (all documented in `BUILD.md`)
- [x] `check.py` (titles, H1, canonical, hreflang, JSON-LD, links/assets/srcset, orphans, tag balance, sitemap parity), `lint_text.py`, `build_new.py`, `build_ua.py`, `build_core.py`, `build_blocks.py`, `postprocess.py`, `build_hub.py`, `build_seo.py`, `build_css.py`, `build_critical.js`.

### Latest verification results
- `check.py`: 154 pages, 0 errors, 0 warnings. `lint_text.py`: 0 hits.
- Full local Lighthouse run (mobile, headless, all 154 pages): Performance min 96 / avg 99.9, Accessibility min 95 / avg 99.7, Best-practices min 96 / avg 99.4, SEO 100 on every page, CLS max 0.01, LCP avg 1.19 s.
  **Caveat:** this run was on the build just before the last round of changes (shared blocks on all articles, text sweep, table wrappers, heading wrap, rebuilt critical CSS). It was **not repeated on the final commit.**
- On the final build only a targeted re-check was done (home, about and contacts in RU + UA and the two pages that had overflowed): no horizontal overflow, all tap targets ≥ 44 px. The all-page overflow/tap check on the final build was cancelled before it finished.

---

## 2. Not possible to do from the development environment (blocked)

| # | Item | Why it is blocked | What is needed |
|---|---|---|---|
| 1 | Inventory / comparison against the **legacy MODX site** (crystalwater.kiev.ua) | The sandbox has no network access to the live site | Compare `sitemap.xml` with the live sitemap and legacy URLs manually; add 301s for anything missing |
| 2 | **Native-speaker proofreading** of the Ukrainian text (77 pages) | All Ukrainian text is machine-translated; quality sign-off needs a human | A Ukrainian-speaking editor |
| 3 | **Google Rich Results Test / Search Console** validation | Online tools; require a public URL and an account | Run after deploy; local validator (`check.py`) covers required properties only |
| 4 | **Deploy** to SherlockHost: upload, enable `.htaccess`, HTTPS, submit sitemaps, client sign-off | Needs server credentials and the owner's approval | Owner / admin access |
| 5 | **Real figures**: TDS values, delivery zones and fees, extra price lists | Not available in the repo; deliberately not invented | Facts from the company; then add to the pages and `llms.txt` |
| 6 | Missing source image `infographic-water-benefits.webp` | File is not in the repository (referenced only inside an HTML comment in `infografik-o-neobxodimosti-i-polze-vodyi.html`) | The original image file |

## 3. Open items inside the code-doable scope (honest list)

- Full 154-page Lighthouse run and all-page overflow/tap-target check **on the final commit** were not repeated (see caveat above). Command sequence: `BUILD.md` steps 9–11, then Lighthouse over `python3 -m http.server`.

## 4. Housekeeping notes

- Commits made in this work were rewritten to the author `stoianov46 <kirillstoianov46@gmail.com>`. Branch `backup-before-author-rewrite` still holds the old commits (old email); delete it with `git branch -D backup-before-author-rewrite` when no longer needed.
- Nothing has been pushed to GitHub; the local `main` is ahead of `origin/main`.
