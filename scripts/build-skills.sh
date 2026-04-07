#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
DIST_DIR="${REPO_ROOT}/dist/skills"
SKILL_INDEX=$(mktemp)
trap 'rm -f "$SKILL_INDEX"' EXIT

usage() {
  echo "Usage: $(basename "$0") [--all | --list | skill-name ...]"
  echo
  echo "Build skill zips for Claude Desktop."
  echo
  echo "  --all          Build all skills"
  echo "  --list         List available skills"
  echo "  skill-name     Build specific skill(s) by name"
  echo "  (no args)      Build only skills changed since last commit"
  exit 0
}

mkdir -p "$DIST_DIR"

# Build index: each line is "name<TAB>package_root"
(cd "$REPO_ROOT" && find skills -name "SKILL.md" -type f | sort) | while IFS= read -r skill_md; do
  skill_dir=$(dirname "$skill_md")

  # Walk up to find package root (directory with README.md)
  pkg_root="$skill_dir"
  while [ "$pkg_root" != "skills" ] && [ ! -f "${REPO_ROOT}/${pkg_root}/README.md" ]; do
    pkg_root=$(dirname "$pkg_root")
  done
  if [ "$pkg_root" = "skills" ]; then
    pkg_root="$skill_dir"
  fi

  name=$(basename "$pkg_root")
  echo "${name}	${pkg_root}"
done | sort -u > "$SKILL_INDEX"

lookup_skill() {
  grep "^${1}	" "$SKILL_INDEX" | cut -f2
}

all_names() {
  cut -f1 "$SKILL_INDEX"
}

# Determine which skills to build
build_names=""

if [ $# -eq 0 ]; then
  # Build changed skills only
  changed=$(cd "$REPO_ROOT" && git diff --name-only HEAD -- skills/ 2>/dev/null || true)
  if [ -z "$changed" ]; then
    changed=$(cd "$REPO_ROOT" && git diff --name-only HEAD~1 HEAD -- skills/ 2>/dev/null || true)
  fi
  if [ -z "$changed" ]; then
    echo "No skill changes detected. Use --all to build everything."
    exit 0
  fi
  while IFS=$'\t' read -r name pkg_root; do
    if echo "$changed" | grep -q "^${pkg_root}/"; then
      build_names="${build_names}${name}"$'\n'
    fi
  done < "$SKILL_INDEX"
  build_names=$(echo "$build_names" | sed '/^$/d')
  if [ -z "$build_names" ]; then
    echo "No skill changes detected. Use --all to build everything."
    exit 0
  fi
elif [ "$1" = "--all" ]; then
  build_names=$(all_names)
elif [ "$1" = "--list" ]; then
  echo "Available skills:"
  while IFS=$'\t' read -r name pkg_root; do
    echo "  ${name}  (${pkg_root})"
  done < "$SKILL_INDEX"
  exit 0
elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  usage
else
  for name in "$@"; do
    pkg_root=$(lookup_skill "$name")
    if [ -z "$pkg_root" ]; then
      echo "Unknown skill: ${name}"
      echo "Available:"
      all_names | sed 's/^/  /'
      exit 1
    fi
    build_names="${build_names}${name}"$'\n'
  done
  build_names=$(echo "$build_names" | sed '/^$/d')
fi

count=$(echo "$build_names" | wc -l | tr -d ' ')
echo "Building ${count} skill(s)..."
echo

echo "$build_names" | while IFS= read -r name; do
  pkg_root=$(lookup_skill "$name")
  out="${DIST_DIR}/${name}.zip"
  rm -f "$out"
  (cd "${REPO_ROOT}/${pkg_root}" && zip -r "$out" . -x "*.zip" > /dev/null)
  echo "  ${name} -> dist/skills/${name}.zip"
done

echo
echo "Done. Output in dist/skills/"
