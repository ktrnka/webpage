# TODO — keith-trnka.com

98 blog posts live (75 WP-era, 23 post-WP). Completed work tracked in [COMPLETED.md](COMPLETED.md).

## Goals

Build the kind of web I want: fast loading, no ads, no trackers, works across platforms, accessible.

## Principles

- **Automate only when it saves time soon.** For recurring-but-infrequent tasks, use a command reference (skills.md or similar) rather than writing a full script.
- **Use proven, reliable, boring technology.** Jekyll, static HTML/CSS, system fonts, GitHub Pages.
- **Stay focused on reader experience.** Every change should connect back to making the site faster, clearer, or easier to use for visitors.

## Priorities

Items actively planned, with clear user or quality impact.

### Fix mobile homepage layout
The homepage layout has two issues on mobile viewports:
DONE 1. **Double border below nav bar** on non-home pages (visual glitch)
2. **Horizontal alignment mismatch** between sidebar and content columns on the home page

These are the most visible remaining quality issues for mobile visitors. Fix in `_sass/minimal-custom.scss` (media queries) and possibly `_layouts/home.html`.

### Improve link discoverability
Inline links have no persistent underline and use a color (`--link: #970c4f`) close to the heading accent. Readers may not recognize them as clickable, especially on content-heavy blog posts. Consider adding a subtle persistent underline or shifting the link color further from the heading color.

### Unfinished LoL draft
`2016-05-19-summary-predicting-winloss-for-league-of-legends.md` has `<!-- KT TODO -->` placeholder text. This is old and probably not worth finishing. Decide: heavily trim to what's there, or just remove it.

## Backlog

Lower priority or needs more thought before starting.

- [ ] **Series/project navigation** — readers landing on one post in a multi-part series (LoL/ML, Searchify/synonyms, MTurk, Over 9000) have no way to find the others. Jekyll `tags:` don't affect URL structure, so they're a lighter-weight starting point than `categories:`. Ref: https://www.ayush.nz/2022/02/creating-article-series-posts-navigation-jekyll
- [ ] **Paper/reference links on academic posts** — cite DOIs or Google Scholar for the MT series and similar posts, so readers can find the original research
- [ ] **Inline gists into post content** — gist embeds add external JS requests and can break if GitHub changes the embed API. Two posts have gists that could be inlined:
  - `2015-11-04-better-predictions-for-league-matches.md` (scikit-learn Keras wrapper)
  - `2015-12-03-ensembles-part-2.md` (StackedEnsembleClassifier)
- [ ] **Link checking CI** — HTMLProofer for internal links (`--disable-external`); Lychee on a cron for externals. After DNS setup, Lychee works with `--offline` pointed at `_site/` with `--root-dir`
- [ ] **Simplify layout templates** — the layout refactor unified `<head>` and nav but total line count increased. Could the sidebar nav be data-driven (`_data/nav.yml`)? Could post-nav styles move fully to SCSS?
- [ ] **RSS/email notifications for blog updates** — most services feel scummy; low subscriber count (1) makes this very low priority
- [ ] **Fix Sass `@import` deprecation** — blocked until theme itself migrates to `@use`/`@forward`. Only fix is vendoring all 4 theme SCSS files. Warning is local-only; not urgent until Dart Sass 3.0.0
- [ ] **Archive page** — blog posts grouped by year for easier browsing across 15 years of content
- [ ] **AI attribution** — figure out how to credit AI assistance on posts where it's heavily used (guest author model, footer note, etc.)
- [ ] **Writing guidelines** — codify personal blogging conventions (I vs we, hedging over false claims, number formatting, image optimization) and aspirational goals (intro hooks, title optimization)
- [ ] **`.github/copilot-instructions.md`** — project-specific guidance for AI coding assistants
- [ ] Medium post claps/views/stats — identify top performers
- [ ] Private repo for blog drafts (git submodule approach)
- [ ] Consider merging recipes repo into this one
- [ ] Add favicon.ico, preferably something tiny in SVG. Ironically this will improve page load over a 404
- [ ] Strip old image metadata

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
- Local dev: `cd webpage && bundle exec jekyll serve --livereload`

</details>
