# TrilliumVideoEmbedConverter

Converts includeded notes that contain video attachments, into embedded videos in the HTML archive export.

## What it does

Scans an exported Trilium HTML file for <section class="include-note"> placeholders,
takes the text from the <p> directly above each placeholder (expects the filename
without extension), and replaces both the <p> and the placeholder with an HTML5
video embed using `{filename}.mp4`.

## Setup

- Python 3.8+
- Create and activate a virtual environment (recommended):
    - Windows:

        ```powershell
        python -m venv .venv
        .venv\Scripts\Activate.ps1
        ```

    - POSIX (macOS/Linux):

        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```

- Install dependencies:

    ```bash
    pip install beautifulsoup4
    ```

## Usage

- The script can be run from wherever it is installed. The script does not assume your current directory is the HTML archive root. Always pass an absolute path to the HTML file (or archive) you want to process.

Example (absolute path):

```bash
python TrilliumConverter.py "D:/Downloads/HtmlArchive.zip"
```

## Options

- `--no-backup` — do not create a `.bak` backup of the input file.

## Example

If your HTML contains:

```html
<p>Video Name</p>
<section class="include-note" data-note-id="asdfasdf"></section>
```

The script will replace them with a video referencing `Video Name.mp4`.

## Notes

- The script makes a `.bak` copy of the original file by default.
- Filenames may contain spaces. The script will append `.mp4` to the text found.
