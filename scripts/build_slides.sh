#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-}"; shift || true
SCENES_FILE="scenes.list"
SITE="site"z
PYTHONPATH_IN="."
MANIM_FLAGS=""
# For a single self-contained HTML use --one-file; drop it to get an assets folder.
SLIDES_FLAGS="--offline --one-file"

# --- Quick reference -------------------------------------------------------
#  Local full deck (4K renders + HTML):
#    ./scripts/build_slides.sh all --scenes-file scenes.list --site site --pythonpath .
#
#  Faster local iteration (720p renders only):
#    MANIM_RENDER_RES=1280,720 ./scripts/build_slides.sh render
#    MANIM_RENDER_RES=1920,1080 ./scripts/build_slides.sh render
#
#  HTML-only rebuild (assumes scenes already rendered):
#    ./scripts/build_slides.sh html
#
#  PDF export (uses existing renders; no extra resolution flags needed):
#    ./scripts/build_slides.sh pdf
#
#  On CI we automatically downgrade to 1280x720. Override via:
#    CI_RENDER_RES=1920,1080 ./scripts/build_slides.sh all
#    CI_RENDER_RES=1920,1080 ./scripts/build_slides.sh all --scenes-file scenes.list --site site --pythonpath 
# ---------------------------------------------------------------------------

# Default to 4K locally, but scale down automatically on CI to keep runtimes sane.
RENDER_RES="${MANIM_RENDER_RES:-3840,2160}"
if [[ "${CI:-}" == "true" ]]; then
  RENDER_RES="${CI_RENDER_RES:-1280,720}"
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scenes-file) SCENES_FILE="$2"; shift 2 ;;
    --site)        SITE="$2"; shift 2 ;;
    --pythonpath)  PYTHONPATH_IN="$2"; shift 2 ;;
    --manim-flags) MANIM_FLAGS="$2"; shift 2 ;;
    --slides-flags) SLIDES_FLAGS="$2"; shift 2 ;;
    --render-res)
      RENDER_RES="$2"
      shift 2
      ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

[[ -n "${MODE}" ]] || { echo "MODE required: render|html|all" >&2; exit 2; }
[[ -f "$SCENES_FILE" ]] || { echo "No $SCENES_FILE" >&2; exit 2; }
mkdir -p "$SITE"

export PYTHONPATH="${PYTHONPATH_IN}${PYTHONPATH:+:${PYTHONPATH}}"

# render() {
#   while read -r file scene || [[ -n "${file:-}${scene:-}" ]]; do
#     [[ -z "${file:-}" || "${file:0:1}" == "#" ]] && continue
#     echo "Render: $file $scene"
#     PYTHONPATH="$PYTHONPATH" manim $MANIM_FLAGS "$file" "$scene"
#   done < "$SCENES_FILE"
# }

render() {
  local res_args=()
  if [[ -n "${RENDER_RES:-}" ]]; then
    res_args=(-r "$RENDER_RES")
  fi

  while read -r file scene || [[ -n "${file:-}${scene:-}" ]]; do
    [[ -z "${file:-}" || "${file:0:1}" == "#" ]] && continue
    echo "Render (${RENDER_RES:-default}): $file $scene"
    local cmd=(manim "${res_args[@]}")
    if [[ -n "${MANIM_FLAGS:-}" ]]; then
      # shellcheck disable=SC2206
      cmd+=($MANIM_FLAGS)
    fi
    cmd+=("$file" "$scene")
    PYTHONPATH="$PYTHONPATH" "${cmd[@]}"
  done < "$SCENES_FILE"
}

html() {
  mapfile -t scenes < <(awk '!/^#/ && NF{print $2}' "$SCENES_FILE")
  echo "HTML (combined): ${scenes[*]} -> $SITE/index.html"
  PYTHONPATH="$PYTHONPATH" manim-slides convert $SLIDES_FLAGS "${scenes[@]}" "$SITE/index.html"
  sed -i 's|<title>.*</title>|<title>MS-DIS Slides</title>|' "$SITE/index.html"
}

# pdf() {
#   mapfile -t scenes < <(awk '!/^#/ && NF{print $2}' "$SCENES_FILE")
#   echo "PDF (combined): ${scenes[*]} -> $SITE/slides.pdf"
#   PYTHONPATH="$PYTHONPATH" manim-slides convert $SLIDES_FLAGS "${scenes[@]}" "$SITE/slides.pdf"
# }

pdf() {
  mapfile -t scenes < <(awk '!/^#/ && NF{print $2}' "$SCENES_FILE")
  echo "PDF (combined, ${PDF_RES:-default}): ${scenes[*]} -> $SITE/slides.pdf"
  local cmd=(manim-slides convert)
  if [[ -n "${PDF_RES:-}" ]]; then
    cmd+=(-r "$PDF_RES")
  fi
  if [[ -n "${SLIDES_FLAGS:-}" ]]; then
    # shellcheck disable=SC2206
    cmd+=($SLIDES_FLAGS)
  fi
  cmd+=("${scenes[@]}" "$SITE/slides.pdf")
  PYTHONPATH="$PYTHONPATH" "${cmd[@]}"
}



case "$MODE" in
  render) render ;;
  html)   html ;;
  pdf)    pdf ;;
  all)    render; html ;;
  *) echo "Unknown MODE: $MODE" >&2; exit 2 ;;
esac
