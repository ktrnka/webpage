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
