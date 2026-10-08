#!/bin/sh
# Re-check every Lean file against the Mathlib project in ../../../../formal (Lean v4.34.1).
# usage: sh run_lean.sh /path/to/formal
FORMAL="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"; OUT="$HERE/../outputs/lean.log"; : > "$OUT"
export PATH="$HOME/.elan/bin:$PATH"
for f in E404Structure E404Block NoCancel E404Halving E404Behaviour E404Frozen SubsetSumsCD; do
  echo "=== $f.lean" >> "$OUT"
  grep -c -w -E "sorry|native_decide" "$HERE/$f.lean" | sed 's/^/occurrences of sorry|native_decide (comments included): /' >> "$OUT"
  ( cd "$FORMAL" && /usr/bin/time -p lake env lean "$HERE/$f.lean" ) >> "$OUT" 2>&1
  echo "exit=$?" >> "$OUT"
done
echo LEAN_DONE >> "$OUT"
