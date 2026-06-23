# TrilliumVideoEmbedConverter

Converts Trilium-linked video references into embedded HTML5 videos in exported HTML.

## What it does

Older exports used <section class="include-note"> placeholders where the video
filename appeared in the `<p>` immediately above the section. This tool used that
pattern to construct `{filename}.mp4` and replace the `<p>` + `<section>` with a
video embed.

Newer Trilium exports place video attachments as regular links. The script now
searches for anchors like `<a class="reference-link" href="...mp4">` (it
decodes the href and checks for `.mp4`), then replaces the anchor — or the
wrapping `<p>` if present — with a `<figure><video>` embed using the anchor's
`href` as the `src` (the href is URL-normalized when necessary).

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

If your HTML contains a linked video (new approach):

```html
<p>
	<a
		class="reference-link"
		href="Evidence%20Journal/Proxy%20Mech%20Legs%20IK%20Setup.mp4"
		>Proxy Mech Legs IK Setup</a
	>
</p>
```

The script will replace the `<p><a>` with a `<figure>` containing a `<video>` whose
`<source src="...mp4">` matches the link's href.

## Notes

- The script makes a `.bak` copy of the original file by default.
- Filenames may contain spaces. The script will append `.mp4` to the text found.
