import CollatzFMF.ConstOdd
import CollatzFMF.ConstRefine

/-! Axiom audit for the sharper-constants development (`ConstCount`, `ConstH`, `ConstCycle`,
`ConstOdd`, `ConstRefine`). Expected for every line: `propext`, `Classical.choice`,
`Quot.sound` only (no `sorryAx`, no `Lean.ofReduceBool`, no `Lean.trustCompiler`). -/

#print axioms CollatzFMF.Const.card_oddCount_block
#print axioms CollatzFMF.Const.card_bad_block
#print axioms CollatzFMF.Const.exact_mass
#print axioms CollatzFMF.Const.run_spec
#print axioms CollatzFMF.Const.exact_mass_run
#print axioms CollatzFMF.Const.bad_mass_tail_odd
#print axioms CollatzFMF.Const.bad_mass_split
#print axioms CollatzFMF.Const.split_step
#print axioms CollatzFMF.Const.theoremH_split
#print axioms CollatzFMF.Const.theoremH_ge
#print axioms CollatzFMF.Const.run0
#print axioms CollatzFMF.Const.run32
#print axioms CollatzFMF.Const.run71
#print axioms CollatzFMF.Const.run0_lower
#print axioms CollatzFMF.Const.run71_lower
#print axioms CollatzFMF.Const.tail300
#print axioms CollatzFMF.Const.bad_mass_0
#print axioms CollatzFMF.Const.bad_mass_32
#print axioms CollatzFMF.Const.bad_mass_71
#print axioms CollatzFMF.Const.theoremH_3134
#print axioms CollatzFMF.Const.harmonic_ge_71
#print axioms CollatzFMF.Const.harmonic_ge_32
#print axioms CollatzFMF.Const.cycle_length_above_71
#print axioms CollatzFMF.Const.cycle_ratio_above_71
#print axioms CollatzFMF.Const.residue_bound_1045
#print axioms CollatzFMF.Const.cycle_pow_bounds_1045
#print axioms CollatzFMF.Const.residue_above_71
#print axioms CollatzFMF.Const.small_part
#print axioms CollatzFMF.Const.residue_split
#print axioms CollatzFMF.Const.residue_split_32
#print axioms CollatzFMF.Const.card_bad_odd_block_le
#print axioms CollatzFMF.Const.exact_mass_odd_run
#print axioms CollatzFMF.Const.runOdd32
#print axioms CollatzFMF.Const.runOdd32_lower
#print axioms CollatzFMF.Const.bad_mass_odd_32
#print axioms CollatzFMF.Const.residue_split_odd
#print axioms CollatzFMF.Const.residue_split_32_odd
#print axioms CollatzFMF.Const.inv_le_chunkH
#print axioms CollatzFMF.Const.chunk_block
#print axioms CollatzFMF.Const.exact_mass_chunk_run
#print axioms CollatzFMF.Const.runC0
#print axioms CollatzFMF.Const.runC0_lower
#print axioms CollatzFMF.Const.bad_mass_0_refined
#print axioms CollatzFMF.Const.theoremH_2793
#print axioms CollatzFMF.Const.residue_bound_931
