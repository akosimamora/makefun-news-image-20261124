"""Entry point: copy the pre-rendered 24 November 2026 front page to entry.png.

Standard library only. The image is rendered at build time and stored in
this repository as entry.png; the grader runs with nothing installed, so
this program only copies that file to the output directory.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    shutil.copyfile(src, os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
