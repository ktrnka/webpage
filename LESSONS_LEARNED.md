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
3. **Replace `graf` code block language** — Medium exports use ` ```graf ` as the language tag; replace with an appropriate language like `shell` or just remove it
4. **Remove the Medium footer** — Delete the last 3 lines: `By [Author](url) on [Date](url).`, the canonical link line, and the "Exported from Medium" line; also the preceding `---` HR separator
5. **Add Jekyll front matter**:

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

### Gist embeds in Medium posts

Medium gist embeds are lost in pandoc conversion — they show as nothing in the output. Check the original HTML for `<script src="https://gist.github.com/...">` tags and fetch the raw gist content:

```bash
curl -sL 'https://gist.githubusercontent.com/USER/ID/raw/HASH/filename.py' > tmp/snippet.py
```

Then insert as a fenced code block at the appropriate point in the post.
