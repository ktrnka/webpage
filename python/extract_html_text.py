#!/usr/bin/env python3
"""Extract readable text content from HTML files, ignoring scripts/styles."""

from html.parser import HTMLParser
import sys
from pathlib import Path


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_chunks = []
        self.in_script = False
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script = True
        self.current_tag = tag
            
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script = False
        if tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            self.text_chunks.append('\n')
            
    def handle_data(self, data):
        if not self.in_script:
            text = data.strip()
            if text and len(text) > 1:
                # Skip obvious JS/code fragments
                if not any(text.startswith(x) for x in ['window.', 'function', 'var ', 'const ', 'let ', '{', '}']):
                    self.text_chunks.append(text)


def extract_text(html_path):
    """Extract readable text from an HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = TextExtractor()
    parser.feed(content)
    return ' '.join(parser.text_chunks)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_html_text.py <html_file>")
        sys.exit(1)
    
    html_file = Path(sys.argv[1])
    if not html_file.exists():
        print(f"File not found: {html_file}")
        sys.exit(1)
    
    text = extract_text(html_file)
    print(text)
