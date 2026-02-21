# TODO — keith-trnka.com

98 blog posts live (75 WP-era, 23 post-WP). Site, pages, and blog all on `main`.

## Blog post cleanup 🔧
Remaining `<!-- KT TODO -->` markers in posts:
- [ ] `2016-05-19-summary-predicting-winloss-for-league-of-legends.md` — unfinished draft with placeholder text; decide: complete, heavily trim, or remove

Dead/hijacked links:
- [X] **`over9000.bitballoon.com` and `over9000.me` now link to someone else's project** — appears in 5 posts. Probably just remove the links or link to the GitHub repo instead.
- [X] Finish reviewing / editing all links. I stopped at 2015-09-21-bigger-league-of-legends-data-set.md

## Deployment & infrastructure 🚀
- [X] Fix relative links on GitHub Pages (internal links break due to baseurl; need to replicate recipes repo deployment approach — see commit 003a0513)
- [X] Restore local `bundle exec jekyll serve` testing (removed in that same commit)
- [X] Test GitHub Pages build end-to-end (verify GitHub Actions succeeds)
- [X] Verify all 33 PDF links work
- [X] Add `jekyll-sitemap` plugin (supported by GitHub Pages, just add to `_config.yml` plugins list)
- [ ] Manual testing: desktop, tablet, mobile across browsers
- [ ] Wire up DNS
- [ ] Redirects from Medium
- [ ] Redirects from Google Sites

## Blog features & enhancements 📋
- [ ] Series/project navigation: readers landing on one post in a series should find the others (LoL/ML, Searchify/synonyms, MTurk, Over 9000). **Research note:** Jekyll `categories:` build into the URL, `tags:` don't — otherwise very similar. Start with small controlled tests before committing to a scheme.
- [ ] Add paper/reference links to academic blog posts (MT series, etc.) — cite DOIs or Google Scholar
- [X] High-res WP images: verify `max-width: 100%` CSS is in place so they don't break layout. Optional: batch resize with ImageMagick.
- [X] Previous/next post links on blog posts (Jekyll built-in `page.previous`/`page.next`) — low effort, helps discoverability
- [ ] Research email notification / RSS-to-email for blog updates
- [ ] Write a post about moving from Medium → self-hosted Jekyll

## Content 📝
- [X] Make a folder for guides, move hiking and detrashing tips there
- [X] Bring the Kodable tips over
- [X] Consider updating or removing "Why have a webpage?" section
- [X] Seattle outdoor volunteering calendar: link from site
- [X] Replace all Amazon book links with Goodreads

## Layout refactor 🏗️
Goal: single source of truth for `<head>`/chrome, shared nav on all pages, clean separation of layout vs content.

> **Long-term note:** The refactor reduced duplication in `<head>` and unified the nav, but the total line count across layouts _increased_. A well-executed refactor should decrease code. Worth revisiting — e.g. could the sidebar nav in `home.html` be driven by a `_data/nav.yml` file? Could the post-nav styles move fully to SCSS? Left for a future pass.

New hierarchy:
- `base.html` — shared `<head>`, SEO, stylesheet, lightweight top nav (Home | Blog | Publications), `{{ content }}`
- `default.html` (extends `base`) — single-column wrapper for pages & blog index
  - `post.html` (extends `default`) — adds post header + date
- `home.html` (extends `base`) — two-column grid with sidebar (profile, full nav, social links)

Other changes:
- `index.md` → `index.html` (content is fundamentally HTML, not Markdown)
- Move inline `<style>` from special.html into SCSS
- Delete `special.html` once `home.html` + `index.html` are working

Steps:
- [X] Create `base.html` with shared `<head>`, top nav bar, `{{ content }}`
- [X] Refactor `default.html` to extend `base` (add `layout: base`, keep single-column wrapper)
- [X] Create `home.html` extending `base` with two-column grid + sidebar
- [X] Convert `index.md` to use `layout: home` (kept as Markdown — content works fine without converting to raw HTML)
- [X] Move homepage inline styles to `_sass/minimal-custom.scss`
- [X] Delete `special.html`
- [X] Verify `post.html` still works (extends `default` → `base`)
- [X] The page title on index.md is weird: "Keith Trnka | Personal website of Keith Trnka, PhD" — fix in `_config.yml`

## Tech debt 🔩
- [ ] Fix mobile homepage layout (sidebar/header alignment above main content)
- [X] Code block syntax highlighting: root cause was `assets/css/style.scss` not importing `jekyll-theme-minimal` (which includes `rouge-github.scss`); fixed by adding `@import "jekyll-theme-minimal"` before `@import "minimal-custom"`
- [ ] Link checking CI: HTMLProofer for internal links (`--disable-external`); Lychee on a cron schedule for external links
- [X] Check for redirected links (faster for users if links are direct)

## Usability
- [ ] For blog pages, consider moving gists into the page content itself — posts with gists:
  - `2015-11-04-better-predictions-for-league-matches.md` → [ktrnka/81c8a7b79cb05c577aab](https://gist.github.com/ktrnka/81c8a7b79cb05c577aab) (scikit-learn wrapper for Keras models)
  - `2015-12-03-ensembles-part-2.md` → [ktrnka/919e0931b4534c05c389](https://gist.github.com/ktrnka/919e0931b4534c05c389) (StackedEnsembleClassifier)
  - `2025-12-04-ubuntu-25-setup-for-a-2014-macbook-pro.md` → [johnjeffers/3006011ec7767a4101cdd118e8d64290](https://gist.github.com/johnjeffers/3006011ec7767a4101cdd118e8d64290) (external reference, probably leave as-is)
- [ ] Link discoverability: inline links have no underline by default and use a color close to the heading accent — users may not immediately recognize them as links. Consider a persistent underline or a more distinct link color.
- [X] Review image file sizes to see if we should optimize for load time
- [X] **Animated GIFs** (~9.4MB total → ~304KB WebM, 97% reduction). Command: `ffmpeg -i input.gif -c:v libvpx-vp9 -b:v 0 -crf 33 -an output.webm`. Used `<video autoplay loop muted playsinline>` with GIF as fallback inside `<video>`.
  - [X] `bertviz.gif` (3.9M → 128K)
  - [X] `im-sorry-fail.gif` (2.6M → 64K)
  - [X] `lower-back-fail.gif` (1.7M → 44K)
  - [X] `verarbeiten-demo.gif` (992K → 24K)
  - [X] `alignment-demo.gif` (132K → 24K)
  - [X] `japanese-example.gif` (76K → 20K)
- [X] **Future Crap Part 1 large PNGs** (~15MB total, 13 PNG images → JPEG at 85% quality, ~2MB total, ~87% reduction). `convert -quality 85`. Updated refs in part-1 and part-2 posts.
- [X] **WP PC-cleaning JPGs** (~10MB → ~3.8MB, 63% reduction) — `mogrify -quality 80` in-place recompress on 8 files in `assets/img/posts/wp/`

## Someday / low priority 💤
- [ ] Fix Sass `@import` deprecation warning — blocked: `jekyll-theme-minimal.scss` itself uses `@import "fonts"` and `@import "rouge-github"` internally, so even converting `style.scss` to `@use` doesn't silence it. Only real fix is vendoring all 4 theme SCSS files into `_sass/` and converting them to `@use`/`@forward`. Warning is local-only (GitHub Pages pins old gem versions). Not urgent until Dart Sass 3.0.0 makes it an error.
- [ ] Look into Medium post claps/views/stats — optimize top performers
- [ ] Set up private repo for blog drafts/candidates (git submodule approach)
- [ ] Consider merging recipes repo into this one
- [ ] Archive page: blog posts grouped by year for easier browsing across 15 years of content
- [ ] Create `.github/copilot-instructions.md` with project-specific guidance
- [ ] Something like "guest authors" in which I can list Claude if I'm relying heavily on AI

---

## Completed ✅

<details>
<summary>Site & pages (done)</summary>

- [x] Profile image, color palette, visual layout (two-column index, single-column pages)
- [x] Import pages: Photos, Hiking tips, Urban detrashing tips, Publications
- [x] Publication PDFs linked from `assets/pdf/`
- [x] External link styling (↗), underline hover, page titles
- [x] Blog section created with index page
- [x] CSS to center images in blog posts

</details>

<details>
<summary>WordPress migration (done)</summary>

- [x] Extracted 75 posts from WP XML export via custom Python script (`python/extract_wordpress.py`)
- [x] Batch cleanup: WP shortcodes (`[youtube=...]`, `[caption ...]`), smart quotes, image URLs, dead links
- [x] Per-file review pass across all 98 posts (typos, dead links, code block fixes)
- [x] Fixed broken images: converted 24 posts to use `{{ "..." | relative_url }}` Liquid filter
- [x] Fixed missing paragraph breaks: inserted blank lines across all 75 WP-era posts
- [x] Downloaded 127 WP images to `assets/img/posts/wp/`
- [x] Removed all `[caption` shortcodes, WP tag/category links
- [x] Repaired all broken WP tables and bad code blocks
- [x] Labeled language tags on all code blocks
- [x] Fixed blog index auto-snippets (good enough)

</details>

<details>
<summary>Medium migration (done)</summary>

- [x] Converted Medium posts to Jekyll Markdown
- [x] Fixed Future Crap Part 1 dropped images
- [x] Re-downloaded rate-limited mt-chat-3 images (.webp)
- [x] Fixed MT chat part 3 conversion
- [x] Removed smart quotes from converted posts

</details>

---

## Reference notes

<details>
<summary>Project context</summary>

- Raw HTML snapshots: `download/`
- WP extraction script: `python/extract_wordpress.py`
- Color palette: mauve/maroon accents (#7f1146)
- Jekyll SEO tag: fills `<head>` with title, description, OG tags, JSON-LD — not much to do ([docs](https://jekyll.github.io/jekyll-seo-tag/usage/))
- Image optimization: not worth automating for this few images
- Performance: run Lighthouse after deploy; use `loading="lazy"` for below-fold images; avoid heavy third-party embeds

</details>
