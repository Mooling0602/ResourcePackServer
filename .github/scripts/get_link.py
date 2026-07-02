#!/usr/bin/env python3
"""Generate GitHub repository links for this project."""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def repo_url() -> str:
    manifest = json.loads(Path("src/mcdreforged.plugin.json").read_text(encoding="utf-8"))
    link = manifest.get("link")
    if not isinstance(link, str) or not link:
        raise SystemExit("Missing string 'link' in src/mcdreforged.plugin.json")

    parsed = urlparse(link)
    if parsed.scheme not in {"http", "https"} or parsed.netloc != "github.com":
        raise SystemExit(f"Unsupported GitHub repository link: {link}")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise SystemExit(f"Invalid GitHub repository link: {link}")

    return f"https://github.com/{parts[0]}/{parts[1]}"


def compare_url(base_repo_url: str, old_tag: str, new_tag: str = "") -> str:
    if new_tag:
        return f"{base_repo_url}/compare/{old_tag}...{new_tag}"
    return f"{base_repo_url}/compare/{old_tag}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GitHub links for this repo.")
    parser.add_argument("--repo", action="store_true", help="Return repository URL.")
    parser.add_argument("--issues", action="store_true", help="Return GitHub Issues URL.")
    parser.add_argument("--actions", action="store_true", help="Return GitHub Actions URL.")
    parser.add_argument(
        "--compare",
        nargs="*",
        metavar=("<old_tag>", "[<new_tag>]"),
        help="Return compare URL. Accepts one tag or old/new tags.",
    )
    args = parser.parse_args()

    base = repo_url()
    if args.compare is not None:
        if len(args.compare) == 1:
            print(compare_url(base, args.compare[0]))
        elif len(args.compare) == 2:
            print(compare_url(base, args.compare[0], args.compare[1]))
        else:
            print("Error: --compare accepts 1 or 2 arguments.", file=sys.stderr)
            raise SystemExit(1)
    elif args.issues:
        print(f"{base}/issues")
    elif args.actions:
        print(f"{base}/actions")
    else:
        print(base)


if __name__ == "__main__":
    main()
