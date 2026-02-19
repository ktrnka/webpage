import argparse
import base64
import datetime
import json
import os
from pprint import pprint
import wpparser
from markdownify import markdownify

def load_data(input_file: str):
    return wpparser.parse(input_file)


def save_data(data, output_file: str):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

class BytesEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("ascii")
        else:
            return super().default(o)


def main():
    args = argparse.ArgumentParser(description="Extract WordPress data")
    args.add_argument("input", type=str, help="Path to the input file")
    args.add_argument("output", type=str, help="Path to the output directory")
    parsed_args = args.parse_args()

    data = load_data(parsed_args.input)

    for post in data["posts"]:
        post_title = post["title"]
        post_slug = post["post_name"]
        try:
            # I'd rather use post_date_gmt but it has junk values in many posts
            post_date = datetime.datetime.fromisoformat(post["post_date"])
            post_content_html = post["content"]
            post_type = post["post_type"]

            # attachments don't have the image content and don't seem to add anything
            if post_type in {"attachment"}:
                continue

            # Generate the filename like YYYY-MM-DD-slug.md
            filename = f"{post_date.strftime('%Y-%m-%d')}-{post_slug}.md"

            with open(os.path.join(parsed_args.output, filename), "w") as f:
                f.write(f"""
---
layout: post
title: {post_title}
date: {post_date.strftime('%Y-%m-%d')}
---
{markdownify(post_content_html)}
""")
        except Exception as e:
            print(f"Error processing post '{post_title}': {e}")

            # Dump the full thing
            with open(os.path.join(parsed_args.output, f"{post_slug}-error.json"), "w") as error_file:
                json.dump(post, error_file, indent=2)



if __name__ == "__main__":
    main()
