#!/usr/bin/env python3
"""Check local href/src links in the static site."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlsplit


SKIPPED_SCHEMES = {"http", "https", "mailto", "tel"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.links.append((name, value))


def iter_html_files(site_root: Path) -> list[Path]:
    return sorted(site_root.glob("*.html"))


def local_target(source: Path, site_root: Path, raw_link: str) -> Path | None:
    parsed = urlsplit(raw_link)
    if parsed.scheme in SKIPPED_SCHEMES or parsed.netloc:
        return None
    if not parsed.path:
        return None

    path = Path(unquote(parsed.path))
    if path.is_absolute():
        return site_root / path.relative_to("/")
    return source.parent / path


def check_site(site_root: Path) -> list[str]:
    missing: list[str] = []
    for html_file in iter_html_files(site_root):
        parser = LinkParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for attr, raw_link in parser.links:
            target = local_target(html_file, site_root, raw_link)
            if target is not None and not target.exists():
                missing.append(
                    f"{html_file.relative_to(site_root)} {attr}={raw_link!r} -> "
                    f"{target.relative_to(site_root)}"
                )
    return missing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_root", nargs="?", default="site")
    args = parser.parse_args()

    site_root = Path(args.site_root)
    missing = check_site(site_root)
    if missing:
        for item in missing:
            print(f"missing local site link: {item}")
        raise SystemExit(1)

    checked = len(iter_html_files(site_root))
    print(f"site local links verified: html_files={checked}")


if __name__ == "__main__":
    main()
