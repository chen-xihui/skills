#!/usr/bin/env bash
# Copy repository skills/ into agent-specific discovery directories (no symlinks).
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-skills.sh <target> [options]

Targets:
  cursor    Copy to .cursor/skills/          (Cursor Agent)
  qoder     Copy to .qoder/skills/           (Qoder IDE / CLI, project-level)
  trae      Copy to .trae/skills/            (TRAE Agent)
  all       Install cursor + qoder + trae (three separate copies)

Options:
  --project-dir <path>   Project root (default: repository root)
  --global               Qoder user-level only: copy to ~/.qoder/skills/
  -h, --help             Show this help

Examples:
  ./scripts/install-skills.sh cursor
  ./scripts/install-skills.sh qoder --project-dir /path/to/app
  ./scripts/install-skills.sh trae
  ./scripts/install-skills.sh all
  ./scripts/install-skills.sh qoder --global

Source of truth: <project-dir>/skills/ (this repository layout).
EOF
}

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_DIR="${ROOT}"
TARGET=""
GLOBAL=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    cursor|qoder|trae|all) TARGET="$1"; shift ;;
    --project-dir) PROJECT_DIR="$(cd "$2" && pwd)"; shift 2 ;;
    --global) GLOBAL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "${TARGET}" ]]; then
  echo "error: missing target (cursor|qoder|trae|all)" >&2
  usage >&2
  exit 1
fi

SRC="${PROJECT_DIR}/skills"
if [[ ! -d "${SRC}" ]]; then
  echo "error: source not found: ${SRC}" >&2
  echo "hint: run from the middleware-skills repo or pass --project-dir" >&2
  exit 1
fi

copy_skills() {
  local dest="$1"
  local label="$2"

  if [[ -L "${dest}" ]]; then
    echo "  remove old symlink: ${dest}"
    rm "${dest}"
  fi

  mkdir -p "$(dirname "${dest}")"
  rm -rf "${dest}"
  mkdir -p "${dest}"

  if command -v rsync >/dev/null 2>&1; then
    rsync -a "${SRC}/" "${dest}/"
  else
    cp -R "${SRC}/." "${dest}/"
  fi

  echo "  OK ${label}: ${dest}/  (copied from ${SRC}/)"
}

install_cursor() {
  echo "[cursor]"
  copy_skills "${PROJECT_DIR}/.cursor/skills" "Cursor (.cursor/skills)"
  local cursor_src="${ROOT}/integrations/cursor"
  if [[ -d "${cursor_src}" ]]; then
    mkdir -p "${PROJECT_DIR}/.cursor"
    if [[ -f "${cursor_src}/hooks.json" ]]; then
      cp "${cursor_src}/hooks.json" "${PROJECT_DIR}/.cursor/hooks.json"
      echo "  OK Cursor hooks: .cursor/hooks.json"
    fi
    if [[ -d "${cursor_src}/commands" ]]; then
      rm -rf "${PROJECT_DIR}/.cursor/commands"
      mkdir -p "${PROJECT_DIR}/.cursor/commands"
      cp -R "${cursor_src}/commands/." "${PROJECT_DIR}/.cursor/commands/"
      echo "  OK Cursor commands: .cursor/commands/"
    fi
  fi
}

install_qoder_project() {
  echo "[qoder project]"
  copy_skills "${PROJECT_DIR}/.qoder/skills" "Qoder (.qoder/skills)"
}

install_qoder_global() {
  echo "[qoder global]"
  local home_skills="${HOME}/.qoder/skills"
  copy_skills "${home_skills}" "Qoder (~/.qoder/skills)"
}

install_trae() {
  echo "[trae]"
  copy_skills "${PROJECT_DIR}/.trae/skills" "TRAE (.trae/skills)"
}

echo "Installing middleware skills (copy mode)"
echo "  project-dir: ${PROJECT_DIR}"
echo "  source:      ${SRC}/"
echo ""

case "${TARGET}" in
  cursor)
    install_cursor
    ;;
  qoder)
    if [[ "${GLOBAL}" -eq 1 ]]; then
      install_qoder_global
    else
      install_qoder_project
    fi
    ;;
  trae)
    install_trae
    ;;
  all)
    install_cursor
    install_qoder_project
    install_trae
    ;;
esac

echo ""
echo "Done. Edit files under ${SRC}/ then re-run this script to refresh copies."
