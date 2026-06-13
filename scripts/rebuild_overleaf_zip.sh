#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAPER="$ROOT/paper"
DIST="$ROOT/dist"
TMP="${TMPDIR:-/tmp}/odd_carrier_holonomy_zip"

ZIP_NAME="Odd_Carrier_Holonomy_and_Metric_Compression_in_a_Finite_Signed_Carrier_Graph_v0.1.1.zip"
ZIP_PATH="$DIST/$ZIP_NAME"

echo "== rebuild Overleaf zip =="
echo "root: $ROOT"

if [ ! -f "$PAPER/main.tex" ]; then
  echo "ERROR: missing paper/main.tex"
  exit 1
fi

if [ ! -d "$PAPER/sections" ]; then
  echo "ERROR: missing paper/sections"
  exit 1
fi

rm -rf "$TMP"
mkdir -p "$TMP"
mkdir -p "$DIST"

cp -R "$PAPER"/* "$TMP"/

rm -f "$ZIP_PATH"

(
  cd "$TMP"
  zip -r "$ZIP_PATH" .
)

echo
echo "== zip written =="
ls -lh "$ZIP_PATH"

echo
echo "== zip contents =="
unzip -l "$ZIP_PATH" | sed -n '1,180p'

echo
echo "== done =="
echo "$ZIP_PATH"
