import CollatzFMF.HarmonicSharp
import CollatzFMF.ResidueProduct
import CollatzFMF.SojournCount

/-!
# Axiom audit for the lean-sharp modules

Expected output for every line: `[propext, Classical.choice, Quot.sound]` (or a subset).
-/

open CollatzFMF

#print axioms HarmonicSharp.bad_mass_odd
#print axioms HarmonicSharp.theoremH_162
#print axioms Sharp.product_identity_iterate
#print axioms Sharp.product_identity
#print axioms Sharp.residue_bound_of_sum
#print axioms Sharp.residue_bound
#print axioms Sharp.cycle_injective
#print axioms Sharp.cycle_bounds_of_sum
#print axioms Sharp.cycle_pow_bounds
#print axioms Sharp.cycle_sharp
#print axioms Sharp.cycle_sharp_of_sum_le_two
#print axioms Sojourn.landing
#print axioms Sojourn.class_card_le
#print axioms Sojourn.sojourn_abstract
#print axioms Sojourn.sojourn_39_20
#print axioms Sojourn.sojourn_sharp
