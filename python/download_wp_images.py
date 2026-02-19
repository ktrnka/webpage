"""
Download images referenced in WordPress-migrated blog posts.

Usage:
    # List mode (no network calls) — validate URLs and see what would be downloaded
    uv run download_wp_images.py

    # Download all images
    uv run download_wp_images.py --download

    # Test with only the first 5 images
    uv run download_wp_images.py --download --limit 5

    # Tune rate limit or user agent if needed
    uv run download_wp_images.py --download --rate-limit 2.0
    uv run download_wp_images.py --download --user-agent "Mozilla/5.0 ..."
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, urlunparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "webpage" / "_posts"
OUTPUT_DIR = REPO_ROOT / "webpage" / "assets" / "img" / "posts" / "wp"

# Only download images hosted on WordPress
WP_IMAGE_PATTERN = re.compile(
    r"https://kwtrnka\.wordpress\.com/wp-content/uploads/[^\s\"')>]+"
)

DEFAULT_RATE_LIMIT = 5.0  # seconds between requests
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


# ---------------------------------------------------------------------------
# URL extraction
# ---------------------------------------------------------------------------
def extract_urls_from_posts(posts_dir: Path) -> dict[str, list[str]]:
    """
    Returns a dict mapping each unique image URL (query-stripped, full-res)
    to the list of post filenames that reference it.
    """
    url_to_posts: dict[str, list[str]] = {}

    for post_path in sorted(posts_dir.glob("*.md")):
        text = post_path.read_text(encoding="utf-8")
        matches = WP_IMAGE_PATTERN.findall(text)
        for raw_url in matches:
            clean_url = strip_resize_params(raw_url)
            url_to_posts.setdefault(clean_url, [])
            if post_path.name not in url_to_posts[clean_url]:
                url_to_posts[clean_url].append(post_path.name)

    return url_to_posts


def strip_resize_params(url: str) -> str:
    """Remove query string (e.g. ?w=300) to get the full-resolution image."""
    parsed = urlparse(url)
    return urlunparse(parsed._replace(query="", fragment=""))


def validate_url(url: str) -> tuple[bool, str]:
    """Basic structural validation via urlparse. Returns (is_valid, reason)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, f"bad scheme: {parsed.scheme!r}"
    if not parsed.netloc:
        return False, "missing netloc"
    if not parsed.path or parsed.path == "/":
        return False, "empty path"
    return True, "ok"


# ---------------------------------------------------------------------------
# Filename assignment (collision-safe)
# ---------------------------------------------------------------------------
def assign_local_filename(url: str, used_names: set[str]) -> str:
    """
    Derive a local filename from the URL's last path component.
    If that name is already taken (collision from a different URL), append _2, _3, …
    """
    raw_name = Path(urlparse(url).path).name
    if not raw_name:
        # Fallback: hash-based name
        import hashlib
        raw_name = hashlib.md5(url.encode()).hexdigest()[:12] + ".bin"

    stem = Path(raw_name).stem
    suffix = Path(raw_name).suffix
    candidate = raw_name
    counter = 2
    while candidate in used_names:
        candidate = f"{stem}_{counter}{suffix}"
        counter += 1
    return candidate


# ---------------------------------------------------------------------------
# Download + verify
# ---------------------------------------------------------------------------
def download_image(
    url: str,
    dest_path: Path,
    user_agent: str,
) -> bool:
    """Download url to dest_path. Returns True on success."""
    import requests  # lazy import so list-mode works without the package

    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        dest_path.write_bytes(response.content)
        return True
    except Exception as exc:
        print(f"  ERROR downloading {url}: {exc}", file=sys.stderr)
        return False


def verify_image_file(path: Path) -> str:
    """Run `file` on the downloaded path and return its output string."""
    try:
        result = subprocess.run(
            ["file", str(path)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except Exception as exc:
        return f"(file check failed: {exc})"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract and optionally download WordPress images from _posts/"
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Actually download the images (default: list mode only)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Only download the first N images (useful for testing)",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=DEFAULT_RATE_LIMIT,
        metavar="SECONDS",
        help=f"Seconds to wait between requests (default: {DEFAULT_RATE_LIMIT})",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        metavar="STRING",
        help="HTTP User-Agent header to send",
    )
    args = parser.parse_args()

    # ---- Extract URLs ----
    print(f"Scanning posts in: {POSTS_DIR}")
    url_to_posts = extract_urls_from_posts(POSTS_DIR)

    if not url_to_posts:
        print("No WordPress image URLs found.")
        return

    # ---- Validate and report ----
    valid_urls: list[str] = []
    invalid_count = 0
    print(f"\nFound {len(url_to_posts)} unique image URL(s):\n")

    for url, posts in url_to_posts.items():
        ok, reason = validate_url(url)
        status = "✓" if ok else f"✗ ({reason})"
        posts_str = ", ".join(posts)
        print(f"  {status}  {url}")
        print(f"         referenced in: {posts_str}")
        if ok:
            valid_urls.append(url)
        else:
            invalid_count += 1

    print(f"\nSummary: {len(valid_urls)} valid, {invalid_count} invalid")

    if not args.download:
        print("\n(List mode — pass --download to fetch images)")
        return

    # ---- Download ----
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    urls_to_download = valid_urls[: args.limit] if args.limit else valid_urls

    if args.limit:
        print(f"\nDownloading first {args.limit} of {len(valid_urls)} images …")
    else:
        print(f"\nDownloading {len(valid_urls)} images …")
    print(f"Output dir: {OUTPUT_DIR}\n")

    used_names: set[str] = {p.name for p in OUTPUT_DIR.iterdir()} if OUTPUT_DIR.exists() else set()
    skipped = 0
    downloaded = 0
    warnings = 0

    for i, url in enumerate(urls_to_download):
        filename = assign_local_filename(url, used_names)
        dest = OUTPUT_DIR / filename

        # Skip if already downloaded (idempotent)
        if dest.exists():
            print(f"  skip  {filename}  (already exists)")
            skipped += 1
            continue

        if i > 0:
            time.sleep(args.rate_limit)

        print(f"  [{i + 1}/{len(urls_to_download)}]  {filename}", end=" … ", flush=True)
        success = download_image(url, dest, args.user_agent)

        if not success:
            print("FAILED")
            warnings += 1
            continue

        # Verify it's actually an image
        file_output = verify_image_file(dest)
        is_image = "image" in file_output.lower() or "bitmap" in file_output.lower()

        if is_image:
            print(f"✓  ({file_output.split(':', 1)[-1].strip()})")
        else:
            print(f"⚠  WARNING — not an image? file says: {file_output}")
            warnings += 1

        used_names.add(filename)
        downloaded += 1

    print(f"\nDone: {downloaded} downloaded, {skipped} skipped, {warnings} warnings")


if __name__ == "__main__":
    main()
