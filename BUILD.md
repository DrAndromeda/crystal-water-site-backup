# Build pipeline (static site, Python 3 + Pillow, Node + puppeteer-core for critical CSS)

All article/page SOURCES live in the repo: `content/articles/<slug>.ru.txt|.ua.txt` (71 articles) and
`content/pages-ua/<slug>.txt` (Ukrainian main of core pages). Hand-written RU pages: `index.html`, `uslugi-i-tseny.html`,
`tekhnologii-ochistki.html`, `about.html`, `o-nas.html`, `articles.html`. Edit sources, then run (repo root, all idempotent):

| # | Command | What it does |
|---|---|---|
| 1 | `python3 build_new.py content/articles` | RU article pages from `<slug>.ru.txt` (TITLE/DESC/CRUMB/===MAIN===) using the clean template |
| 2 | `python3 build_ua.py content/articles` and `python3 build_ua.py content/pages-ua` | UA pages (RU page + translated main), UA canonical/hreflang, FAQPage JSON-LD rebuilt from the translated FAQ, `sitemap-ua.xml` |
| 3 | `python3 build_core.py` | Core-page blocks (steps, price table, FAQ, why-us, reviews, map) + FAQPage / LocalBusiness / BreadcrumbList JSON-LD |
| 4 | `python3 build_blocks.py` | Same shared blocks on every article: FAQ accordion, ServiceCards, HowItWorks |
| 5 | `python3 postprocess.py` | WebP + AVIF (`<picture>`), real width/height, srcset, heading order, a11y attrs, noopener, form noscript fallback, YouTube click-to-load |
| 6 | `python3 build_hub.py` then `python3 postprocess.py` | Article cards on `articles.html` / `ua/articles.html` |
| 7 | `python3 build_seo.py` | `sitemap.xml` (+hreflang alternates), `llms.txt`, `llms-full.txt` |
| 8 | `python3 build_css.py` | Minify + bundle `css/*.css` into `css/b/*.min.css` (edit sources, never bundles) |
| 9 | `NODE_PATH=<dir with puppeteer-core> node build_critical.js` (with `python3 -m http.server 8765` running) | Inline above-the-fold CSS per bundle (desktop+mobile), load the full bundle non-blocking. LAST build step; `build_css.py` undoes it before re-bundling |
| 10 | `python3 check.py` | Validator: titles/descriptions unique+length, one H1, canonical, hreflang reciprocity, JSON-LD validity + required properties per schema type, FAQ questions visible on page, broken links/assets/srcset, orphans, tag balance, sitemap parity. Exit 1 on errors |
| 11 | `python3 lint_text.py [-v]` | Text lint (IMPROVEMENTS.md task 4): hype/AI-slop words, unsupported "best/ideal/unique" claims, clichés, medical and health promises, RU + UA, whole page incl. header/footer. Exit 1 on hits |

Design tokens + shared a11y/touch/responsive rules: `css/tokens.css`. Block styles: `css/blocks.css`, demo: `blocks.html` (noindex).
Server config: `.htaccess` (Apache), `_redirects`, `404.html`. URL structure: keep flat URLs (`blog-structure-decision.md`, Variant A).
