#!/bin/sh
# Build every harmonised book into the repo and refresh the index.
set -e
W=$(cd "$(dirname "$0")" && pwd); R=$(cd "$W/../../.." && pwd)/docs/olp-vethozaveta
B=$(for d in "$W"/out/*/; do [ -f "$d/_harmonized" ] && basename "$d"; done; true)
python3 "$W/build.py" "$R/kanon/data" $B
python3 "$W/update_index.py" "$R"
