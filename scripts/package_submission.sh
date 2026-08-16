#!/usr/bin/env bash
set -euo pipefail

mode="${1:-quick}"
out_dir="${2:-dist}"

usage() {
  cat <<'USAGE'
Usage: scripts/package_submission.sh [quick|full|skip-verify] [output-dir]

Builds a reproducible submission bundle for the FMF density-and-reduction
manuscript. This packages the PDF, Typst sources, verification scripts,
diagnostics, and claim-boundary notes, then smoke-tests representative
diagnostics from the archived copy. It does not certify a proof of the Collatz
conjecture.
USAGE
}

case "$mode" in
  quick|full)
    bash scripts/verify_snapshot.sh "$mode"
    ;;
  skip-verify)
    typst compile paper/main.typ site/paper/collatz-fmf.pdf
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage
    exit 2
    ;;
esac

root="$(git rev-parse --show-toplevel)"
cd "$root"

stamp="$(date -u +%Y%m%d)"
commit="$(git rev-parse --short HEAD)"
name="collatz-fmf-submission-${stamp}-${commit}"
tmp_dir="$(mktemp -d)"
pkg_dir="${tmp_dir}/${name}"
archive="${out_dir}/${name}.tar.gz"
checksum="${archive}.sha256"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

copy_file() {
  local src="$1"
  local dst="${pkg_dir}/${src}"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
}

smoke_archive() {
  local smoke_dir="${tmp_dir}/archive-smoke"
  mkdir -p "$smoke_dir"
  tar -C "$smoke_dir" -xzf "$archive"

  (
    cd "${smoke_dir}/${name}"
    python3 scripts/check_site_links.py >/dev/null
    python3 explorations/explore62_terminal_windows.py >/dev/null
    python3 explorations/explore55_height_survival.py --return-max-bits 16 --gap-max-bits 16 >/dev/null
    python3 explorations/explore56_counting_discrepancy.py >/dev/null
    python3 explorations/explore57_start_counts.py >/dev/null
    python3 explorations/explore58_critical_discrepancy.py >/dev/null
    python3 explorations/explore59_critical_clusters.py >/dev/null
    python3 explorations/explore75_mechanical_recurrence.py --length 16 --search-factor 8 >/dev/null
    python3 explorations/explore76_template_recurrence.py --length 16 --search-factor 8 >/dev/null
    python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 2 --max-prefix-symbols 2 --search-length 128 >/dev/null
    python3 explorations/explore81_rank_bound_frontier.py --bits 24 >/dev/null
  )
}

mkdir -p "$pkg_dir" "$out_dir"

top_level_files=(
  README.md
  LICENSE
  CITATION.cff
  diagnostics.md
  lemma-roadmap.md
  proof-obligations.md
  publication-readiness.md
  referee-brief.md
  review.md
  submission-checklist.md
)

for file in "${top_level_files[@]}"; do
  copy_file "$file"
done

copy_file paper/main.typ
copy_file paper/refs.bib
for file in paper/lib/*.typ paper/sections/*.typ; do
  copy_file "$file"
done

copy_file scripts/verify_snapshot.sh
copy_file scripts/package_submission.sh
copy_file scripts/check_site_links.py

for file in explorations/explore51_binary_return_code.py \
  explorations/explore52_binary_partial_map.py \
  explorations/explore53_gap_minima.py \
  explorations/explore54_return_minima.py \
  explorations/explore55_height_survival.py \
  explorations/explore56_counting_discrepancy.py \
  explorations/explore57_start_counts.py \
  explorations/explore58_critical_discrepancy.py \
  explorations/explore59_critical_clusters.py \
  explorations/explore60_backward_branches.py \
  explorations/explore62_terminal_windows.py \
  explorations/explore64_terminal_ranks.py \
  explorations/explore66_terminal_zero_digits.py \
  explorations/explore68_periodic_branches.py \
  explorations/explore69_window_shells.py \
  explorations/explore70_bounded_alphabet_minima.py \
  explorations/explore71_aperiodic_templates.py \
  explorations/explore72_bounded_alphabet_beam.py \
  explorations/explore73_balanced_frontier.py \
  explorations/explore74_mechanical_landing.py \
  explorations/explore75_mechanical_recurrence.py \
  explorations/explore76_template_recurrence.py \
  explorations/explore77_uniform_morphism_recurrence.py \
  explorations/explore78_uniform_morphism_symbolic_witness.py \
  explorations/explore79_q9_boundary.py \
  explorations/explore80_q9_boundary_residues.py \
  explorations/explore81_rank_bound_frontier.py; do
  copy_file "$file"
done

for file in site/*.html site/style.css site/favicon.svg; do
  copy_file "$file"
done
copy_file site/paper/collatz-fmf.pdf

{
  printf 'FMF Collatz density-and-reduction submission bundle\n'
  printf 'Bundle: %s\n' "$name"
  printf 'UTC date: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'Git commit: %s\n' "$(git rev-parse HEAD)"
  printf '\nThis archive does not claim a proof of the Collatz conjecture.\n'
  printf 'See proof-obligations.md and submission-checklist.md for the current claim boundary.\n'
  printf '\nIncluded files:\n'
  find "$pkg_dir" -type f | sed "s#^${pkg_dir}/##" | LC_ALL=C sort
} > "${pkg_dir}/MANIFEST.txt"

tar -C "$tmp_dir" -czf "$archive" "$name"
shasum -a 256 "$archive" > "$checksum"
smoke_archive

printf 'Created %s\n' "$archive"
printf 'Created %s\n' "$checksum"
printf 'Archive smoke test completed\n'
