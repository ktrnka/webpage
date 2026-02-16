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

## In Progress 🚧
- [ ] Visual improvements:
  - [ ] Two-column index layout (left: name+photo+links; right: content)
  - [ ] Visually separate internal vs external links
  - [ ] One-column centered layout for non-index pages (wider content area)
  - [ ] Fix page titles: "Keith Trnka" for home, "Page | Keith Trnka" for others
  - [ ] Replace bold-on-hover for links with standard styling
  - [ ] Restore missing inline links (Palia, Singularity 6, 98point6, Swype, etc.)
  - [ ] Remove "Hosted on GitHub Pages" footer

## Backlog 📋
- [ ] Find and add link for: Kamboj et al. AAMAS workshop 2010 (Electric Vehicle Coalitions)
- [ ] Find and add link for: Elzer et al. ACL 2005 (information graphics captions)
- [ ] Review and approve remaining assets to include (images, fonts)
- [ ] Consider: reformat citations (APA/IEEE) or add BibTeX export
- [ ] Consider: split publications into year‑indexed pages

Notes:
- Raw HTML snapshots are in `download/`.
- Extraction script: `python/extract_html_text.py`
- Working branch: `import/keith-trnka-com`.

