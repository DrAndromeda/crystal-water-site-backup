# Crystal Water — Claude Code Master TODO / Website Specification

Last consolidated: 2026-11-17
Production domain: https://crystalwater.kiev.ua/ (legacy live MODX website)
Static redesign / staging: https://drandromeda.github.io/crystal-water-site-backup/
Prototype repository: https://github.com/DrAndromeda/crystal-water-site-backup
Languages: Russian (RU) and Ukrainian (UK/UA as implemented; verify language codes)
Architecture decision: static HTML, no CMS/database unless the owner explicitly changes this
Migration status: NOT APPROVED by this TODO. Preserve the live MODX website until explicit approval.

> This is the master implementation brief for Claude Code. Inspect the real repository and live website, implement safe changes in ordered phases, test them, and update this checklist with evidence. A Git commit or staging preview is never proof of production deployment.

## 0. Non-negotiable project decisions and safety rules

- The live MODX site remains the production source of truth until the owner explicitly approves migration.
- Keep the existing indexed article URLs and slugs. The owner selected Option A: preserve flat legacy article URLs and organize articles through the existing /voda-h2o-stati/ hub. Do not migrate articles to /blog/.
- Keep the site static HTML with no CMS or database unless the owner explicitly changes this decision.
- Mobile navigation must be static and fully visible. No hamburger menu, no collapsed/hidden mobile navigation. This explicit decision overrides generic design preferences.
- Preserve all useful original content and assets. Do not use destructive mirroring or overwrite commands against production.
- Start with git status, branch, latest commit, file inventory and a dated backup/rollback point. Do not overwrite uncommitted user work.
- Do not deploy, change DNS, replace MODX, or alter production files without explicit owner approval and a verified backup/rollback plan.
- Never invent laboratory results, purification stages, pH/TDS/mineral values, certificates, licenses, medical benefits, testimonials, ratings, prices, delivery promises or technical capabilities.
- Do not expose or commit customer records, bot data, tokens, passwords, hosting credentials, database credentials or private operational files.
- Mark unverified claims and missing evidence as BLOCKED / OWNER CONFIRMATION REQUIRED.

## 1. Project goal and quality benchmark

Create a modern, trustworthy, conversion-focused water-delivery website for the actual Crystal Water business serving Brovary and Kyiv, while preserving URL equity, brand identity, useful legacy content and the existing production service until migration is approved.

Apply the engineering and editorial lessons from FORMA and CreativeLAB:
- A consistent design system and professional page templates.
- Strong content hierarchy, readable typography, clear navigation and polished responsive layouts.
- Useful, substantial content rather than filler or keyword repetition.
- Natural localization, not literal machine translation.
- Fast, accessible pages with optimized original imagery.
- Crawlable HTML, accurate metadata, reciprocal hreflang and valid structured data.
- A disciplined staged rollout with measurable QA and rollback.

Do not copy FORMA's luxury design or CreativeLAB's agency aesthetic. Preserve Crystal Water's recognizable blue identity.

## 2. Phase 1 — Baseline, repository mapping and security (P0)

- [ ] Inspect the prototype repository: branch, commit SHA, git status, file tree, scripts, assets, CSS, JS, generated output and existing documentation.
- [ ] Inspect the live MODX website without modifying it. Record current page inventory, URLs, content, assets, navigation, contact details and behavior.
- [ ] Compare the prototype with production and available historical snapshots. Identify missing pages, images, fonts, styles, scripts and content.
- [ ] Measure the real current counts of HTML pages and articles. Earlier handoffs mentioned 66+, 71+, 85 pages and 63 articles; these are historical claims, not current verified counts.
- [ ] Inventory RU and UK page pairs and record HTTP status, final URL, title, description, H1, canonical, hreflang, breadcrumbs, robots and internal links.
- [ ] Review all existing helper scripts before running them: fix_site_issues.py, add_hreflang.py, generate_sitemap_ua.py, generate_article_jsonld.py and unify_social_links.py. Understand their exact modifications and backup behavior.
- [ ] Read the project documents: IMPROVEMENTS.md, INSTRUCTIONS_FOR_NEXT_ASSISTANT.md, TZ-1-full-spec.txt, proposal.md, medical-claims-rewrite.md, blog-structure-decision.md, images-mobile-performance-checklist.md and HANDOVER.md. Resolve contradictions in favor of explicit owner decisions in this TODO.
- [ ] Create a dated backup/rollback point before edits.

### Security review — mandatory blocker

The historical public repository DrAndromeda/crystalwater.kiev.ua was reported to contain operational-looking filenames such as .htpasswd, .my.cnf, kickstart.php, php-cgi.core and a manager/ directory. This does not prove that credentials are valid, but it requires a security review.

- [ ] Review repository history for accidentally committed credentials, database configuration, hosting data, private backups, crash dumps, customer data or tokens.
- [ ] If real secrets were ever committed, rotate/revoke them immediately. Deleting the latest copy does not remove historical exposure.
- [ ] Plan any history cleanup carefully, with owner approval and coordination for existing clones/forks.
- [ ] Never fetch, reproduce, quote, copy or commit the contents of suspected credential/configuration files as part of website work.
- [ ] Never run kickstart.php, import a backup, expose manager/ or copy operational MODX files into the static public site.
- [ ] Keep the original production backup private and access-controlled.
- [ ] Treat historical bot customer files, including clients.json, Telegram identifiers, order history and bot logs, as confidential. Never place them in public repositories, website assets, HTML, JSON-LD or reports.

## 3. Phase 2 — Content and business accuracy (P0)

### Commercial facts and pricing

- [ ] Use the current confirmed price consistently: 150 UAH per bottle plus a 350 UAH refundable bottle deposit (залог). Do not reintroduce the outdated 100 UAH figure.
- [ ] Show the product, bottle price, refundable deposit and ordering method clearly near the top of the homepage and on relevant price/order pages.
- [ ] Explain the deposit as refundable and distinguish it from the bottle's purchase/delivery price. Do not present it as a non-refundable fee.
- [ ] Verify all other prices, business tariffs, minimum order quantities, offers, delivery zones, schedules, payment methods and conditions against the owner's current instructions before publishing.
- [ ] Keep every price table, CTA, FAQ, metadata snippet and translated page consistent.
- [ ] Display currency and units explicitly. State when a price is per bottle, per delivery, per order or a deposit.
- [ ] Never copy outdated prices from archived pages without checking.

### Technology and product claims

- [ ] Audit every description of purification, filtration, bottling, mineralization and quality control against current technical documentation.
- [ ] The previous handoff explicitly warned that stages 05–07 of the claimed “8 stages of purification” were assumptions. Do not invent or publish them. Confirm the actual process with the owner and technical evidence.
- [ ] Verify reverse osmosis, carbon filtration, ozonation, UV treatment and any other claimed process individually before stating that it is used.
- [ ] Verify pH ~7.5, TDS, mineral composition, laboratory testing, certificates and other numerical/quality claims against current primary lab reports or official documentation.
- [ ] If evidence is missing or expired, remove the numerical claim or mark it for owner confirmation. Do not imply a test or certificate exists.
- [ ] Do not fabricate laboratory imagery, certificates, awards, endorsements or production photographs.

### Contact and delivery facts

- [ ] Verify phone numbers, Telegram/social accounts, address, opening hours, service areas and delivery terms with the owner/current business source.
- [ ] Do not assume that historical footer details or old bot accounts remain active.
- [ ] Keep contact details identical across header, footer, contact page, structured data and language versions.
- [ ] Make call and order actions clear and easy to use on mobile.

## 4. Phase 3 — Medical/editorial compliance (P0)

- [ ] Search all RU and UK content, metadata, structured data and image text for health claims, including “лечит”, “стимулирует иммунитет”, “восстанавливает на клеточном уровне”, disease-prevention/cure promises, weight-loss promises and claims about an “ideal acid–alkaline balance”.
- [ ] Apply the approved neutral rewrites in medical-claims-rewrite.md only where they remain factually accurate.
- [ ] Fully rewrite xolodnaya-voda-i-vliyanie-na-organizm.html and butilirovannaya-voda-nuzhna-dlya-poxudeniya.html, or temporarily remove them from navigation/indexing until reviewed. These articles were explicitly identified for full review, not superficial phrase edits.
- [ ] Review articles about daily water intake, pregnancy, breastfeeding, infants, children, weight loss, minerals, water composition and health effects with current reliable evidence.
- [ ] Distinguish general educational information from medical advice. Do not imply that Crystal Water treats, prevents or cures disease.
- [ ] Cite real, relevant primary or high-quality sources for scientific claims. Do not fabricate citations or overstate study findings.
- [ ] Remove unsupported universal water-intake rules, detox claims, immunity claims, weight-loss guarantees and disease-related promises.
- [ ] Add a suitable informational disclaimer where health education remains. A disclaimer does not make an unsupported or misleading claim acceptable.
- [ ] Keep editorial review date and source references where appropriate; do not invent author credentials or medical reviewer identities.

## 5. Phase 4 — Content architecture and page quality (P0)

### Homepage and conversion pages

- [ ] The homepage must explain what the product is, who it is for, delivery geography, current price/deposit and how to order without forcing visitors to search through the site.
- [ ] Use a clear H1, concise introduction, visible product/price information, delivery explanation, verified process/quality information, clear ordering CTA and useful FAQ.
- [ ] Ensure price, technology, delivery, contact and article hub pages are easy to reach.
- [ ] Keep the product and order action prominent but not intrusive.

### Service, price and technology pages

- [ ] Provide clear, detailed pages for delivery, prices, business/customer terms and water treatment technology where those pages reflect real offerings.
- [ ] Explain what is included, who the service is for, delivery area, ordering steps, conditions, payment and limitations.
- [ ] Use clear price tables with the 150 UAH bottle price and 350 UAH refundable deposit wherever relevant; other figures require verification.
- [ ] Make the distinction between product price and refundable container deposit unmistakable.
- [ ] Ensure all tables are mobile-readable and do not cause horizontal overflow.
- [ ] Keep claims about the purification process aligned with verified documentation.

### Articles and editorial hub

- [ ] Preserve all existing article URLs and filenames.
- [ ] Keep /voda-h2o-stati/ as the logical article hub. Do not migrate to /blog/.
- [ ] Retain original useful content and improve it with accurate facts, useful examples, source citations and contextual internal links.
- [ ] Do not mass-generate thin pages or keyword-swapped articles.
- [ ] Every article must have one clear H1, logical H2/H3 structure, unique title/description, correct language and a clear date/source policy.
- [ ] Add concise direct answers and FAQs when they genuinely help readers.
- [ ] Use article schema only for real editorial articles and only with accurate visible author/date/headline/image information.
- [ ] Review RU and UK texts for native quality, consistent terminology, grammar and localized phrasing.

## 6. Phase 5 — Design, header, navigation and responsive behavior (P0)

### Brand and layout

- [ ] Preserve the Crystal Water blue identity. Existing palette reference: #0f5f96, #1e88c7, #00c2e6, #eaf6fc, white and readable dark text.
- [ ] Use a compact, blue, sticky header that remains readable and functional.
- [ ] Keep the logo clear and correctly proportioned. Verify logo and “Доставка воды” home links on staging and production.
- [ ] Use consistent typography, spacing, buttons, content widths, cards, tables and section hierarchy.
- [ ] Avoid excessive animation, oversized empty hero areas, clutter and generic stock imagery.

### Navigation — explicit owner decision

- [ ] Desktop may use horizontal navigation.
- [ ] Mobile navigation must remain static and fully visible. Do not implement a hamburger, collapsed menu, hidden drawer or menu that requires tapping to reveal the links.
- [ ] Allow navigation items to wrap cleanly and remain legible on narrow screens.
- [ ] Ensure the RU/UK language switcher leads to the equivalent page in the other language, not always to the language homepage.
- [ ] Use correct language attributes and direction; do not accidentally mark Ukrainian as Russian.
- [ ] Make phone and order actions visible without obscuring content.

### Footer and responsive testing

- [ ] Footer must stack naturally on mobile and include verified contact details, location/service area, Telegram/social links, navigation and copyright.
- [ ] Test at 320, 360, 375, 390, 430, 768, 1024, 1280, 1440 and 1920px.
- [ ] Check real iPhone and Android rendering where available.
- [ ] No horizontal overflow, clipped text, overlapping buttons, unreadable tables or tiny tap targets.
- [ ] If a sticky order bar exists, add sufficient page spacing so it never covers content or browser controls.
- [ ] Ensure keyboard focus, contrast and semantic controls are usable.

## 7. Phase 6 — Images and performance (P1)

- [ ] Inventory original product, bottle, delivery and production images. Preserve genuine assets and identify missing files.
- [ ] Do not replace genuine brand/product imagery with unrelated stock photos or AI images that imply nonexistent equipment, labs or certifications.
- [ ] Convert suitable images to WebP/AVIF while retaining originals and checking visual quality.
- [ ] Provide appropriate responsive image sizes and explicit width/height or aspect ratio.
- [ ] Add meaningful localized alt text in RU and UK.
- [ ] Lazy-load below-the-fold images, but do not lazy-load the actual hero/LCP image.
- [ ] Optimize font loading, CSS/JS payloads, caching and compression.
- [ ] Measure PageSpeed Insights/Lighthouse for homepage, prices, technology and a long article on mobile and desktop.
- [ ] Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1. These are targets, not claims until measured.

## 8. Phase 7 — Technical SEO, localization and structured data (P0/P1)

- [ ] Preserve all current production article URLs and slugs.
- [ ] Ensure canonicals point to https://crystalwater.kiev.ua/ and never to GitHub Pages.
- [ ] Correctly map Ukrainian language tags (normally uk, not ua) after inspecting the current implementation; use reciprocal RU/UK hreflang pairs for equivalent pages.
- [ ] Add x-default only where a genuine language-selection/default page exists and is appropriate.
- [ ] Ensure each indexable page has a unique title, description, one H1, correct lang, canonical and Open Graph metadata.
- [ ] Fix the sitemap generator so URLs always contain the correct slash after the domain. Validate every loc value; no malformed URLs, duplicates, redirects, 404s, noindex pages or non-canonical URLs.
- [ ] Keep sitemap entries aligned with actual indexable pages and update lastmod only when content genuinely changes.
- [ ] Check robots.txt for accidental blocking of important pages/assets and ensure sitemap location is correct for the actual host.
- [ ] Keep staging URLs out of production canonicals, sitemap, JSON-LD and social metadata.
- [ ] Fix GitHub Pages project-base links so staging navigation works under /crystal-water-site-backup/, while production links resolve to the real domain.
- [ ] Verify trailing-slash and host policy, HTTP/HTTPS redirects, redirect chains, 404 and soft-404 behavior.
- [ ] Validate breadcrumbs and BreadcrumbList markup on relevant pages.
- [ ] Use Organization/LocalBusiness, Product, Service, Article, BreadcrumbList and FAQPage only when the type is appropriate and all properties are supported by visible content.
- [ ] Keep structured data synchronized with visible prices, deposit, product, FAQs and contact details. Never use fake ratings, offers or reviews.
- [ ] Add /llms.txt or /llms-full.txt only if they can be maintained accurately and do not expose private data.
- [ ] Run Schema.org Validator and Google Rich Results Test on representative live URLs after any approved production deployment.
- [ ] Submit the correct production sitemap in Google Search Console and Bing Webmaster Tools after deployment approval.

## 9. Phase 8 — Static hosting and migration readiness (P0)

- [ ] Keep the current static HTML/no-CMS architecture.
- [ ] Confirm the final hosting platform and document root before changing paths, redirects or server configuration.
- [ ] Verify all assets and links from the actual deployment root, including GitHub Pages staging base path and cPanel/static production path if selected.
- [ ] Check case-sensitive filenames, encoded URLs, MIME types, CSS/JS/font/image paths and relative links.
- [ ] Ensure custom 404 pages return an actual HTTP 404 status, not just a 200 HTML page.
- [ ] Confirm HTTPS, compression, caching, security headers and directory-listing behavior for the chosen host.
- [ ] Prepare a complete deployment manifest and rollback plan.
- [ ] Before migration, create and verify a full backup of the live MODX files and database. Keep it private and test restoration where possible.
- [ ] Compare every production URL and asset against the static replacement. Preserve redirects for any unavoidable URL changes, but do not change legacy article URLs.
- [ ] Obtain explicit owner approval before replacing MODX, changing DNS or publishing the static version to the production document root.
- [ ] Do not treat a GitHub Pages preview as production verification.

## 10. Phase 9 — Privacy, security and forms (P0/P1)

- [ ] Check the public repository and generated output for secrets, tokens, customer data, private bot data, database exports and operational backups.
- [ ] Keep customer/order information out of all static files, analytics payloads, logs and public TODOs.
- [ ] Inspect contact/order forms and their destinations. Do not send a real enquiry during testing without authorization.
- [ ] Avoid unnecessary third-party scripts and unsafe embeds.
- [ ] Add security headers appropriate to the actual static host without breaking required resources.
- [ ] Ensure privacy information accurately describes any real data collection and third-party services.

## 11. Phase 10 — Final QA and evidence

- [ ] Validate HTML and crawl every expected staging page.
- [ ] Verify every expected internal link and image; identify orphan pages and broken assets.
- [ ] Audit sitemap URLs, HTTP status, final URL, canonical, hreflang, title, description, H1, language and robots directives.
- [ ] Validate JSON-LD syntax and consistency with visible page content.
- [ ] Test mobile static navigation, RU/UK switcher, phone/order links, footer, tables and long article layouts.
- [ ] Test representative pages in both languages: homepage, prices, technology, delivery/contact and long-form articles.
- [ ] Run performance and accessibility checks and record device/browser/date.
- [ ] Record commands, URLs, date, commit SHA and concise outputs.
- [ ] Mark every task PASS / FAIL / BLOCKED / NOT TESTED. Never mark a real-device or production test complete if it was not performed.
- [ ] Deliver a handoff report with changed files, unresolved content/evidence questions, migration blockers, deployment steps and rollback instructions.

## 12. Execution order

1. P0 — Secure baseline: inspect repository/live site, inspect git state, backup, review security exposure and map actual pages/assets.
2. P0 — Protect content and URLs: preserve article slugs, hub structure, production MODX and all useful original content.
3. P0 — Verify business facts: current 150 UAH bottle price + 350 UAH refundable deposit, delivery terms, technical process and laboratory claims.
4. P0 — Editorial compliance: review and rewrite health-related content; fully address the two specifically flagged articles.
5. P0 — Core pages: homepage, prices, delivery, technology, contact and article hub.
6. P0 — Visual/mobile implementation: compact blue header, fully visible static mobile navigation, correct language switcher and footer.
7. P0 — RU/UK completeness: equivalent pages, correct hreflang/language tags and natural localized content.
8. P0 — Technical SEO: canonical, sitemap, robots, schema, redirects, 404 and staging/production URL separation.
9. P1 — Images, performance, accessibility and conversion refinement.
10. P0 — Full staging QA and evidence report.
11. P0 — Owner approval, verified backup, migration and production deployment only when explicitly authorized.
12. P0 — Post-deployment crawl, Search Console/Bing submission and monitoring.

**Definition of done:** the static site is accurate, medically responsible, visually polished, fast, accessible and complete in RU/UK; preserves the agreed URLs and static/mobile-navigation decisions; shows the correct 150 UAH + 350 UAH refundable-deposit pricing; and has passed documented staging and (only after approval) production verification.
