# Lessons Learned

## Blog Migration from Medium

### Pandoc Conversion Formats

When converting Medium HTML exports to Markdown using pandoc, **gfm-raw_html** (GitHub Flavored Markdown without raw HTML) produces the cleanest output:

```bash
pandoc 'input.html' -t gfm-raw_html --wrap=none -o output.md
```

**Comparison of formats tested:**

| Format | Content starts | Total lines | Heading format | Link format |
|--------|---------------|-------------|----------------|-------------|
| `markdown` | Line 330 | ~1098 | `## Heading {#id .class1 .class2}` | `[text](url){.class}` |
| `markdown-raw_attribute` | Line 327 | ~1098 | `## Heading {#id .class1 .class2}` | `[text](url){.class}` |
| `commonmark` | Line 508 | ~1497 | `## Heading` (clean) | `<a href="...">` (HTML) |
| `gfm-raw_html` | **Line 59** ✅ | **~349** ✅ | `## Heading` (clean) | `[text](url)` (clean) |

**Why gfm-raw_html is best:**
- Minimal UI clutter at the top (only ~58 lines vs 300-500+ for other formats)
- Clean markdown headings without CSS attributes
- Standard markdown link format
- Shortest output file by far
- Ready to use with minimal cleanup

**Recommendation:** Use `pandoc -t gfm-raw_html --wrap=none` for converting Medium HTML exports. The article content starts much earlier and requires minimal post-processing.

### Post-conversion cleanup checklist

After running pandoc, apply these fixes before saving as a Jekyll post:

1. **Remove the H1 title** (first line) — goes into front matter as `title:` instead
2. **Remove the truncated teaser line** — Medium adds a short preview sentence ending in `…` right after the title, followed by a `---` separator; delete both
3. **Check for Medium subtitle / duplicated heading** — Some posts have a subtitle or a repeated heading near the top (e.g., `### Post Title` appearing again right after the teaser removal). This makes the post snippet on the blog index uninformative. Clean it up so the first visible paragraph is real content.
4. **Replace `graf` code block language** — Medium exports use ` ```graf ` as the language tag; assign the correct language to every code block (e.g., `python`, `yaml`, `dockerfile`, `hcl`, `json`) so syntax highlighting works.
5. **Remove the Medium footer** — Delete the last 3 lines: `By [Author](url) on [Date](url).`, the canonical link line, and the "Exported from Medium" line; also the preceding `---` HR separator
6. **Add Jekyll front matter**:

```yaml
---
layout: post
title: <title from H1>
date: <YYYY-MM-DD from filename>
---
```

**One-liner for the mechanical parts** (run before final review):

```bash
pandoc 'download/medium/YYYY-MM-DD_Title-slug.html' -t gfm-raw_html --wrap=none | \
  sed '1{/^# /d}' | \
  sed '/^.*…$/{ N; /\n---/d }' | \
  sed 's/``` graf/```shell/g' | \
  sed '/^By \[/,$d' \
  > tmp/output.md
```

Use `tmp/` (repo root, gitignored) for intermediate files — not `/tmp/`.

Note: the sed for the teaser line is fragile; manual review of the first ~10 lines is recommended.

### Images in Medium posts

Medium exports reference images as `![](https://cdn-images-1.medium.com/max/800/...)`. Download them to `webpage/assets/img/posts/` with descriptive names and reference them with Jekyll's `relative_url` filter:

```markdown
![Alt text]({{ "/assets/img/posts/descriptive-name.png" | relative_url }})
```

Download command:
```bash
curl -sL 'https://cdn-images-1.medium.com/...' -o webpage/assets/img/posts/name.png
```

**Verify image count:** After converting, count image references in the draft (`grep -c 'cdn-images'`) and confirm it matches the number of `curl` downloads. It's easy to miss images, especially in image-heavy posts.

**Image centering:** Jekyll/kramdown has no centering shorthand. Recommended approach: add a CSS rule in `_sass/` that centers all `img` inside `.post` content (affects all post images uniformly). Alternatively wrap individual images in `<div style="text-align:center">` blocks. Implemented rule:
```scss
.post-content img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
```

**Download images one at a time** — Medium rate-limits batch downloads. If you download multiple images in a loop without delays, many will silently return an HTML error page (~8.9K or ~6.8K) instead of image data. Always download sequentially (one `curl` per image, no parallelism).

**Detecting bad downloads:** After downloading, verify with `file`:
```bash
file webpage/assets/img/posts/postname-* | grep -v 'image data'
```
Any line returned is a bad file (HTML or empty). Suspicious size pattern: bad files are suspiciously uniform (~8.9K or ~6.8K); real images vary widely (30K–2M). Use `ls -lh` to spot outliers at a glance.

**Re-downloading rate-limited images:** If a URL stays rate-limited across multiple retries in the same session, stop trying — Medium appears to block the specific URL for the session. Note the filename and URL in TODO.md and retry later (e.g., next day or different network).

**Mapping CDN URLs to descriptive filenames:** When you need to identify which CDN URL corresponds to which named file (e.g., after a failed batch download), grep the draft in `tmp/` with a few lines of context:
```bash
grep -B2 -A2 'partial-cdn-hash' tmp/postname-draft.md
```
The draft's image table (generated during conversion) maps line numbers, partial hashes, descriptions, and target filenames, making URL→name lookups fast.

### Gist embeds in Medium posts

Medium gist embeds are lost in pandoc conversion — they show as nothing in the output. Check the original HTML for `<script src="https://gist.github.com/...">` tags and fetch the raw gist content:

```bash
curl -sL 'https://gist.githubusercontent.com/USER/ID/raw/HASH/filename.py' > tmp/snippet.py
```

Then insert as a fenced code block at the appropriate point in the post.
