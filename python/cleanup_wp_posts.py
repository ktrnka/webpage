"""
Batch cleanup of WordPress-migrated posts in webpage/_posts/.

Fixes applied to each post:
  1. [caption] shortcodes → clean markdown image with local path
  2. Linked markdown images [![alt](wp-url)](any-url) → ![alt](local-path)
  3. Plain markdown images ![alt](wp-url) → ![alt](local-path)
  4. Internal WP post links → local Jekyll URLs (/blog/YYYY/MM/slug/)
  5. Smart quotes / curly apostrophes → straight ASCII equivalents

Usage:
    # Dry run — print what would change without writing files
    uv run cleanup_wp_posts.py

    # Apply changes
    uv run cleanup_wp_posts.py --apply
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "webpage" / "_posts"
WP_IMAGE_DIR = REPO_ROOT / "webpage" / "assets" / "img" / "posts" / "wp"
LOCAL_IMAGE_PREFIX = "/assets/img/posts/wp"

WP_HOST = "kwtrnka.wordpress.com"
JEKYLL_BLOG_PREFIX = "/blog"

# ---------------------------------------------------------------------------
# Rebuild URL → local filename mapping
# (mirrors the logic in download_wp_images.py so filenames are consistent)
# ---------------------------------------------------------------------------
WP_IMAGE_PATTERN = re.compile(
    r"https?://kwtrnka\.wordpress\.com/wp-content/uploads/[^\s\"')>]+"
)


def strip_query(url: str) -> str:
    """Remove query string and normalize http→https (WP redirects anyway)."""
    parsed = urlparse(url)
    scheme = "https" if parsed.scheme == "http" else parsed.scheme
    return urlunparse(parsed._replace(scheme=scheme, query="", fragment=""))


def assign_local_filename(url: str, used_names: dict[str, str]) -> str:
    """
    Same collision-resolution logic as download_wp_images.py.
    used_names maps filename → url that claimed it.
    """
    raw_name = Path(urlparse(url).path).name
    if not raw_name:
        import hashlib
        raw_name = hashlib.md5(url.encode()).hexdigest()[:12] + ".bin"
    stem = Path(raw_name).stem
    suffix = Path(raw_name).suffix
    candidate = raw_name
    counter = 2
    while candidate in used_names and used_names[candidate] != url:
        candidate = f"{stem}_{counter}{suffix}"
        counter += 1
    return candidate


def build_url_to_local(posts_dir: Path) -> dict[str, str]:
    """
    Returns {clean_wp_url: local_filename} for every WP image found in posts.
    """
    url_to_posts: dict[str, list[str]] = {}
    for post_path in sorted(posts_dir.glob("*.md")):
        text = post_path.read_text(encoding="utf-8")
        for raw_url in WP_IMAGE_PATTERN.findall(text):
            clean = strip_query(raw_url)
            url_to_posts.setdefault(clean, [])
            if post_path.name not in url_to_posts[clean]:
                url_to_posts[clean].append(post_path.name)

    used_names: dict[str, str] = {}  # filename → url
    url_to_local: dict[str, str] = {}
    for url in url_to_posts:
        fname = assign_local_filename(url, used_names)
        used_names[fname] = url
        url_to_local[url] = fname
    return url_to_local


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def wp_url_to_local_img(raw_url: str, url_map: dict[str, str]) -> str | None:
    """Given a raw WP image URL (may have query params), return '/assets/img/posts/wp/filename'."""
    clean = strip_query(raw_url)
    fname = url_map.get(clean)
    if fname:
        return f"{LOCAL_IMAGE_PREFIX}/{fname}"
    return None


def wp_post_url_to_jekyll(url: str) -> str | None:
    """
    Convert https://kwtrnka.wordpress.com/YYYY/MM/DD/slug/ to /blog/YYYY/MM/slug/
    Tag and category pages are NOT converted (return None).
    """
    parsed = urlparse(url)
    if parsed.netloc not in (WP_HOST, f"www.{WP_HOST}"):
        return None
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    # Tag/category pages — leave as external
    if parts and parts[0] in ("tag", "category", "wp-content", "feed"):
        return None
    # Expect YYYY/MM/DD/slug or YYYY/MM/slug
    if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
        year, month = parts[0], parts[1]
        # Skip day component if present
        slug_start = 3 if (len(parts) >= 4 and parts[2].isdigit()) else 2
        slug = "/".join(parts[slug_start:])
        if slug:
            return f"{JEKYLL_BLOG_PREFIX}/{year}/{month}/{slug}/"
    return None


# ---------------------------------------------------------------------------
# Per-post fixes
# ---------------------------------------------------------------------------

# 1. [caption] shortcodes
# Pattern A: caption="..." attribute  →  use that as alt text
CAPTION_ATTR_RE = re.compile(
    r'\[caption[^\]]*caption="([^"]*)"[^\]]*\]'   # opening tag with caption attr
    r'(\[!\[.*?\]\(.*?\)\]\(.*?\))'                # linked image [![alt](url)](url)
    r'\[/caption\]',
    re.DOTALL
)
# Pattern B: caption text after the image, before [/caption]
CAPTION_BODY_RE = re.compile(
    r'\[caption[^\]]*\]'                           # opening tag (no caption attr)
    r'(\[!\[.*?\]\(.*?\)\]\(.*?\))'                # linked image
    r'([^\[]*?)'                                   # caption text after image
    r'\[/caption\]',
    re.DOTALL
)

# Inner linked image: [![alt](url "title")](url)
LINKED_IMG_RE = re.compile(
    r'\[!\[([^\]]*)\]\(([^)]*?)\)\]\([^)]*\)'
)


def extract_wp_url_from_linked_img(linked_img_md: str) -> str | None:
    """Pull the src URL out of [![alt](url)](url) markdown."""
    m = LINKED_IMG_RE.match(linked_img_md.strip())
    if m:
        return m.group(2).split()[0]  # strip any title token
    return None


def fix_captions(text: str, url_map: dict[str, str]) -> str:
    def replace_caption_attr(m: re.Match) -> str:
        caption_text = m.group(1)
        linked_img = m.group(2)
        raw_url = extract_wp_url_from_linked_img(linked_img)
        local = wp_url_to_local_img(raw_url, url_map) if raw_url else None
        if local:
            return f"![{caption_text}]({local})"
        # Fallback: keep original linked image, just remove caption tags
        return linked_img

    def replace_caption_body(m: re.Match) -> str:
        linked_img = m.group(1)
        caption_text = m.group(2).strip()
        raw_url = extract_wp_url_from_linked_img(linked_img)
        local = wp_url_to_local_img(raw_url, url_map) if raw_url else None
        if local:
            return f"![{caption_text}]({local})"
        return linked_img

    text = CAPTION_ATTR_RE.sub(replace_caption_attr, text)
    text = CAPTION_BODY_RE.sub(replace_caption_body, text)
    return text


# 2 & 3. Linked + plain WP images (match http:// and https://)
# [![alt](wp-url "title")](any-url) or [![alt](wp-url)](any-url)
LINKED_WP_IMG_RE = re.compile(
    r'\[!\[([^\]]*)\]\((https?://kwtrnka\.wordpress\.com/wp-content/uploads/[^)">\s]*)'
    r'(?:\s+"[^"]*")?\)\]\([^)]*\)'
)
# ![alt](wp-url "title") or ![alt](wp-url)
PLAIN_WP_IMG_RE = re.compile(
    r'!\[([^\]]*)\]\((https?://kwtrnka\.wordpress\.com/wp-content/uploads/[^)">\s]*)'
    r'(?:\s+"[^"]*")?\)'
)


def fix_images(text: str, url_map: dict[str, str]) -> str:
    def replace_linked(m: re.Match) -> str:
        alt, raw_url = m.group(1), m.group(2)
        local = wp_url_to_local_img(raw_url, url_map)
        if local:
            return f"![{alt}]({local})"
        return m.group(0)  # unchanged

    def replace_plain(m: re.Match) -> str:
        alt, raw_url = m.group(1), m.group(2)
        local = wp_url_to_local_img(raw_url, url_map)
        if local:
            return f"![{alt}]({local})"
        return m.group(0)

    text = LINKED_WP_IMG_RE.sub(replace_linked, text)
    text = PLAIN_WP_IMG_RE.sub(replace_plain, text)
    return text


# 4. Internal WP post links (non-image; images already handled above)
# Match both http and https, with or without trailing slash
WP_LINK_RE = re.compile(
    r'https?://kwtrnka\.wordpress\.com(/[^\s"\')\]]*)'
)


def fix_internal_links(text: str) -> str:
    def replace_link(m: re.Match) -> str:
        full_url = m.group(0)
        local = wp_post_url_to_jekyll(full_url)
        return local if local else full_url

    return WP_LINK_RE.sub(replace_link, text)


# 5. Smart quotes
SMART_QUOTE_MAP = str.maketrans({
    "\u2018": "'",   # left single quotation mark
    "\u2019": "'",   # right single quotation mark / apostrophe
    "\u201C": '"',   # left double quotation mark
    "\u201D": '"',   # right double quotation mark
    "\u2013": "-",   # en dash
    "\u2014": "--",  # em dash
})


def fix_smart_quotes(text: str) -> str:
    return text.translate(SMART_QUOTE_MAP)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_post(path: Path, url_map: dict[str, str], apply: bool) -> list[str]:
    """
    Apply all fixes to one post. Returns a list of change description strings.
    If apply=True, writes the file. Otherwise just reports.
    """
    original = path.read_text(encoding="utf-8")
    text = original

    text = fix_captions(text, url_map)
    text = fix_images(text, url_map)
    text = fix_internal_links(text)
    text = fix_smart_quotes(text)

    if text == original:
        return []

    # Summarise changes
    changes = []
    for label, orig_pat, new_text_fn in [
        ("[caption] tags", re.compile(r'\[/?caption'), None),
        ("wp-content image URLs", re.compile(r'wp-content/uploads'), None),
        ("wordpress.com links", re.compile(r'kwtrnka\.wordpress\.com'), None),
        ("smart quotes", re.compile(r'[\u2018\u2019\u201C\u201D\u2013\u2014]'), None),
    ]:
        before = len(orig_pat.findall(original))
        after = len(orig_pat.findall(text))
        if before != after or (before > 0 and label == "smart quotes"):
            changes.append(f"  {label}: {before} → {after}")

    if apply:
        path.write_text(text, encoding="utf-8")

    return changes


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean up WordPress artifacts in _posts/ markdown files"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to files (default: dry run, print only)",
    )
    args = parser.parse_args()

    if not args.apply:
        print("DRY RUN — pass --apply to write changes\n")

    print("Building URL → local filename map …")
    url_map = build_url_to_local(POSTS_DIR)
    print(f"  {len(url_map)} WP image URLs mapped\n")

    changed = 0
    unchanged = 0
    total_issues: dict[str, int] = {}

    for post_path in sorted(POSTS_DIR.glob("*.md")):
        changes = process_post(post_path, url_map, apply=args.apply)
        if changes:
            changed += 1
            print(f"{'UPDATED' if args.apply else 'WOULD UPDATE'}  {post_path.name}")
            for c in changes:
                print(c)
        else:
            unchanged += 1

    verb = "Updated" if args.apply else "Would update"
    print(f"\n{verb} {changed} files, {unchanged} already clean.")
    if not args.apply and changed:
        print("Run with --apply to write changes.")


if __name__ == "__main__":
    main()
