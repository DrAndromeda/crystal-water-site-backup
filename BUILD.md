# Build pipeline (static site, Python 3 + Pillow, no CMS)

Edit sources, then run in this order (all scripts are idempotent, run from repo root):

| Step | Command | What it does |
|---|---|---|
| 1 | `python3 build_new.py <dir>` | New/upgraded RU articles from `<slug>.ru.txt` (TITLE/DESC/CRUMB/===MAIN===) using the clean article template |
| 2 | `python3 build_ua.py <dir>` | UA pages from RU pages + translated `<slug>.txt`; UA canonical/hreflang; `sitemap-ua.xml` |
| 3 | `python3 build_core.py` | Content blocks (steps, price table, FAQ, why-us, reviews, map) + FAQPage / LocalBusiness / BreadcrumbList JSON-LD on core pages |
| 4 | `python3 postprocess.py` | WebP + AVIF (`<picture>`), width/height, srcset, heading order, a11y attributes, noopener, noscript form fallback, YouTube click-to-load facade |
| 5 | `python3 build_hub.py [new slugs]` | Regenerates the article cards on `articles.html` / `ua/articles.html` (then re-run step 4) |
| 6 | `python3 build_seo.py` | `sitemap.xml` (with hreflang alternates), `llms.txt`, `llms-full.txt` |
| 7 | `python3 build_css.py` | Minifies CSS sources and bundles them to `css/b/*.min.css` (edit `css/*.css`, never the bundles) |
| 8 | `NODE_PATH=<dir with puppeteer-core> node build_critical.js` (needs `python3 -m http.server 8765` running) | Inlines above-the-fold CSS (desktop+mobile) in `<style id="cw-critical">` and loads the full bundle non-blocking (preload + noscript). Always the LAST build step; `build_css.py` undoes it before re-bundling |
| 9 | `python3 check.py` | Validator: unique titles/descriptions, one H1, canonical, hreflang reciprocity, JSON-LD, broken links/assets, orphans, tag balance, sitemap parity. Exit 1 on errors |

Design tokens and shared a11y/touch/responsive rules: `css/tokens.css`. Reusable blocks: `css/blocks.css`, demo `blocks.html` (noindex).
Server config: `.htaccess` (Apache/SherlockHost), `_redirects` (Netlify/Cloudflare), `404.html`.
URL structure decision: keep existing flat URLs (see `blog-structure-decision.md`, Variant A).
