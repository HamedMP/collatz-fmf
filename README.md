# Elementary Exponential Density Bounds for Collatz Growth Chains

Via First-Multiple-of-Four (FMF) decomposition.

## Key Results

- **Theorem A (FMF Step Formula):** Exact algebraic formulas for hop length and output value
- **Theorem B (State Independence):** Hop output distributions are state-independent via 2-adic inverse structure
- **Theorem C (Spectral Contraction):** rho = 0.8638 < 1 from exact 2-adic formulas
- **Theorem D (Quartering Law):** Growth chain continuation probability = 1/4 exactly, giving (1/4)^k density decay
- **Main Theorem:** Natural-density bounds strictly stronger than Tao's logarithmic-density result, with exponential rather than sub-polynomial decay, via elementary mod-8 arithmetic

## Honest Assessment

The "almost all to all" gap remains open. The exceptional set is provably infinite. This is a frontier problem in p-adic dynamics.

## Structure

```
paper/          Typst source for the paper
site/           GitHub Pages website
explorations/   44 Python exploration scripts
```

## Building

```bash
typst compile paper/main.typ site/paper/collatz-fmf.pdf
```

## License

CC BY 4.0
