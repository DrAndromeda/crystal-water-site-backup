# Crystal Water — Claude Code TODO (2026-11-12)

Project: Crystal Water, water delivery in Brovary and Kyiv  
Production: https://crystalwater.kiev.ua/ (legacy live MODX site; preserve as source of truth until migration is explicitly approved)  
Staging: https://drandromeda.github.io/crystal-water-site-backup/  
Repository: https://github.com/DrAndromeda/crystal-water-site-backup



## 0. Obsidian handoff and repository map — added 2026-11-12

The owner supplied two Obsidian notes. Treat them as project context, not as proof that tasks were deployed.

### Repository and workspace roles

- **Production domain / historical ORIGINAL:** https://crystalwater.kiev.ua/
- **Prototype / static redesign:** https://drandromeda.github.io/crystal-water-site-backup/
- **Prototype repository:** https://github.com/DrAndromeda/crystal-water-site-backup (default branch: `main`; this is the repository containing this TODO).
- **Additional historical/live-site repository recorded in Obsidian:** https://github.com/DrAndromeda/crystalwater.kiev.ua (default branch: `master`). GitHub metadata confirms this repository exists and is public. Its root contains MODX/PHP-era material and operational-looking files; its README currently describes the Seo4Evo MODX package, not a clear static-site handoff. Do not assume this repository is the prototype or the authoritative current source tree. Inspect its tree and commit history carefully before using it.
- **Historical local workspace path recorded in Obsidian:** `~/.openclaw/workspace/crystal-water-site/`. Verify that this path still exists on the owner's machine before assuming it is the current working clone.
- Obsidian previously recorded the project as active, priority P3. Treat that as a note status, not a verified deployment status.
- Historical Obsidian completion claims: 66+ HTML pages, all articles, compact header phone alignment, bottle logo adjustment, and 63/63 article sitemap match. A later note claims 85 pages. These are historical assertions; measure the actual current inventories and report exact counts.

### Security blocker — inspect before cloning or deployment

A GitHub root-directory listing of the public `DrAndromeda/crystalwater.kiev.ua` repository exposed filenames including `.htpasswd`, `.my.cnf`, `kickstart.php`, `php-cgi.core`, and a `manager/` directory. Their contents have not been inspected. This is enough to require a security review; it does **not** prove that credentials are valid or currently usable.

- [ ] Owner/security administrator: determine whether `.htpasswd`, `.my.cnf`, database credentials, hosting credentials, backup installer files, crash/core dumps, or other private operational data were ever committed publicly.
- [ ] If any real credentials or secrets were present in repository history, rotate/revoke them immediately; removing a file from the latest commit alone does not remove historical exposure.
- [ ] Review repository history and remove sensitive material from all reachable history using a carefully planned, owner-approved cleanup; coordinate with anyone who cloned/forked it.
- [ ] Check the public repository for private customer data, database exports, backups, tokens and personal information. Never copy any such data into this prototype repository.
- [ ] Do not fetch, quote, reproduce, or commit the contents of suspected credential/configuration files as part of this TODO.
- [ ] Do not run `kickstart.php`, import a backup, or expose the `manager/` area as part of static-site work.
- [ ] Keep the production MODX backup private and access-controlled. Public visibility of this repository is not proof that the owner intended every operational file to be public.

### Private customer/bot data — never publish

The owner supplied a private Obsidian note describing the legacy `@CrystalWaterBro_bot` customer store. It records that the old bot used a local `clients.json` file at `/Users/Andromeda/bots/crystal-water-bot/clients.json`. The note contained Telegram identifiers and order statistics; those values are intentionally omitted from this public TODO.

- Treat `clients.json`, bot logs, Telegram IDs, order history and customer records as confidential personal/business data.
- Do not commit, upload to public repositories, place in site assets, expose in HTML/JSON-LD, or include raw customer identifiers in Claude prompts or reports.
- If bot maintenance requires the file, work only on an owner-authorized private local copy with least-privilege access and a separate backup. Do not assume the historical path still exists.
- The existence and format of the old file are historical facts from the note; current bot storage and current customer counts must be verified privately before any migration.

## Instructions and safety rules

- Work in a local clone/working branch. First inspect `git status`, current branch, latest commit and all existing changes. Do not overwrite uncommitted user work.
- Create a timestamped backup/rollback point before editing.
- Do not deploy, replace production files, change DNS, or disable the existing MODX site without explicit owner approval and a verified backup.
- The live MODX site is the reference for existing content and URLs. Do not assume the GitHub Pages version is production.
- Preserve all existing article URLs/slugs. The user selected **Option A** in `blog-structure-decision.md`: keep flat legacy article URLs and organize them through the existing `/voda-h2o-stati/` hub. Do NOT migrate to `/blog/...` unless the owner explicitly reverses this decision.
- Mobile navigation must be **static and fully visible**, with no hamburger menu, no collapsed/hidden menu. This explicit user decision overrides older generic instructions.
- Do not invent water-treatment stages, laboratory results, TDS/pH values, certificates, awards, customer reviews, delivery promises, prices or medical benefits. Verify claims against primary evidence and the actual production site.
- Keep the site static HTML (no CMS/database) unless the owner explicitly changes the architecture decision.
- Treat older TODOs, checklists and scripts as proposed work, not proof that changes were applied. Verify actual site files and staging/live behavior.

## 1. Establish the real baseline

- [ ] Record commit SHA, branch, clean/dirty status and file inventory.
- [ ] Compare repository pages against the live MODX site and available Web Archive snapshots. Identify missing pages, assets, images, CSS, JS, fonts and content. Do not use a destructive mirror command against production.
- [ ] Inventory all RU and UA URLs; record status codes, redirects, titles, descriptions, H1s, canonicals, hreflang, breadcrumbs and internal links.
- [ ] Confirm actual page count; earlier documents mention 71+ HTML pages, 63 articles and a target of 85+ pages. Report measured counts rather than repeating old numbers.
- [ ] Review existing helper scripts before running them: `fix_site_issues.py`, `add_hreflang.py`, `generate_sitemap_ua.py`, `generate_article_jsonld.py`, `unify_social_links.py`. Understand their exact changes and backup behavior first.
- [ ] Inspect existing `IMPROVEMENTS.md`, `INSTRUCTIONS_FOR_NEXT_ASSISTANT.md`, `TZ-1-full-spec.txt`, `proposal.md`, `medical-claims-rewrite.md`, `blog-structure-decision.md`, and `images-mobile-performance-checklist.md`. This TODO consolidates their requirements; it does not supersede explicit user decisions recorded there.

## 2. Preserve URLs and repair technical SEO

- [ ] Preserve every currently indexed production URL and slug, including legacy article filenames.
- [ ] Fix the sitemap generator so it cannot concatenate the domain and filename without a slash. Validate all sitemap loc values; no malformed URLs, duplicates or missing pages.
- [ ] Add/verify RU/UK hreflang pairs on every corresponding page, with correct reciprocal URLs and x-default only where appropriate. Confirm language code convention with current site implementation; do not mix `ua` and `uk` incorrectly.
- [ ] Ensure canonical URLs point to the intended production domain `https://crystalwater.kiev.ua/`, never GitHub Pages.
- [ ] Verify Open Graph/Twitter metadata. All `og:image` values must be absolute production URLs and resolve successfully.
- [ ] Fix staging-only root links so logo/home navigation works under the GitHub Pages project base path, while production links resolve correctly.
- [ ] Check breadcrumbs and correct BreadcrumbList structured data on all relevant pages.
- [ ] Check robots.txt, sitemap.xml and AI crawler policy. Ensure robots rules do not accidentally block important pages/assets. Decide static-host behavior only after the deployment platform is confirmed.
- [ ] Add/verify `llms.txt` and `llms-full.txt` only if accurate and maintained.
- [ ] Check HTTP/HTTPS, www/non-www, trailing slash policy, redirect chains, 404/soft-404 and mixed content.
- [ ] Validate JSON-LD against visible page content. Use LocalBusiness/Organization, Product/Service, Article, BreadcrumbList and FAQPage only where the type is appropriate and supported by visible content. Do not fabricate ratings, offers, prices or business facts.

## 3. Medical and health-claim compliance — high priority

- [ ] Search all RU and UA HTML, metadata, structured data and article content for claims such as “лечит”, “стимулирует иммунитет”, “восстанавливает на клеточном уровне”, “навсегда устраняет проблемы со здоровьем”, weight-loss promises, or “идеальный кислотно-щелочной баланс”.
- [ ] Apply the approved neutral rewrites in `medical-claims-rewrite.md` where they remain factually accurate.
- [ ] Fully rewrite `xolodnaya-voda-i-vliyanie-na-organizm.html` and `butilirovannaya-voda-nuzhna-dlya-poxudeniya.html` OR temporarily remove them from navigation/indexing until rewritten. These two articles were explicitly identified as requiring full review, not minor phrase edits.
- [ ] If discussing research, cite real, relevant sources and accurately distinguish evidence from general information. Do not imply that the product treats, prevents or cures disease.
- [ ] Verify pH ~7.5 and any mineral/TDS claims against current lab reports before publishing. Remove unsupported numerical claims.
- [ ] Add an appropriate informational disclaimer where health-related educational content remains. A disclaimer does not make a false claim acceptable.

## 4. Product, pricing, technology and conversion accuracy

- [ ] Make the product, price and ordering method clear near the top of the home page and relevant service pages.
- [ ] Verify all current prices, deposits, minimum order quantities, free-first-bottle offers, delivery zones, schedules, payment terms and business tariffs directly with the owner/current business source before publishing. Existing old figures are not automatically current.
- [ ] Audit the “8 stages of purification” against the actual documented production process and current `tekhnologii-ochistki.html`. The previous handoff explicitly warns that stages 05–07 were assumptions. Do not invent them; use only verified process stages.
- [ ] Verify claims about reverse osmosis, carbon filtration, ozonation, UV treatment, mineralization, bottling and quality control against technical documentation.
- [ ] Ensure price tables and order CTAs are consistent across home, prices, service and contact pages.
- [ ] Ensure phone numbers, Telegram/social links, address, opening hours and service area are consistent. Check current live footer as a reference, but confirm accounts with owner before applying `unify_social_links.py`.
- [ ] Fix known typo on `prices.html`: “за бутыля” → “за бутыль”, if still present.
- [ ] Inspect `prices.html` for raw Markdown artifacts such as `****`, stray `*` or `**`; replace with valid HTML formatting.
- [ ] Keep phone visible and make call/order actions easy to use on mobile. If a fixed mobile order bar is present, ensure it does not cover page content.

## 5. Header, footer and responsive design

- [ ] Preserve the recognizable Crystal Water blue brand identity. Existing palette reference: `#0f5f96`, `#1e88c7`, `#00c2e6`, light blue background `#eaf6fc`, white and dark readable text.
- [ ] Header is blue, sticky, compact and usable. Desktop may show horizontal navigation; mobile must show all menu items statically, with wrapping as needed. No hamburger/collapsed menu.
- [ ] Mobile footer must be readable, stack naturally, and include verified contact details, location, Telegram, navigation and copyright.
- [ ] Verify logo and “Доставка воды” links on staging and production.
- [ ] Verify RU/UA switcher on every page: it must lead to the equivalent language page, not always to the language homepage.
- [ ] Verify responsive behavior at 360, 375, 390, 430, 768, 1280 and 1920px. Check actual iPhone/Android rendering where possible.
- [ ] No horizontal overflow, clipped text, overlapping buttons, tiny tap targets or broken tables.
- [ ] If using a sticky mobile order bar, add sufficient bottom spacing and verify it does not obscure content or browser UI.
- [ ] Test all interactive controls and links; prefer graceful behavior without JavaScript where feasible.

## 6. Images and performance

- [ ] Inventory actual image files and identify missing assets; do not replace genuine product/brand photos with unrelated stock imagery.
- [ ] Convert suitable images to WebP/AVIF while retaining source originals and verifying visual quality.
- [ ] Add meaningful RU/UA alt text; include explicit width/height to reduce layout shift.
- [ ] Use lazy loading below the fold; do not lazy-load the LCP/hero image.
- [ ] Serve responsive image dimensions appropriate to rendered size.
- [ ] Check font loading, CSS/JS payloads, caching and compression.
- [ ] Run PageSpeed Insights/Lighthouse on home, prices, technology and a heavy article, mobile and desktop.
- [ ] Targets: LCP < 2.5s, INP < 200ms, CLS < 0.1; Lighthouse targets from the old spec are goals, not claims until measured.

## 7. Content architecture and editorial quality

- [ ] Keep the existing article URL structure. Use `/voda-h2o-stati/` as the logical article hub.
- [ ] Do not generate thin doorway pages or bulk keyword-swapped pages.
- [ ] Preserve original useful content and add unique value, accurate facts, clear structure and contextual internal links.
- [ ] Every indexable page should have a unique title, meta description, one clear H1 and logical H2/H3 hierarchy.
- [ ] Add concise direct answers and useful FAQs where they genuinely answer user questions. Do not add FAQ schema merely to decorate a page.
- [ ] Review RU and UA copy for native quality, consistency and terminology; no literal machine translation.

## 8. Security, forms and deployment readiness

- [ ] Review forms and contact destinations; test only with an authorized test enquiry.
- [ ] Check for exposed credentials, tokens, private data, unsafe third-party scripts and mixed-content resources.
- [ ] Add/verify appropriate security headers for the actual host; do not blindly copy headers that break required embeds or assets.
- [ ] Confirm static hosting compatibility, MIME types, fallback behavior and redirects. No CMS/database is required by the current project brief.
- [ ] Before any production migration: create and verify a full backup of the current MODX site and database, document rollback, compare all URLs/assets, and obtain explicit owner approval.
- [ ] Do not replace the live MODX site or alter DNS as part of this TODO without that approval.

## 9. Final QA and evidence

- [ ] Run HTML validation, link crawl, route/URL checks, sitemap validation, hreflang/canonical audit, JSON-LD validation, image audit and responsive checks.
- [ ] Test representative RU and UA pages plus all core conversion pages.
- [ ] Confirm all internal links resolve and all expected pages return 200 on staging.
- [ ] Record exact commands, date, commit SHA, URLs and output summaries.
- [ ] Mark each task as PASS / FAIL / NOT TESTED with evidence. Never mark a browser/device test as passed unless it was actually performed.
- [ ] Produce a concise report of blockers, residual risks and recommended next steps.

## Known decisions and unresolved items

**Decisions already made**
- Keep existing article URLs; use the existing article hub. No silent migration to `/blog/`.
- Mobile navigation is static and fully visible; no hamburger.
- Static HTML / no CMS / no database is the current project requirement.
- Preserve the live MODX site until migration is explicitly approved.

**Must be verified, not assumed**
- Whether all proposed changes in the handoff folder were actually applied to the site HTML/CSS.
- Final current prices, deposit, offers, delivery terms and phone/social account details.
- Exact technical sequence of all eight purification stages.
- Current verified laboratory data (pH, TDS, mineral composition and certificates).
- Whether robots.txt and final deployment architecture are correct for the chosen host.
- Visual appearance of mobile header/footer on real devices.
- Availability and quality of original image assets.

## Source documents in this repository

- `IMPROVEMENTS.md`
- `INSTRUCTIONS_FOR_NEXT_ASSISTANT.md`
- `TZ-1-full-spec.txt`
- `proposal.md`
- `medical-claims-rewrite.md`
- `blog-structure-decision.md`
- `images-mobile-performance-checklist.md`
- `HANDOVER.md`

Treat these documents as historical project requirements and handoff context. If they conflict, follow the explicit user decisions documented above and report unresolved contradictions rather than guessing.
