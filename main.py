"""Entry point: render the 24 November 2026 front page to entry.png.

Writes the image to $MAKEFUN_OUTPUT_DIR/entry.png (default /output),
and also next to this file when that directory is writable, so the
repository snapshot carries the rendered page.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build.draw import render_page


def main():
    page = render_page()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    page.save(os.path.join(outdir, "entry.png"), format="PNG")
    # Keep a copy beside this file for the repository snapshot.
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        page.save(os.path.join(here, "entry.png"), format="PNG")
    except OSError:
        pass


if __name__ == "__main__":
    main()
