# Crystal Water — Master TODO

Specs: `IMPROVEMENTS.md`, `proposal.md`, `BUILD.md` (pipeline), `blog-structure-decision.md` (URL decision A: keep flat URLs).
Infrastructure access details are NOT stored in this repo (keep them in a private note).

## Status (2026-11-17) — everything that can be done in code is done

Quality gates (run `python3 check.py`): 154 pages, 0 errors, 0 warnings. Local Lighthouse (mobile, headless, re-run after the final changes) on 17 sampled pages (home, prices, tech, about, contacts, both hubs, delivery article RU+UA, 4 video/embed articles, UA home/prices/article): Performance 95-100, Accessibility 100, Best-practices 100, SEO 100 (`blocks.html` and `404.html` are intentionally noindex). LCP ≈ 1.3-1.4 s, CLS ≈ 0. No horizontal overflow at 320/375/390/430/768/1024/1440/1920 px; all interactive targets ≥ 44 px.

### Phases
- [x] 1 Audit & blockers — duplicates merged (`prices`→`uslugi-i-tseny`, `tech`→`tekhnologii-ochistki`, `articles_updated` and 3 duplicate `/ua/` pages removed), junk/backups removed, URL decision documented (Variant A), 301 map in `.htaccess` + `_redirects`, `404.html`
- [x] 2 Medical claims — home rewritten; all 63 older articles rewritten with neutral claims + disclaimer block; scan finds no unsupported claims (remaining "не лечит" = negations)
- [x] 3 SEO foundation — unique title/description/H1/canonical everywhere (enforced by `check.py`), hreflang ru/uk/x-default reciprocal, `sitemap.xml` (+xhtml alternates) and `sitemap-ua.xml`, `robots.txt` (AI bots allowed), `llms.txt`/`llms-full.txt`, BreadcrumbList on every page
- [x] 4 Structured data — LocalBusiness (home, contacts RU+UA), Organization, Product, Service, Article, FAQPage (home, prices, tech, about, contacts, every article), BreadcrumbList; all JSON-LD parses (`check.py`)
- [x] 5 Design system & blocks — `css/tokens.css` (single palette), `css/blocks.css` + `blocks.html`: HowItWorks, PriceTable (cards on mobile), ServiceCard, OrderForm (existing, with noscript fallback), FAQBlock (native `<details>`, no JS), WhyUs, ReviewCarousel (CSS scroll-snap), FooterMap; hover/focus/active states
- [x] 6 Core pages content — home ≈ 860+ words, prices/tech/about ≥ 500, contacts with map+FAQ, cooler/filter/delivery pages upgraded to 800+
- [x] 7 Articles — all 71 articles (63 upgraded + 8 new) in RU and UA: 800+ words (all 142 pages incl. delivery article, checked by script), Direct Answer 50-80 words, FAQ + FAQPage JSON-LD, internal links
- [x] 8 Performance — critical CSS inlined (6.6 KB avg) + full bundle non-blocking, WebP + AVIF (`<picture>`) for all used images (~13 MB saved vs originals), , width/height (CLS), srcset 480/800w, lazy-load, YouTube click-to-load facade (no third-party cookies/requests until click), CSS minified + bundled into 9 files, deferred scripts, cache/compression rules in `.htaccess`
- [x] 9 Responsive & a11y — verified widths above, skip links, landmarks, focus-visible, AA contrast, labels, iframe titles, 44 px targets, reduced-motion
- [x] 10 QA — `check.py` (links, assets, orphans, tag balance, sitemap parity, hreflang, JSON-LD)
- [ ] 11 Deploy — see blocked list

## Blocked physically (cannot be done from code/this environment)
1. Inventory against the legacy MODX site (network to crystalwater.kiev.ua is not reachable from the sandbox; compare `sitemap.xml` with the live sitemap manually).
2. Native-speaker proofreading of the Ukrainian text (machine translation).
3. Verification with Google Rich Results Test / Search Console (online tools).
4. Real figures for extra facts (TDS values, delivery zones/fees) — not invented; add when provided.
5. Upload to SherlockHost, enable `.htaccess`, submit sitemaps in Search Console, client sign-off.
6. Missing source image `infographic-water-benefits.webp` (referenced only inside a comment in `infografik-o-neobxodimosti-i-polze-vodyi.html`).
