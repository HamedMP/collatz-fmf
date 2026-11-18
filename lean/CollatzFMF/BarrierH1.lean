import CollatzFMF.TwoBlock

/-!
# Link between the two-letter map and the binary return partial map `ReturnStep` / `H1`

In the coordinate `w = 33 n + 32`, a return block of length `r` is the word `b^r a`.
Everything in this file is complete (no `sorry`, no extra axioms).
-/

namespace CollatzFMF
namespace Barrier

open Letter

/-- The return letter `r` as a word over `{a,b}`: `b^r a`. -/
def retBlock (r : ℕ) : List Letter := List.replicate r b ++ [a]

theorem B_replicate_b (r : ℕ) : B (List.replicate r b) = 4 * r := by
  induction r with
  | zero => rfl
  | succ r ih => rw [List.replicate_succ, B_cons, ih]; simp [bits]; omega

theorem B_retBlock (r : ℕ) : B (retBlock r) = 4 * r + 3 := by
  simp [retBlock, B_replicate_b, bits]

theorem retBlock_ne_nil (r : ℕ) : retBlock r ≠ [] := by simp [retBlock]

theorem run_replicate_b (r z : ℕ) : Run (List.replicate r b) (16 ^ r * z) (27 ^ r * z) := by
  induction r generalizing z with
  | zero => simp [Run]
  | succ r ih =>
    rw [List.replicate_succ]
    refine ⟨16 ^ r * (27 * z), ⟨?_, by ring⟩, ?_⟩
    · have : 16 ^ (r + 1) * z = 16 * (16 ^ r * z) := by ring
      rw [this]; exact Nat.mul_mod_right _ _
    · have h := ih (27 * z)
      have e : 27 ^ r * (27 * z) = 27 ^ (r + 1) * z := by ring
      rw [e] at h; exact h

/-- **The link.**  If `T(n) = n'` through the return gate `(r, w)`, then in the coordinate
`33 n + 32` the word `b^r a` is admissible and leads to `33 n' + 32`. -/
theorem returnStep_run {n n' : ℕ} (h : ReturnStep n n') :
    ∃ r w, ReturnGate n r w ∧ Run (retBlock r) (33 * n + 32) (33 * n' + 32) := by
  obtain ⟨r, w, ⟨h1, h2⟩, h3⟩ := h
  refine ⟨r, w, ⟨h1, h2⟩, run_append.mpr ⟨27 ^ r * w, ?_, 33 * n' + 32, ⟨?_, ?_⟩, rfl⟩⟩
  · rw [h1]; exact run_replicate_b r w
  · rw [Nat.mul_mod, pow27_mod8, h2]
    unfold epsR
    split_ifs <;> rfl
  · have : 3 * 27 ^ r * w = 3 * (27 ^ r * w) := by ring
    omega

/-- Conversely, a `b^r a` step between `33n+32` and `33n'+32` is a return step. -/
theorem returnStep_of_run {n n' r : ℕ} (h : Run (retBlock r) (33 * n + 32) (33 * n' + 32)) :
    ReturnStep n n' := by
  obtain ⟨z, hb, ha⟩ := run_append.mp h
  obtain ⟨z', ⟨-, h8⟩, rfl⟩ := ha
  -- 16^r z = 27^r (33n+32)
  have key : ∀ (r u v : ℕ), Run (List.replicate r b) u v → 16 ^ r * v = 27 ^ r * u := by
    intro r
    induction r with
    | zero => intro u v h; simp only [List.replicate_zero, Run] at h; simp [h]
    | succ r ih =>
      intro u v h
      rw [List.replicate_succ] at h
      obtain ⟨y, ⟨-, hs⟩, hr⟩ := h
      have := ih y v hr
      calc 16 ^ (r + 1) * v = 16 * (16 ^ r * v) := by ring
        _ = 27 ^ r * (16 * y) := by rw [this]; ring
        _ = 27 ^ (r + 1) * u := by rw [hs]; ring
  have hk := key r _ _ hb
  refine returnStep_of_identity (r := r) ?_
  have e1 : 88 * n' + 85 = 3 * z := by omega
  rw [e1]
  calc 16 ^ r * (3 * z) = 3 * (16 ^ r * z) := by ring
    _ = 3 * 27 ^ r * (33 * n + 32) := by rw [hk]; ring

/-- Along an `H1` orbit the word `b^(r_0) a b^(r_1) a …` is the itinerary of `33 n_0 + 32`:
orbit version for a return word taking at most two values `r0` (first) and `s`. -/
theorem H1_orbit_run_twoBlock (n : ℕ → ℕ) (hn : ∀ j, ReturnStep (n j) (n (j + 1))) (r0 s : ℕ)
    (y : ℕ → Bool)
    (hy : ∀ j, ∃ w, ReturnGate (n j) (if y j then r0 else s) w) (N : ℕ) :
    Run (blk (retBlock r0) (retBlock s) (seg y 0 N)) (33 * n 0 + 32) (33 * n N + 32) := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [seg_succ, blk_append]
    refine run_append.mpr ⟨_, ih, ?_⟩
    obtain ⟨r, w, hg, hr⟩ := returnStep_run (hn N)
    obtain ⟨w', hg'⟩ := hy N
    obtain ⟨rfl, -⟩ := returnGate_unique hg hg'
    rw [Nat.zero_add]
    cases hyN : y N <;> simp only [hyN, blk, List.append_nil] at hr ⊢ <;> simpa using hr

/-- **Corollary of Theorem B for `H1` orbits.**  If an orbit of the binary return partial map
has a return word `(r_j)` taking only two values `r0 = r_0` and `s`, then
`(33 n_0 + 33)^4 · 3^(9(4 r0 + 3)) > 2^(16(4 r0 + 3))`. -/
theorem H1_orbit_twoBlock_bound (n : ℕ → ℕ) (hn : ∀ j, ReturnStep (n j) (n (j + 1)))
    (r0 s : ℕ) (y : ℕ → Bool) (h0 : y 0 = true)
    (hy : ∀ j, ∃ w, ReturnGate (n j) (if y j then r0 else s) w) :
    2 ^ (16 * (4 * r0 + 3)) < (33 * n 0 + 33) ^ 4 * 3 ^ (9 * (4 * r0 + 3)) := by
  have h := theoremB (retBlock r0) (retBlock s) (retBlock_ne_nil _) (retBlock_ne_nil _) y h0
    (33 * n 0 + 32) (by omega) (fun N => ⟨_, H1_orbit_run_twoBlock n hn r0 s y hy N⟩)
  rw [B_retBlock] at h
  exact h

/-! ### Sanity examples (values from `Return.lean`: `T(7) = 8`, `T(48) = 92`) -/

-- r = 0, n = 7: w = 263 --a--> 296 = 33·8 + 32
example : Run (retBlock 0) (33 * 7 + 32) (33 * 8 + 32) := ⟨296, by decide, rfl⟩
-- r = 1, n = 48: w = 1616 = 16·101 --b--> 2727 --a--> 3068 = 33·92 + 32
example : Run (retBlock 1) (33 * 48 + 32) (33 * 92 + 32) :=
  ⟨2727, by decide, 3068, by decide, rfl⟩

end Barrier
end CollatzFMF
