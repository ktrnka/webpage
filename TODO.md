# TODO — import keith-trnka.com

Branch: `import/keith-trnka-com`

## Completed ✅
- [x] Get profile/header image(s) into `webpage/assets/` — added `webpage/assets/img/profile.jpg` (resized with ImageMagick)
- [x] Apply site color palette from screenshot — CSS variables set
- [x] Improve `publications.md` using `download/publications.html` — rebuilt; local PDFs linked from `assets/pdf/`
- [x] Import "Other" pages: `Photos`, `Hiking tips`, `Urban detrashing tips` — converted and moved into site root
- [x] Move imported pages out of `webpage/imported-keith-trnka/` into `webpage/` (overwrote temp `index.md`)
- [x] Publication PDFs: linked from `webpage/assets/pdf/` (user-provided)
- [x] Remove import notes and LLM commentary from all pages
- [x] Hide logo on non-index pages (show only on home)
- [x] Visual improvements:
  - [x] Two-column index layout (left: name+photo+links; right: content)
  - [x] Visually separate internal vs external links (external marked with ↗)
  - [x] One-column centered layout for non-index pages (wider content area)
  - [x] Fix page titles: "Keith Trnka" for home, "Page | Keith Trnka" for others
  - [x] Replace bold-on-hover for links with underline styling
  - [x] Restore missing inline links (Palia, Singularity 6, 98point6, Swype, etc.)
  - [x] Remove "Hosted on GitHub Pages" footer
- [ ] Test GitHub Pages build (verify GitHub Actions succeeds)
- Fix relative links on github pages
- Create a blog section

## Before Merge/Deploy 🚀
- [x] Add missing "Blog before 2017" link (https://kwtrnka.wordpress.com/)
- [ ] Verify all 33 PDF links work
- [ ] Manual testing:
  - [ ] Test UI across sizes/browsers (desktop, tablet, mobile)
  - [ ] Check number of network round-trips (minimize for performance)
- [ ] Consider updating or removing "Why have a webpage?" section (revisit after blog migration)

## In Progress 🚧
- Blog migration from Medium
  - MT part 3 didn't convert correctly — needs to be done manually
  - Touch up Future Crap Part 1: some images were dropped during conversion ✅ fixed
  - Re-download 2 rate-limited mt-chat-3 images ✅ fixed (downloaded as .webp, renamed accordingly)
  - Improve posts where Medium subtitle/heading got duplicated, making blog-index snippets uninformative (e.g., Future Crap posts)
  - Add CSS to center images in blog posts ✅
  - Review code blocks in all converted posts — ensure correct language tags for syntax highlighting (python, yaml, etc.)
- Older blog migration from WordPress
    - Tried to find the old export feature but it looks like it's gone
    - Export XML: https://github.com/ktrnka/resume/blob/main/data_exports/wordpress/trnkaphd.WordPress.2025-07-26.xml (warning: slow page load!)
    - Research Python libraries for processing WordPress XML exports (e.g., `wordpress-export-to-markdown`), or write a custom parser. This looks reasonable: https://pypi.org/project/wpparser/


## Backlog 📋
- Blog — bugs found in local preview
    - ~~**Broken images in WP posts**~~ ✅ Fixed: converted all 24 affected WP posts to use `{{ "/assets/img/posts/wp/..." | relative_url }}` Liquid filter
    - ~~**Missing paragraph breaks in old WP posts**~~ ✅ Fixed: inserted blank lines between adjacent paragraph lines across all 73 WP-era posts (2010–2016) using a Python script that preserves front matter, code blocks, setext headings, and tight lists
- Blog
    - Add paper/reference links to academic blog posts (MT series, etc.) — many papers are cited by name but not linked; find DOIs or Google Scholar links so readers can follow the research
    - Cross-post project navigation: Several blog series span many posts (LoL/ML prediction series, Searchify/synonyms series, MTurk series, Over 9000 series). Research a good way to surface this — options include Jekyll `categories:` or `tags:`, a naming convention in titles, a dedicated "series" collection, or a handcrafted index page per project. Goal: readers landing on one post in a series can easily find the others.
    - High-res WP images: some downloaded images are very large (up to 3996×1926px). Options: (a) add `max-width: 100%` CSS for post images (cheap, browser scales down), (b) run a batch resize script with ImageMagick (`mogrify -resize 1200x\> *.png`) before deploying, (c) serve both and use `srcset`. At minimum ensure CSS prevents them from breaking the layout.
    - Remove smart quotes from all converted blog posts (create script to automate)
    - Begin converting old Medium articles to the new form (waiting on export)
    - Begin converting old WordPress articles to the new form
    - Research and implement email notification system for blog updates (RSS-to-email services, etc.)
    - Look into Medium post claps/views/stats — identify most popular posts and consider light optimization on top performers
    - Write a post about why I'm moving blog hosting again (Medium → self-hosted Jekyll)
    - Set up private repo for blog drafts/candidates
      - Use git submodule for private repo (lives in same directory tree but separate version control)
      - Ensure private submodule is in .gitignore of public repo
      - Merge existing content aggregation repo (has tooling for Reddit posts, YouTube office hours, emails/advice docs)
      - Workflow: aggregation → drafts → manual review/editing → manual copy to public _posts/ → commit to public repo
- AI/Development tooling
    - Create .github/copilot-instructions.md with project-specific guidance
    - Document common task patterns as Copilot skills
- Recipes
    - Consider merging the recipes repo into this one
- Seattle outdoor volunteering calendar: Link from my site
- Scripting support
    - Check for dead links (CI test)
    - Check for redirected links: It'll be faster for users if the links are direct not redirects
    - Search `_posts/` for remaining `[caption` WP shortcodes (not all were caught by the batch cleanup): `grep -r '\[caption' _posts/`
    - Search `_posts/` for `kwtrnka.wordpress.com/tag/` URLs (WP tag links that should be replaced or removed): `grep -r 'kwtrnka.wordpress.com/tag/' _posts/`
- Tech debt:
    - Reduce code duplication between the index layout and default page layouts
    - Fix Sass @import deprecation warning (migrate to @use/@forward before Dart Sass 3.0.0)
    - The internal links don't work (need to copy the subdir thing from recipes deployment script)
    - I edited the Github Action to use the standard patterns from other repos to help fix relative links, but that effort removed local testing too! 003a0513e2dbb2456ac792007c068c8dc4197d9f
- Content
    - Make a folder for guides, move hiking and detrashing to there
    - Bring the Kodable tips over
    - Write a basic crawler from my old blog because their site is super broken: https://kwtrnka.wordpress.com/feed/
- Mobile layout: I checked the pages and most look good. The homepage is a little janky though (the sidebar/header is now above the main content, which is good, but it's not aligned very nicely)

Notes:
- Raw HTML snapshots are in `download/`.
- Extraction script: `python/extract_html_text.py`
- Working branch: `import/keith-trnka-com`.
- Color palette: Mauve/maroon accents (#7f1146) from original site
- Layout: Two-column index (name+links | content), single-column wider for other pages
- Link styling: External links marked with ↗, underline on hover (no bold to prevent layout shift)
- Profile photo: Only on index, not other pages
- Navigation: Sidebar links grouped (internal, HR, external)
- GitHub Pages URL for now, custom domain later

What's the Jekyll SEO thing about?
- Fills out the HTML HEAD from _config data: page title, description, canonical URL, Open Graph tags, JSON-LD, etc
- Not too exciting https://jekyll.github.io/jekyll-seo-tag/usage/

# Link checking

## Site-internal links
Build the Jekyll site, then run a checker against _site/ with external checks disabled (so it’s deterministic and fast). HTMLProofer supports disabling external checks (--disable-external) and is commonly used exactly this way for Jekyll output.

Practical tip: for Jekyll’s “pretty URLs” (extensionless), HTMLProofer recommends an “assume extension” mode so internal links like /about/ don’t look broken when validating files on disk.
​
## Site-external links (harder due to rate limits, etc)
Use GitHub Actions’ on: schedule with a cron expression to run periodic link checks on the default branch (e.g., daily/weekly). GitHub Actions documents that scheduled workflows use POSIX cron syntax and run on the latest commit of the default branch.
​

With Lychee, there’s an official “check repository links once per day” recipe that demonstrates using schedule and optionally creating an issue when broken links are found.
​
That recipe also shows running Lychee with fail: false so the workflow doesn’t fail, which is ideal for external links (you get a report/issue instead of red CI).
​
# Auto image optimization
> Do image optimization outside Jekyll (e.g., a script/CI step that compresses/resizes into assets/), then have Jekyll just reference the optimized files. This is commonly recommended because image optimization can slow builds and is easier to control as a separate pipeline step.

Conclusion: Not worth the effort for a tiny number of images

# Research Jekyll best practices for performance optimization

- Run Lighthouse/PageSpeed or WebPageTest against production, then optimize the top offenders (usually images, fonts, third-party). Jekyll itself isn’t typically the bottleneck for end-user load time; asset choices are.
- Be cautious with third-party embeds (Medium widgets, social widgets, etc.) since they can dominate load time even on an otherwise static site.
​- Resize to display size and serve responsive variants (srcset / <picture>), otherwise you’re sending “kilobytes of pixels the user will never see.”
- Use loading="lazy" for below-the-fold images so the initial render isn’t blocked by long image downloads