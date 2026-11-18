import CollatzFMF.Barrier
import CollatzFMF.TwoBlock
import CollatzFMF.BarrierH1
import CollatzFMF.KLSound

/-! Axiom audit for the round-6 lean-gate theorems. -/

open CollatzFMF

#print axioms Barrier.run_modEq
#print axioms Barrier.run_of_modEq
#print axioms Barrier.cylinder_eq_residue_class
#print axioms Barrier.cylinder_nonempty
#print axioms Barrier.step_lt
#print axioms Barrier.step_a_growth
#print axioms Barrier.step_b_growth
#print axioms Barrier.run_growth
#print axioms Barrier.four_e_le_three_B
#print axioms Barrier.barrier_core
#print axioms Barrier.theoremA
#print axioms Barrier.theoremA_diff
#print axioms Barrier.lemmaL
#print axioms Barrier.twoBlock_arith
#print axioms Barrier.theoremB
#print axioms Barrier.theoremB_XX
#print axioms Barrier.theoremB_bound
#print axioms Barrier.no_twoBlock_hierarchy
#print axioms Barrier.returnStep_run
#print axioms Barrier.returnStep_of_run
#print axioms Barrier.H1_orbit_run_twoBlock
#print axioms Barrier.H1_orbit_twoBlock_bound
#print axioms KL.core
#print axioms KL.core_four
#print axioms KL.disjoint_S
#print axioms KL.admissible_four_mul
#print axioms KL.admissible_r2
#print axioms KL.lemmaG
#print axioms KL.theoremT
