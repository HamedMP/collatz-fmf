#!/usr/bin/env bash
set -euo pipefail

mode="${1:-quick}"

run() {
  printf '\n==> %s\n' "$*"
  "$@"
}

usage() {
  cat <<'USAGE'
Usage: scripts/verify_snapshot.sh [quick|full]

quick  Runs the core algebra/reduction checks and compiles the paper.
full   Runs the longer verifier snapshot recorded in proof-obligations.md.

Neither mode proves the Collatz conjecture. These commands verify the current
paper's algebraic reductions, density normalizations, finite certificates, and
diagnostic frontiers only.
USAGE
}

if [[ "$mode" != "quick" && "$mode" != "full" ]]; then
  usage
  exit 2
fi

run typst compile paper/main.typ site/paper/collatz-fmf.pdf

if command -v pdftotext >/dev/null 2>&1; then
  run pdftotext site/paper/collatz-fmf.pdf /tmp/collatz-fmf.txt
  paper_patterns=(
    "Main Results and Logical Dependencies"
    "^2\\. FMF Formulas and the Hop Map"
    "^5\\. The Quartering Law"
    "^6\\. What This Does and Does Not Prove"
    "^8\\. Future Directions"
    "Theorem 5\\.9 \\(The Quartering Law\\)"
    "Proposition 5\\.52 \\(Binary Return Weighted Expansion-Shell Count\\)"
  )
  if command -v rg >/dev/null 2>&1; then
    for pattern in "${paper_patterns[@]}"; do
      run rg -n "$pattern" /tmp/collatz-fmf.txt
    done
  else
    for pattern in "${paper_patterns[@]}"; do
      run grep -nE "$pattern" /tmp/collatz-fmf.txt
    done
  fi
else
  printf '\n==> skipping pdftotext check; pdftotext is not installed\n'
fi

run python3 explorations/explore52_binary_partial_map.py
run python3 explorations/explore60_backward_branches.py
run python3 explorations/explore64_terminal_ranks.py
run python3 explorations/explore66_terminal_zero_digits.py
run python3 explorations/explore68_periodic_branches.py
run python3 explorations/explore69_window_shells.py
run python3 explorations/explore70_bounded_alphabet_minima.py
run python3 explorations/explore71_aperiodic_templates.py --length 1024
run python3 explorations/explore73_balanced_frontier.py
run python3 explorations/explore74_mechanical_landing.py
run python3 explorations/explore75_mechanical_recurrence.py
run python3 explorations/explore76_template_recurrence.py
run python3 explorations/explore77_uniform_morphism_recurrence.py
run python3 explorations/explore78_uniform_morphism_symbolic_witness.py
run python3 explorations/explore79_q9_boundary.py
run git diff --check

if [[ "$mode" == "quick" ]]; then
  printf '\nQuick verification snapshot completed.\n'
  exit 0
fi

run python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 18
run python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 19
run python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 20
run python3 explorations/explore70_bounded_alphabet_minima.py --profile-ones 21
run python3 explorations/explore77_uniform_morphism_recurrence.py --q 4 --max-power 4 --search-factor 16
run python3 explorations/explore77_uniform_morphism_recurrence.py --q 5 --max-power 4 --search-factor 16
run python3 explorations/explore77_uniform_morphism_recurrence.py --q 6 --max-power 3 --search-factor 16
run python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 7 --search-length 8192
run python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 8 --search-length 8192
run python3 explorations/explore78_uniform_morphism_symbolic_witness.py --q 9 --max-prefix-symbols 18 --search-length 40000
run python3 explorations/explore72_bounded_alphabet_beam.py --max-length 120 --beam-width 2000 --report-every 20

printf '\nFull verification snapshot completed.\n'
