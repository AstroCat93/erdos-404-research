#!/usr/bin/env bash
# render.sh -- rebuild note.pdf and note.tex from note.md.
#   note.pdf: pandoc -> standalone HTML with MathML -> print to PDF with headless Chromium.
#   note.tex: pandoc, amsart class (not compiled here).
# Needs pandoc (3.1.3 was used) and Chromium or Chrome; set CHROME=/path/to/chrome if it is not on PATH.
set -euo pipefail
cd "$(dirname "$0")"
CHROME=${CHROME:-$(command -v chromium || command -v chromium-browser || command -v google-chrome || true)}
FROM=markdown+tex_math_dollars+lists_without_preceding_blankline
pandoc note.md -f $FROM --mathml -s --css note.css --embed-resources -o note.html
if [ -n "$CHROME" ]; then
  "$CHROME" --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer --disable-pdf-tagging \
            --print-to-pdf="$PWD/note.pdf" "file://$PWD/note.html" 2> /dev/null
else
  echo "Chromium not found: note.pdf not rebuilt (set CHROME=...)" >&2
fi
pandoc note.md -f $FROM -s -t latex -V documentclass=amsart -o note.tex
rm -f note.html
ls -l note.pdf note.tex
