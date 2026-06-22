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
from urllib.parse import quote


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
    sections = list(soup.find_all("section", class_="include-note"))
    for sec in sections:
        # find previous meaningful <p> sibling
        prev = sec.find_previous_sibling()
        # walk backwards until we find a <p> or run out
        while prev is not None and prev.name != "p":
            prev = prev.find_previous_sibling()

        filename_base = meaningful_text(prev) if prev is not None else None
        if not filename_base:
            # no usable filename above this include-note; skip
            continue

        # strip extension if present
        if filename_base.lower().endswith(".mp4"):
            filename_base = filename_base[: -4]

        # Videos are stored in a folder that matches the HTML filename (without ext)
        media_folder = path.stem
        # URL-encode components to handle spaces and special chars
        video_src = f"{quote(media_folder)}/{quote(filename_base)}.mp4"

        # build figure/video
        figure = soup.new_tag("figure", **{"class": "video"})
        video = soup.new_tag("video", controls=True)
        video.attrs["style"] = "width:100%;max-width:1200px;"
        source = soup.new_tag("source", src=video_src, type="video/mp4")
        video.append(source)
        fallback = soup.new_string(
            f"Your browser does not support the video tag. You can download the video.")
        video.append(fallback)
        figure.append(video)

        # replace the <p> with the figure, and remove the section
        prev.replace_with(figure)
        sec.decompose()
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
