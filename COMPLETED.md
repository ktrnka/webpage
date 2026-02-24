# Completed work — keith-trnka.com

History of completed tasks, moved here from TODO.md to keep the active list focused.

## Site & pages

- [x] Profile image, color palette, visual layout (two-column index, single-column pages)
- [x] Import pages: Photos, Hiking tips, Urban detrashing tips, Publications
- [x] Publication PDFs linked from `assets/pdf/`
- [x] External link styling (↗), underline hover, page titles
- [x] Blog section created with index page
- [x] CSS to center images in blog posts

## WordPress migration

- [x] Extracted 75 posts from WP XML export via custom Python script (`python/extract_wordpress.py`)
- [x] Batch cleanup: WP shortcodes (`[youtube=...]`, `[caption ...]`), smart quotes, image URLs, dead links
- [x] Per-file review pass across all 98 posts (typos, dead links, code block fixes)
- [x] Fixed broken images: converted 24 posts to use `{{ "..." | relative_url }}` Liquid filter
- [x] Fixed missing paragraph breaks: inserted blank lines across all 75 WP-era posts
- [x] Downloaded 127 WP images to `assets/img/posts/wp/`
- [x] Removed all `[caption` shortcodes, WP tag/category links
- [x] Repaired all broken WP tables and bad code blocks
- [x] Labeled language tags on all code blocks
- [x] Fixed blog index auto-snippets

## Medium migration

- [x] Converted Medium posts to Jekyll Markdown
- [x] Fixed Future Crap Part 1 dropped images
- [x] Re-downloaded rate-limited mt-chat-3 images (.webp)
- [x] Fixed MT chat part 3 conversion
- [x] Removed smart quotes from converted posts

## Deployment & infrastructure

- [x] Homepage meta description restored (Lighthouse SEO fix)
- [x] Fix relative links on GitHub Pages (baseurl issue, commit 003a0513)
- [x] Restore local `bundle exec jekyll serve` testing
- [x] Test GitHub Pages build end-to-end (GitHub Actions)
- [x] Verify all 33 PDF links work
- [x] Add `jekyll-sitemap` plugin
- [x] Wire up DNS
- [x] Redirects from Medium
- [x] Redirects from Google Sites
- [x] `jekyll-redirect-from` redirects for renamed pages (/other/hiking-tips → /guides/hiking, etc.)

## Content

- [x] Make a folder for guides, move hiking and detrashing tips there
- [x] Bring the Kodable tips over
- [x] Consider updating or removing "Why have a webpage?" section
- [x] Seattle outdoor volunteering calendar: link from site
- [x] Replace all Amazon book links with Goodreads
- [x] Write a post about moving from Medium → self-hosted Jekyll

## Blog features

- [x] High-res WP images: `max-width: 100%` CSS in place
- [x] Previous/next post links on blog posts (Jekyll `page.previous`/`page.next`)

## Blog post cleanup

- [x] `over9000.bitballoon.com` / `over9000.me` hijacked links — removed/replaced across 5 posts
- [x] Full link review pass across all posts

## Layout refactor

Single source of truth for `<head>`/chrome, shared nav, clean layout vs content separation.

Layout hierarchy:
- `base.html` — shared `<head>`, SEO, stylesheet, top nav (Home | Blog | Publications)
- `default.html` (extends `base`) — single-column wrapper for pages & blog index
  - `post.html` (extends `default`) — adds post header + date
- `home.html` (extends `base`) — two-column grid with sidebar (profile, full nav, social links)

Steps completed:
- [x] Create `base.html` with shared `<head>`, top nav bar
- [x] Refactor `default.html` to extend `base`
- [x] Create `home.html` extending `base` with two-column grid + sidebar
- [x] Convert `index.md` to use `layout: home`
- [x] Move homepage inline styles to `_sass/minimal-custom.scss`
- [x] Delete `special.html`
- [x] Verify `post.html` still works (extends `default` → `base`)
- [x] Fix page title duplication in `_config.yml`

## Performance

- [x] Add `fetchpriority="high"` to profile image (Lighthouse LCP, ~450ms savings)
- [x] Resize profile image: 600×600 (105KB) → 200×200 (15KB, 86% reduction) from raw source at quality 85
- [x] Animated GIFs → WebM (~9.4MB → ~304KB, 97% reduction) with `<video>` fallback
- [x] Future Crap Part 1 PNGs → JPEG (~15MB → ~2MB, 87% reduction)
- [x] WP PC-cleaning JPGs recompressed (~10MB → ~3.8MB, 63% reduction)

## Tech debt & accessibility

- [x] Add `<main>` landmark to `base.html` + `aria-label` on `<nav>`
- [x] Darken nav link color: `#7f7f7f` → `#595959` (4.0:1 → 6.4:1 contrast, WCAG AA)
- [x] Code block syntax highlighting (fixed `style.scss` imports)
- [x] Check for redirected links
- [x] Image file size review and optimization
- [x] Resize profile image to display dimensions

---

DONE 1. **Double border below nav bar** on non-home pages (visual glitch)
DONE-ish 2. **Horizontal alignment mismatch** between sidebar and content columns on the home page