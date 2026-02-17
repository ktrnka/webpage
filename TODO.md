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

## Before Merge/Deploy 🚀
- [x] Add missing "Blog before 2017" link (https://kwtrnka.wordpress.com/)
- [ ] Verify all 33 PDF links work
- [ ] Test GitHub Pages build (verify GitHub Actions succeeds)
- [ ] Manual testing:
  - [ ] Test UI across sizes/browsers (desktop, tablet, mobile)
  - [ ] Check number of network round-trips (minimize for performance)
- [ ] Consider updating or removing "Why have a webpage?" section (revisit after blog migration)

## In Progress 🚧


## Backlog 📋
- Blog
    - Create a blog section
    - Begin converting old Medium articles to the new form
    - Begin converting old WordPress articles to the new form
- Recipes
    - Consider merging the recipes repo into this one
- Scripting support
    - Check for dead links (CI test)
    - Check for redirected links: It'll be faster for users if the links are direct not redirects
- Tech debt:
    - Reduce code duplication between the index layout and default page layouts
    - Fix Sass @import deprecation warning (migrate to @use/@forward before Dart Sass 3.0.0)
    - The internal links don't work (need to copy the subdir thing from recipes deployment script)
    - I edited the Github Action to use the standard patterns from other repos to help fix relative links, but that effort removed local testing too! 003a0513e2dbb2456ac792007c068c8dc4197d9f

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