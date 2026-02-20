# TODO — keith-trnka.com

98 blog posts live (75 WP-era, 23 post-WP). Site, pages, and blog all on `main`.

## Blog post cleanup 🔧
Remaining `<!-- KT TODO -->` markers in posts:
- [ ] `2016-05-19-summary-predicting-winloss-for-league-of-legends.md` — unfinished draft with placeholder text; decide: complete, heavily trim, or remove

Other post quality issues:
- [ ] Fix poor auto-snippets on blog index (headings/images leaking into excerpt):
  - `bigger-league-of-legends-data-set`, `future-crap-part-1`, `future-crap-part-2`, `scikit-learn-0-17-is-out`, `predicting-league-match-outcomes-gathering-data`
- [X] MT chat part 3 didn't convert correctly from Medium — needs manual redo
- [X] Review code blocks in all converted posts — ensure correct language tags for syntax highlighting
- [X] Remove smart quotes from all converted blog posts (script to automate)

## Deployment & infrastructure 🚀
- [ ] Fix relative links on GitHub Pages (internal links break due to baseurl; need to replicate recipes repo deployment approach — see commit 003a0513)
- [X] Restore local `bundle exec jekyll serve` testing (removed in that same commit)
- [ ] Test GitHub Pages build end-to-end (verify GitHub Actions succeeds)
- [ ] Verify all 33 PDF links work
- [ ] Manual testing: desktop, tablet, mobile across browsers

## Blog features & enhancements 📋
- [ ] Series/project navigation: readers landing on one post in a series should find the others (LoL/ML, Searchify/synonyms, MTurk, Over 9000). **Research note:** Jekyll `categories:` build into the URL, `tags:` don't — otherwise very similar. Start with small controlled tests before committing to a scheme.
- [ ] Improve blog index snippets where Medium subtitle/heading got duplicated (e.g., Future Crap posts)
- [ ] Add paper/reference links to academic blog posts (MT series, etc.) — cite DOIs or Google Scholar
- [Might be done?] High-res WP images: at minimum add `max-width: 100%` CSS so they don't break layout. Optional: batch resize with ImageMagick.
- [ ] Research email notification / RSS-to-email for blog updates
- [ ] Write a post about moving from Medium → self-hosted Jekyll

## Content 📝
- [ ] Make a folder for guides, move hiking and detrashing tips there
- [ ] Bring the Kodable tips over
- [ ] Consider updating or removing "Why have a webpage?" section
- [ ] Seattle outdoor volunteering calendar: link from site

## Tech debt 🔩
- [ ] Reduce code duplication between index layout and default page layouts
- [ ] Fix Sass `@import` deprecation warning (migrate to `@use`/`@forward` before Dart Sass 3.0.0)
- [ ] Fix mobile homepage layout (sidebar/header alignment above main content)
- [ ] Link checking CI: HTMLProofer for internal links (`--disable-external`); Lychee on a cron schedule for external links
- [ ] Check for redirected links (faster for users if links are direct)

## Someday / low priority 💤
- [ ] Look into Medium post claps/views/stats — optimize top performers
- [ ] Set up private repo for blog drafts/candidates (git submodule approach)
- [ ] Consider merging recipes repo into this one
- [ ] Create `.github/copilot-instructions.md` with project-specific guidance

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

</details>

<details>
<summary>Medium migration (done)</summary>

- [x] Converted Medium posts to Jekyll Markdown
- [x] Fixed Future Crap Part 1 dropped images
- [x] Re-downloaded rate-limited mt-chat-3 images (.webp)

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
