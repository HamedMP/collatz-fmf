import Mathlib

example (a b : ℕ) (h : a ∣ b) (hb : 0 < b) : a ≤ b := Nat.le_of_dvd hb h
