/- Own file (audit).  Definitions copied verbatim from CollatzPositiveDensity.lean (v2.1 source),
   checked against local Lean 4.36.0 / Mathlib v4.36.0.  This checks the MEANING of the statement
   vocabulary only; it does not check Mazur's proof. -/
import Mathlib

namespace Audit

def step (n : ℕ) : ℕ := if Even n then n / 2 else 3 * n + 1

def fastConvergent (C : ℝ) (n : ℕ) : Prop :=
  0 < n ∧ ∃ k : ℕ, (k : ℝ) ≤ C * Real.log (n : ℝ) ∧ step^[k] n = 1

noncomputable def countBelow (C : ℝ) (X : ℕ) : ℕ := by
  classical
  exact Nat.count (fastConvergent C) X

-- the step is the ordinary (unaccelerated) Collatz map
example : step 7 = 22 := by decide
example : step 22 = 11 := by decide
example (n : ℕ) (h : ¬ Even n) : step n = 3 * n + 1 := by simp [step, h]
-- 0 is excluded, 1 is included (k = 0)
example (C : ℝ) : ¬ fastConvergent C 0 := fun h => (Nat.lt_irrefl 0) h.1
example (C : ℝ) : fastConvergent C 1 := ⟨Nat.one_pos, 0, by simp, rfl⟩
-- a member really reaches 1
example (C : ℝ) (n : ℕ) (h : fastConvergent C n) : ∃ k, step^[k] n = 1 := by
  obtain ⟨_, k, _, hk⟩ := h; exact ⟨k, hk⟩
-- countBelow counts n < X (strictly), so it is at most X: the claimed bound c*X <= count is a genuine density bound
example (C : ℝ) (X : ℕ) : countBelow C X ≤ X := by
  classical
  unfold countBelow
  exact Nat.count_le _
-- countBelow C X = #{n < X : fastConvergent C n}
example (C : ℝ) (X : ℕ) : countBelow C X = by classical exact ((Finset.range X).filter (fastConvergent C)).card := by
  classical
  unfold countBelow
  exact Nat.count_eq_card_filter_range _ _

end Audit
