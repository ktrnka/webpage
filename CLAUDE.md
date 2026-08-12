# CLAUDE.md — keith-trnka.com

Context for AI-assisted development on this repo.

## Project Overview

Personal blog and portfolio site (Keith Trnka). Jekyll static site hosted on GitHub Pages.
Design philosophy: fast, no JS frameworks, no custom fonts, no analytics, boring tech.

## Quick Start

```bash
cd webpage
bundle install
bundle exec jekyll serve --livereload   # http://localhost:4000
```

`bundle exec` is required — bare `jekyll` won't find the right gem version.

## Key Architecture

| What | Where |
|------|-------|
| Site config | `webpage/_config.yml` |
| Layout templates | `webpage/_layouts/` — `base.html` → `default.html` / `post.html` |
| Custom styles | `webpage/_sass/minimal-custom.scss` (CSS variables, dark mode, colors) |
| Stylesheet entry | `webpage/assets/css/style.scss` |
| Blog posts | `webpage/_posts/YYYY-MM-DD-slug.md` → URL `/blog/YYYY/MM/slug/` |
| Images | `webpage/assets/img/posts/` |
| PDFs | `webpage/assets/pdf/` |

## Common Workflows

### New blog post

Create `webpage/_posts/YYYY-MM-DD-slug.md` with:

```yaml
---
layout: post
title: Post Title Here
date: YYYY-MM-DD
---
```

### Adding images

Download to `webpage/assets/img/posts/`, reference with Jekyll's `relative_url` filter:

```markdown
![Alt text]({{ "/assets/img/posts/name.png" | relative_url }})
```

Internal links must also use `relative_url` — bare paths break in local dev vs production.

### Deployment

Push to `main`. GitHub Actions (`.github/workflows/jekyll.yml`) builds and deploys to GitHub Pages automatically. No manual steps.

## Design Constraints

These are intentional — don't work around them without a strong reason:

- **No JS frameworks or libraries** — site is JS-free except the theme's `scale.fix.js`
- **No custom web fonts** — system fonts only (`-apple-system`, `BlinkMacSystemFont`, etc.)
- **No analytics or tracking scripts**
- **No heavy third-party embeds** — inline content instead (see gist policy in `LESSONS_LEARNED.md`)
- Prefer CSS-only solutions; if JS is needed, document why

## Known Non-Issues

- **Sass `@import` deprecation warning** during `jekyll serve` — blocked on upstream `jekyll-theme-minimal` migrating to `@use`/`@forward`. Warning is local-only; production builds are unaffected. Safe to ignore.
- `vendor/` contains bundled theme gems — don't edit or delete

## Gotchas

- **Medium CDN rate-limits parallel downloads** — always `curl` images one at a time. See `LESSONS_LEARNED.md` for detection and recovery steps.
- **Intermediate files** — use `tmp/` at repo root (gitignored), not `/tmp/`
- **Favicon is two files, deliberately.** `assets/img/favicon.svg` is the only one linked from `base.html`; it adapts to light/dark via `prefers-color-scheme` inside the SVG. `webpage/favicon.ico` sits unlinked at the site root, where browsers that can't use an SVG icon fall back to it on their own. Don't "fix" the absent `<link>` tag for the `.ico` – adding one back can make Chrome prefer the static `.ico` over the theme-aware SVG.

## Active Priorities

See `TODO.md` for the full backlog. Current top priority:
- **Link discoverability** — inline links have no persistent underline; color is close to heading accent (`#970c4f`). Readers may not recognize them as clickable.

## Link checking

Two lychee configs in `link_testing/`:

```bash
# Fast local-only check (no network) — catches missing images and broken internal links
cd webpage && bundle exec jekyll build && cd ..
lychee --config link_testing/lychee-config-local-only.toml --root-dir webpage/_site "webpage/_site/**/*.html"

# Full external check — catches dead external links (results cached 2 days)
cd webpage && bundle exec jekyll build && cd ..
lychee --config link_testing/lychee-config.toml --root-dir webpage/_site --output link_testing/lychee-report.md "webpage/_site/**/*.html"
```

Most 403 errors are bot-blocking false positives (dl.acm.org, medium.com, etc.). See `LESSONS_LEARNED.md` for triage guidance and dead-link fix patterns.

## Migration Reference

For converting Medium or WordPress posts to Jekyll Markdown, see `LESSONS_LEARNED.md`. It covers pandoc format selection, post-conversion cleanup checklist, image handling, and gist embeds.
