#!/usr/bin/env python3
"""Replace Trilium include-note placeholders with HTML5 video embeds.

Usage:
  python tools/embed_videos.py path/to/file.html

The script will create a backup of the original file with a .bak extension
before writing changes.
"""
import argparse
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote


def meaningful_text(p_tag):
    if p_tag is None:
        return None
    txt = p_tag.get_text(separator="", strip=True)
    if not txt:
        return None
    # normalize non-breaking spaces to regular spaces so filenames aren't polluted
    txt = txt.replace('\xa0', ' ').strip()
    if not txt:
        return None
    return txt


def process_file(path: Path, backup: bool = True) -> int:
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    replaced = 0
    # Find all anchor links that reference .mp4 files and have class "reference-link".
    anchors = list(soup.find_all("a", class_="reference-link"))
    for a in anchors:
        href = a.get("href")
        if not href:
            continue

        # Check for .mp4 in the (possibly percent-encoded) href
        if ".mp4" not in unquote(href).lower():
            continue

        # Normalize/encode the href so it is safe to use as video src.
        # Preserve existing path separators.
        href_unquoted = unquote(href)
        video_src = quote(href_unquoted, safe="/")

        # build figure/video
        figure = soup.new_tag("figure", **{"class": "video"})
        video = soup.new_tag("video", controls=True)
        video.attrs["style"] = "width:100%;max-width:1200px;"
        source = soup.new_tag("source", src=video_src, type="video/mp4")
        video.append(source)
        fallback = soup.new_string(
            "Your browser does not support the video tag. You can download the video.")
        video.append(fallback)
        figure.append(video)

        # If the anchor is wrapped in a <p>, replace the entire <p>, otherwise replace the anchor.
        parent = a.parent
        if parent and parent.name == "p":
            parent.replace_with(figure)
        else:
            a.replace_with(figure)

        replaced += 1

    if replaced:
        if backup:
            bak = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, bak)
        # Preserve original character entities and avoid smart-quote/nbsp conversions
        html_out = soup.decode(formatter="html")
        path.write_text(html_out, encoding="utf-8")

    return replaced


def main():
    parser = argparse.ArgumentParser(
        description="Embed videos in exported Trilium HTML")
    parser.add_argument("file", type=Path, help="HTML file to process")
    parser.add_argument("--no-backup", dest="backup",
                        action="store_false", help="Don't create a .bak backup")
    args = parser.parse_args()

    if not args.file.exists():
        print("File not found:", args.file)
        raise SystemExit(2)

    try:
        count = process_file(args.file, backup=args.backup)
        print(f"Processed {args.file}: replaced {count} include-note(s).")
    except Exception as e:
        print("Error:", e)
        raise


if __name__ == "__main__":
    main()
