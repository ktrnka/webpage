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
- [ ] Find and add link for: Kamboj et al. AAMAS workshop 2010 (Electric Vehicle Coalitions)
- [ ] Find and add link for: Elzer et al. ACL 2005 (information graphics captions)
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
- Research:
    - Look into Jekyll plugins for automated link testing
    - Look into Jekyll plugins for automated image optimization/sizing
    - Research Jekyll best practices for performance optimization
    - What's the Jekyll SEO thing about?

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

