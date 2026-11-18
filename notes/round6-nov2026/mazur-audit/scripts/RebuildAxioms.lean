import CollatzPositiveDensity

open CollatzPositiveDensity

#check @CollatzPositiveDensity.positive_density
#print CollatzPositiveDensity.positive_density
#print CollatzPositiveDensity.step
#print CollatzPositiveDensity.fastConvergent
#print CollatzPositiveDensity.countBelow
#print CollatzPositiveDensity.densityConstant
#print CollatzPositiveDensity.cutoff
#check @CollatzPositiveDensity.densityConstant_pos
#check @CollatzPositiveDensity.cutoff_pos

#print axioms CollatzPositiveDensity.positive_density
#print axioms CollatzPositiveDensity.densityConstant_pos
#print axioms CollatzPositiveDensity.cutoff_pos
#print axioms CollatzPositiveDensity.positive_density_ten48

-- independently written restatement (own vocabulary, Mathlib only), proved from the built theorem
theorem rebuild_restatement :
    ∃ c : ℝ, 0 < c ∧ ∃ X₀ : ℕ, ∀ X : ℕ, X₀ ≤ X →
      c * X ≤ ((@Nat.count (fun n : ℕ => 0 < n ∧ ∃ k : ℕ, (k : ℝ) ≤ (523 / 50 : ℝ) * Real.log (n : ℝ) ∧
        (fun m : ℕ => if m % 2 = 0 then m / 2 else 3 * m + 1)^[k] n = 1)
        (Classical.decPred _) X : ℕ) : ℝ) := by
  refine ⟨(densityConstant : ℝ), by exact_mod_cast densityConstant_pos, cutoff, fun X hX => ?_⟩
  have h := positive_density X hX
  have hstep : (fun m : ℕ => if m % 2 = 0 then m / 2 else 3 * m + 1) = step := by
    funext m
    simp [step, Nat.even_iff]
  rw [hstep]
  convert h using 3

#print axioms rebuild_restatement
