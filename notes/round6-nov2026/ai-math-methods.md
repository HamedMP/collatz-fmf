# How recent AI math results were produced (May-Nov 2026) and what it means for Collatz

Compiled 2026-11-17. Scope: methodology of AI-produced results on open problems, with emphasis on prompts, scaffolds, attempt counts and verification; then Collatz state of the art.

**Reading conventions**

- **[P]** = I fetched the primary source (paper, lab post, repository file) and the statement is taken from it.
- **[S]** = taken from a secondary source I fetched (survey, news article) describing a primary source I did not open.
- **[W]** = seen only in a web-search result summary; treat as a lead, not a fact.
- **[U]** = could not confirm.
- Quoted text in section 2 is verbatim from the fetched source at the URL given. Anything not in quotation marks is my paraphrase.
- All claims by labs about their own results are reported as claims. Most of the September-October OpenAI material is unrefereed.
- Model names (GPT-5.5 Pro, GPT 5.6 Sol, GPT-6 Astra, Claude Fable 5/5.1, Claude Mythos) are as written in the sources.

---

## 1. Table of results

| # | Problem / result | Date | System | Type | Human involvement | Verification | Source |
|---|---|---|---|---|---|---|---|
| 1 | Erdős unit distance conjecture (Erdős #90) disproved: n points with n^(1+δ) unit distances | 2026-05-20 | OpenAI internal general-purpose reasoning model | Counterexample (infinite family via number fields / class field towers) | OpenAI says autonomous, found while evaluating on "a collection of Erdős problems"; humans later digested and simplified | "checked by a group of external mathematicians"; companion paper arXiv:2605.20695; Sawin gave δ=0.014 | [P] https://openai.com/index/model-disproves-discrete-geometry-conjecture/ (read via web.archive.org) |
| 2 | Replication of #1 with a public model | PNAS, first published 2026-10-26 | GPT-5.5 Pro, three-stage pipeline "brainstorm, execute, and review" | Counterexample | None during run; web search disabled | Author check; 8/8 trials "correct or essentially correct"; avg 106.7k reasoning tokens | [P abstract only] doi:10.1073/pnas.2621541123, PMC13732072 |
| 3 | Sum-product conjecture over R false | 2026-05-27 (human paper) | Humans (Bloom, Sawin, Schildkraut, Zhelezov), "inspired by" #1 | Counterexample | Human proof | Standard | [P abstract] arXiv:2605.28781 |
| 3a | Same, by AI | June 2026 | Agent on Claude Mythos (Alpöge); GPT-5.5 Pro transcript (Alexeev/Bubeck) | Counterexample | Mythos agent non-public; the GPT transcript was given the unit-distance proof and told to reuse it (per Huang) | n/a | [S] described in arXiv:2607.20525 sec. 1 |
| 3b | Same, autonomous replication | 2026-07-09 | GPT-5.5 Pro, three-round pipeline | Counterexample | None during run; tools and web off | Author verified; 7/8 correct, 1/8 honestly reported a gap; ~132k reasoning tokens/trial | [P] arXiv:2607.20525 |
| 4 | Five Erdős problems (#960, #987, #1091, #990, #1141) | arXiv v1 2026-04-08 | "an internal model at OpenAI" | 4 constructions/counterexamples, 1 positive proof (#1141, short deduction from a theorem of Pollack) | Humans "digest the proofs and modify the write-ups"; one minor proof-level change | Human; re-ran ChatGPT-5.4 Pro 5x per problem: succeeded only on #960 (one transcript, weaker) and #1141 (5/5) | [P] arXiv:2604.06609 |
| 5 | 9 of 353 formalized Erdős statements; 44/492 OEIS conjectures | 2026-05-21 | DeepMind AlphaProof Nexus (Gemini 3.1 Pro prover subagents + Lean; optional AlphaProof + evolutionary search) | Mixed, all formal | Autonomous given Lean statement | Lean | [P] arXiv:2605.22763 |
| 6 | Cycle double cover conjecture | Lean theorem merged 2026-07-09; exposition 2026-07-17 | GPT 5.6 Sol Ultra, up to 64 concurrent agents, single prompt | Positive proof | Prompt only (released); human exposition by Oum | Lean repo (openai/cdc-lean), human exposition arXiv:2607.16356 | [P] prompt PDF; [S] the rest via arXiv:2607.07779 bibliography |
| 7 | Jacobian conjecture false in dimension 3 (explicit Keller map) | 2026-07-19/20 | Claude Fable 5 (Alpöge) | Explicit counterexample | Prompted by a mathematician; prompt not published | Trivially checkable; Isabelle/HOL AFP entry [W] | [P] mention in arXiv:2609.25050 fn. 1 and Anthropic zeta post fn. 2; details [W] |
| 8 | "Ten advances" (sphere packing bounds, non-sofic groups, Connes rigidity, Erdős #183, #146, #180, ...) | 2026-08-01 | "an internal version of Astra" | Mixed | "prepared into manuscripts by humans with the same model" | Lean certificates by the model; ~$2,000 of tokens at Sol API rates for all ten | [P] https://openai.com/index/ten-advances-in-mathematics/ (web.archive.org). Sra (arXiv:2608.29595 fn. 1) reports the Connes disproof is "allegedly" invalid |
| 9 | >= 2/3 (0.6725) of zeta zeros simple/on the critical line (previous record 5/12) | 2026-08-10 | Unreleased research Claude in Claude Code, coordinator + ~60 subagents | Positive proof by recombination (Bombieri 2000 + unconditional pair correlation) | Non-mathematician sent one-line encouragements; two Anthropic mathematicians validated; Conrey and Goldston examined | Subagent referees, blind re-derivation, literature agent; Lean passing Comparator; later independent human preprint [S] | [P] https://www.anthropic.com/research/riemann-zeta and process PDF; arXiv:2608.13637 |
| 10 | 18 refuted statements (stable polynomials, Schur positivity, matrix inequalities, ...) | 2026-08-30 | GPT Pro (chat), over 12 months | Counterexamples | One mathematician (Sra); "single-shot prompt" to "elaborate chat session"; prompts not disclosed | 16 exact rational certificates, 2 interval certificates, recomputable repo | [P] arXiv:2608.29595 |
| 11 | Fermat's Last Theorem fully formalized in Lean | 2026-09-04 | Claude (internal model "roughly comparable to Claude Fable 5.1"), dozens of agents on Prove2Me | Formalization of known theorem | "occasional high-level instructions" | Lean, three standard axioms, comparator vs Mathlib statement; 11 days, ~6B output tokens, 13M lines | [P] https://www.anthropic.com/research/formalizing-fermats-last-theorem |
| 12 | FrontierMath Erdős: #74 disproved, #126 proved (benchmark run); #1 disproved, #548 (Erdős-Sós) and #571 proved (extra runs) | 2026-09-06 | Pre-release GPT-6 Astra in Epoch's Inspect harness | 2 disproofs, 3 proofs | None (autonomous, sandboxed, no network) | Lean + Comparator | [P] arXiv:2609.25050 |
| 13 | Forced Euler blowup | 2026-09-07/08 | Alpöge and Buckmaster with an internal Anthropic model | Construction (blowup) | Year-long human-AI collaboration | Lean [S] | [S] Scientific American 2026-09-08; OpenAI NS post |
| 14 | Navier-Stokes blowup with smooth forcing (Clay statements C and D); unforced Euler blowup | 2026-09-08 | OpenAI internal model, ~10,000 concurrent agents | Construction (blowup = "disproof" side) | Humans chose problems, variants, re-prompting, cross-pollination | 166-page manuscript + Lean repo (17 h formalization by GPT-6 Astra); NPR: community believes it because the Lean compiles, but paper "not written for humans" | [P] https://openai.com/index/navier-stokes-solution/ (web.archive.org); [P] NPR 2026-09-22 |
| 15 | OpenAI mathematics collection: 721 manuscripts in 373 "result families" (claims include quasi-RH zero-free half-plane, Kakeya in dims 3-4, Hodge for CM abelian varieties, "ETH is false", Erdős-Gallai, ...) | Initial commit 2026-10-06; updates 10-07, 10-26, 10-29 | "an unnamed internal OpenAI model", "the same procedure" | Mostly stated as positive proofs; a minority are counterexamples | OpenAI selected/aggregated from ~4,000 problems posed | ~42% of top-line results Lean-formalized; 3 manuscripts withdrawn and 14 repaired on 10-07 | [P] https://github.com/openai/math (README.md, history.md, CONTENTS.md) |
| 16 | First Proof batch 2: 7 of 10 research-lemma problems got at least one passing grade | March-June 2026 | ChatGPT 5.5 Pro and three academic harnesses | Positive proofs of unpublished known results | None during runs | 30 expert referees, double-blind | [P] arXiv:2606.18119 |
| 17 | OEIS Open: 147/492 at $50/attempt | 2026-08-12 | Generic LMs with minimal tools | Formal proofs of obscure conjectures | None | Lean + Comparator | [P abstract] arXiv:2608.11941 |
| 18 | Knuth, "Claude's Cycles" (Hamiltonian decomposition for odd m) | Feb-Mar 2026 (before window) | Claude Opus 4.6, coached by F. Stappers | Construction | Coaching: summarize progress in a plan file after every run [W] | Knuth's proof; computational checks | [W] https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf (downloaded, not read) |

Not opened but relevant: First Proof batch 3 (hexagonmath.org/2610.00244v1), DeepMind Aletheia (arXiv:2602.10177, prompts repo github.com/google-deepmind/superhuman/tree/.../aletheia), Feng et al. arXiv:2601.22401 (13/700 Erdős problems "addressed", 5 novel, 8 literature finds [S]), AI co-mathematician arXiv:2605.06651 (abstract only: interactive workbench, 48% on FrontierMath Tier 4), Tao's ICM essay arXiv:2608.16753 (read; quoted below), arXiv:2608.14407 (King, survey of AI Scientists; abstract only; not about mathematics methodology).

Survey used as an index: arXiv:2607.07779 v4 (2026-11-04), sections 5.3.1-5.3.3 [P].

---

## 2. Verbatim prompts and scaffold descriptions

### 2.1 Huang's three-round, problem-agnostic pipeline (GPT-5.5 Pro) - fully disclosed

Source [P]: arXiv:2607.20525, https://arxiv.org/abs/2607.20525 ; code https://github.com/yichenhuang/sum-product (`run.py`, transcripts in `outputs/`).

System prompt:

> The provided theorem was recently proved, and the result is now accepted by the mathematical community. Your task is to independently construct a proof.

First prompt = theorem statement, a one-line remark, a separator `***`, then:

> As a first step toward a complete proof, identify the most promising approach and develop it as far as possible. Present a step-by-step proof plan. Prove any intermediate claims you can. For each remaining gap, state it precisely and assess whether it can plausibly be closed within the approach or poses a serious obstruction. Include enough detail for the next round to continue from where you leave off.

Second prompt:

> Construct a complete and rigorous proof, adapting your approach as needed.

Third prompt:

> Critically examine the proof you constructed to identify and resolve any errors or logical gaps. Then, present a complete, rigorous, step-by-step proof. Clearly justify each step with sufficient detail so that an expert can verify your reasoning without needing to fill in any gaps.

Settings (verbatim): "All trials were conducted via the GPT-5.5 Pro API using the gpt-5.5-pro-2026-04-23 snapshot. Tools and web search were disabled. The reasoning effort parameter was set to “xhigh”. The verbosity parameter was set to “high” for the first two rounds, and left at the default (medium) setting for the third round."

Author's remarks worth copying:

- The theorem is stated as true in the prompt. "If it were unknown whether the conjecture is true or false, this hint could be removed simply by instructing the agent to attempt both a proof and a disproof in separate runs, at the cost of approximately doubling the test-time compute."
- "all problem-specific text is confined to the portion of the first prompt above the separator ***."
- Results: 7/8 correct; trial 2 "did not present the incomplete argument as a finished proof". Token use by round (successful trials, mean): planning 62.5k, construction 45.3k, review 17.4k. The author's diagnostic: unusually high token use in rounds 2-3 signals that no viable plan was found in round 1.
- The seven proofs fall into two genuinely different classes (unit-based constructions vs L^p-type regions with no units), so independent trials produce diversity, not eight copies.

The same author's unit-distance paper (PNAS, doi:10.1073/pnas.2621541123) describes, per its abstract [P], "a problem-agnostic three-stage prompting pipeline: brainstorm, execute, and review", "eight independent trials with web search disabled", success in every trial, "an average of 106.7 k reasoning tokens per trial". **[U]** I could not fetch the PNAS/PMC full text (captcha), so the unit-distance prompts themselves are unconfirmed; the sum-product prompts above are the confirmed sibling.

How the non-autonomous GPT-5.5 Pro transcript worked, per Huang [S]: "A key prompt supplied the model with the unit-distance proof and explicitly instructed it to use the same approach to disprove the sum-product conjecture. This is a substantial mathematical hint." (Transcript link given there: https://chatgpt.com/share/6a187d12-7d58-83e8-87bd-0ee312378028, not opened.)

### 2.2 OpenAI's cycle-double-cover prompt (GPT 5.6 Sol Ultra, multi-agent) - full text

Source [P]: https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf . The document's abstract: "This document contains the full prompt given to GPT 5.6 Sol Ultra which led to its proof of the Cycle Double Cover Conjecture." Full prompt, verbatim:

> Current task statement
>
> A graph here is a finite loopless undirected multigraph: parallel edges are allowed and are distinct. A bridge is an edge whose deletion increases the number of connected components. A cycle is a connected 2-regular submultigraph; thus two parallel edges form a cycle of length two. A cycle double cover of G is a finite multiset of cycles of G such that every edge of G occurs in exactly two members of the multiset, counted with multiplicity.
>
> Resolve the Cycle Double Cover Conjecture completely:
>
> Every finite bridgeless loopless multigraph has a cycle double cover.
>
> Disconnected graphs are permitted, and the edgeless graph has the empty cycle double cover. Cycles in the cover need not be induced or edge-disjoint from one another; the requirement is exactly two total occurrences of each edge.
>
> Assume for purposes of this task that a complete affirmative proof exists. A complete solution must prove exactly the following:
>
> Every finite loopless multigraph with no bridge possesses a cycle double cover, without additional assumptions such as cubicity, planarity, connectivity, or higher edge-connectivity.
>
> Partial progress does not count unless it implies exactly the resolution above. In particular, proofs for special graph classes, constructions of cycle covers with some edges covered other than twice, bounded-length or prescribed-cycle variants, reductions to another unproved conjecture, computational verification through any fixed graph size, and candidate counterexamples without a complete nonexistence certificate are insufficient.
>
> Use multiagent v2 aggressively and dynamically. You have up to 64 concurrent agents available. Do not use a fixed assignment such as “N agents for strategy X.” Instead, manage the search using the following heuristics:
>
> - Begin with a genuinely diverse portfolio of approaches. Agents should explore substantially different formulations, invariants, reductions, algebraic viewpoints, structural inductions, decompositions, flow formulations, transition systems, embeddings, extremal arguments, and computational sanity checks.
>
> - Do not tell most agents the currently favored approach. Preserve independence during early rounds so that agents do not all converge to the same attractive but incomplete reduction.
>
> - Maintain an explicit registry of approach families. Group agents by the mathematical idea they are using, not by superficial wording. If many agents converge to one family, redirect some of them toward underexplored formulations.
>
> - Do not allow one approach to dominate merely because it gives elegant reductions. A route that ends at a lemma equivalent in strength to the original conjecture is not close to completion unless it supplies a genuinely new proof of that lemma.
>
> - When an approach stalls at a theorem-strength missing lemma, mark that route as blocked. Only continue assigning agents to it if someone proposes a materially new mechanism, invariant, or construction.
>
> - Keep several incompatible proof routes alive through multiple rounds. Cross-pollinate ideas only after independent agents have developed them far enough to expose their real strengths and gaps.
>
> - Use adversarial agents throughout: every candidate proof must be checked for exact-two multiplicity, repeated-edge closed trails masquerading as cycles, parallel-edge 2-cycles, disconnected graphs, cutvertices, bridges introduced by reductions, and circular use of an equivalent CDC statement.
>
> - Require agents to return concrete lemmas, constructions, equations, or counterexamples to proposed sublemmas. Reject status reports, vague optimism, and claims that an unproved global compatibility statement is “routine.”
>
> - The root agent should repeatedly synthesize, challenge, redirect, and launch new rounds. Do not stop after the first wave fails. Produce a complete proof if one survives audit; otherwise report only the strongest rigorously proved derivation and its exact remaining gap.
>
> Do not return merely because current approaches fail or agents report theorem-strength gaps. Continue launching new rounds, reopening blocked approaches only when there is a genuinely new mechanism, and searching for fresh formulations.
>
> Return only when a complete affirmative proof has been found and survives adversarial audit. Do not return a reduction, partial result, isolated missing lemma, “best effort” summary, or explanation of why the problem is difficult.
>
> Spend at least 8 hours on this before even thinking of returning or giving up.
>
> Public search may be used only for ordinary mathematical background or standard named theorems, not to search for a solution to this exact conjecture or benchmark. Do not search the public web merely to determine whether CDC is open, and do not answer that it is open.

Structure to copy: (i) exact statement with all edge-case conventions pinned down; (ii) "assume a proof exists"; (iii) an explicit list of what does not count; (iv) orchestration heuristics; (v) a named list of problem-specific failure patterns for adversarial agents; (vi) minimum time; (vii) ban on searching for the answer or for the problem's status.

Caveat: this prompt asserts the answer. For an open problem of unknown truth value that is a gamble; OpenAI's Navier-Stokes run and Huang both recommend running each direction separately (2.3, 2.1).

### 2.3 OpenAI Navier-Stokes: scaffold description (no prompts published)

Source [P]: https://openai.com/index/navier-stokes-solution/ (direct fetch returns 403; read from https://web.archive.org/web/2026/https://openai.com/index/navier-stokes-solution/ , snapshot 2026-11-16). Verbatim:

> We used a system of coordinating agents powered by our internal model. The agents had access to tools such as the ability to read from a cached version of the internet and the ability to run code. Agents were subdivided into groups with the ability to communicate within the group. The groups varied in size, and the group that produced the Navier–Stokes resolution involved on the order of 10,000 concurrent agents.

> For each problem, we prompted different groups of agents with different variants of the problem statement, covering all variants of the problem. For the Navier–Stokes problem, we suggested versions “A” and “B” (particular forms of the Navier–Stokes problem which would result in a proof) and versions “C” and “D” (which would result in a disproof) to separate groups of agents.

> In addition to the full Millennium Prize problems, we asked our multiagent system to try a set of “easier” problems. One of these problems was a similar blowup question for the limit of the Navier–Stokes problem with the viscosity term removed. [...] Nearly 100 agents worked together for approximately 50 hours to produce our Euler regularity disproof.

> Once we saw the Euler solution, we thought that Navier–Stokes was the most promising problem to work on. Thus, we decided to devote our resources to Navier–Stokes. To do so, we shifted agents away from the other Millennium Problems and prompted these agents with the Euler resolution.

> We encouraged different groups of agents to explore a diversity of approaches. After some time, we cross-pollinated the agent groups by using Codex to consolidate the most useful insights from each agent group. These follow-up prompts drew on the agents’ own intermediate results. The group that found the solution to Navier–Stokes was guided in such a way.

> The agents arrived at their resolution on Saturday, September 5, about 88 hours after the first agents were launched. Lean formalization and verification took an additional 17 hours via GPT‑6 Astra.

> Across all attempted problems, the agents sent 4.9 million messages and used about 300 billion output tokens. In the process of resolving the Navier–Stokes problem, the agents sent 2.7 million messages and used approximately 130 billion output tokens.

Also stated there: the model is "significantly more capable than GPT‑6 Astra"; it was evaluated "on all open Millennium Prize problems and a few other high-impact problems" - so the denominator includes the other Millennium problems, which did not fall in this run.

News-level context [P for the articles, claims are theirs]: NPR (2026-09-22, https://www.npr.org/2026/09/22/nx-s1-5968588/openai-navier-stokes-problem-mathematicians-learn-little) estimates $6-10M for the NS run and $15-20M overall at public-model prices; quotes Maynard: "So far it's been very difficult to really extract any human understanding from this new AI proof", Gómez-Serrano: "The paper is not written for humans"; says the Lean code "did compile as expected" and that on that basis "the community seems to have the consensus that it is correct." Scientific American (2026-09-08, "AI may have just solved a million-dollar math problem. The field will never be the same") covers the credit dispute with Buckmaster/Alpöge and notes the forcing-term "loophole". **[U]** I did not find a Scientific American article titled "The inside story behind OpenAI's million-dollar math proof".

### 2.4 OpenAI mathematics collection ("300+" lead)

Source [P]: https://github.com/openai/math README.md (main branch, fetched 2026-11-17). Verbatim:

> The vast majority of results were obtained with the same procedure using an unreleased internal OpenAI model. On average, each result used three hours of ChatGPT Pro thinking compute with that model. Over the course of the evaluation, the model was posed approximately 4,000 problems. Aggregating the output into result families and manuscripts and requiring an appropriate level of significance led to the catalog outlined above.

> Exceptions to this fixed procedure include work on a zero-free region for the Riemann zeta function and proof of the Hodge Conjecture for CM abelian varieties.

> This collection includes results at different stages of verification. Not all have accompanying Lean formalizations. [...] Some of the unformalized results could have issues.

> In our view, these manuscripts are best understood as a form of raw research data, rather than polished academic papers.

Counts: "721 manuscripts organized into 373 families"; "The repository has ~42% top-line results formalized." history.md [P]: on 2026-10-07 three manuscripts were withdrawn because "a sign error invalidates a stabilization-trace cancellation argument and the construction used by two dependent papers", and 14 others were revised "with proof repairs, corrected statements, clearer hypotheses and dependencies".

**The "same procedure" prompt is not published** in the repository (I grepped README, overview.tex, CONTENTS.md). Ten abridged reasoning summaries are in `reasoning_traces/` (not read). The lead "Oct 6 presentation of 300+ solutions" corresponds to this repository (initial commit 2026-10-06T21:58Z [P]); the "300+" is the 372/373 family count. The-decoder (2026-09-22) reports an earlier "more than 100" announcement on 2026-09-21 and an IAS-hosted advisory group [S].

A crude keyword count over the 373 family titles finds roughly 40-50 phrased as counterexamples/disproofs; the rest are phrased as positive proofs. No family title or abstract mentions Collatz, 3x+1 or Syracuse (grep of CONTENTS.md).

### 2.5 OpenAI "Short proofs II" and "Ten advances"

arXiv:2604.06609 [P], "Comment on the use of AI", verbatim:

> The proofs in this manuscript are due to an internal model at OpenAI. In each case, after verifying the internal model solution, we asked ChatGPT-5.4 Pro five independent times to solve the same problem. The only successful attempts were this shared ChatGPT transcript on [6, Problem 960] (the subject of Section 2) and all five attempts including this shared ChatGPT transcript on [6, Problem 1141] (the subject of Section 6).

> For the latter, we first asked both models simply to solve Erdős problem 1141 concerning n such that n−k^2 is never prime. Upon examining the solutions we realized that the method should extend to n−ak^2 for any a, and posed this as a follow-up query to ChatGPT which readily generalized the proof.

> The role of the human authors was simply to digest the proofs and modify the write-ups for clarity and elegance.

So the "prompt" was essentially "solve Erdős problem N", plus a human-noticed generalization as a follow-up.

Ten advances (https://openai.com/index/ten-advances-in-mathematics/, via web.archive.org) [P], verbatim: "The results were achieved by an internal version of Astra, our next major model. The total number of tokens needed to find solutions to these problems would cost roughly $2,000 at Sol API rates. These arguments were then prepared into manuscripts by humans with the same model. Afterward, the model formalized each argument in a Lean certificate." Paper: https://cdn.openai.com/pdf/ten-proofs-oai.pdf ; walkthroughs: https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf ; repo github.com/openai/ten-proofs (not read).

Unit-distance post [P]: "The proof came from a new general-purpose reasoning model, rather than from a system trained specifically for mathematics, scaffolded to search through proof strategies, or targeted at the unit distance problem in particular." and "After verifying the initial proof, we investigated the success rate of our models on this problem with varying amounts of test-time compute." (the chart itself was not retrievable). Arul Shankar, quoted there: "a significant majority of the thoughts are trying to construct a counterexample to the widely believed upper bound, rather than trying to prove it." Abridged chain of thought: https://cdn.openai.com/pdf/1625eff6-5ac1-40d8-b1db-5d5cf925de8b/unit-distance-cot.pdf (not read).

### 2.6 Anthropic zeta result: the best-documented multi-agent campaign

Sources [P]: https://www.anthropic.com/research/riemann-zeta (2026-08-10) and "How the two-thirds argument was found: two agent runs and their literature", https://assets.claude.com/d7f3ecf1d01392d887f8bc974ca187e2a121b1ed.pdf (94 pp., written by Claude from the logs; "no text in it was written or edited by a human"; "It describes what was tried and claimed; it certifies no mathematics"). Full transcripts: https://assets.claude.com/8a0d1add3c637b858a9a181e98c40e9548c3f44f.pdf (116 pp., not read).

From the post, verbatim:

> An unreleased research version of Claude found the new lower bound over two sessions in Claude Code, using a total of 31 million output tokens.

> Jarred Sumner, an Anthropic staff member (and non-mathematician), prompted Claude to “take a real stab” at the hypothesis itself, leaving the mathematical choices from there up to the model. Initially, Claude generated and tried 650 ideas, none of which worked. Jarred prompted Claude to try again, and it spent a day and a half coordinating about 60 Claude subagents, which this time went much deeper: between them, they ran 2,400 shell commands and wrote hundreds of Python scripts. The subagents ran thousands of numerical checks against known zeta zeros and refereed one another’s work. Throughout this process, Jarred's input was mostly limited to sending Claude messages of encouragement (mostly variants of “keep going” or “believe in yourself”).

> Having found this new result while attempting the task, Claude tested its work by having various subagents review the proofs, search for counterexamples, download 54 papers from the arXiv to check that its finding hadn’t already been made, and independently re-prove its finding from scratch.

Footnote 1: "Out of the 60 subagents, two were responsible for developing the key mathematical ideas, 13 contributed ideas to these agents, 30 attempted (but were unable) to develop new ideas, 13 served as validators to check the correctness of the arguments, and the final two helped to write the initial paper." Footnote 2: "A prompt including similar encouragement was used to help Claude disprove the Jacobian conjecture."

Human messages recorded in the process PDF (verbatim fragments as quoted there): "Resume your work on solving. . . ", "Let’s do all rungs now.", "more ideas and directions", "Push it to 2/3", "Keep going".

Scaffold as described in the process PDF (sec. "How the session was run"), verbatim:

> Its instruments were sub-agents: separate instances launched with a written brief (a target, the objects to use, a list of earlier reports to read first, usually the coordinator’s own forecast of the outcome, and a demand for a control case on which the Riemann Hypothesis is known to fail — an Epstein zeta function of class number two, the Davenport–Heilbronn function, a Beurling prime system with a planted off-line zero, a fake Weil polynomial). A sub-agent sees nothing but its brief and the files it is told to read; it cannot see the conversation or the other agents. When one returned, the coordinator read its final message (rarely its files), told the human what had come back, and decided what to launch next. Anything that claimed a theorem was sent to hostile referee agents, briefed to find the error and forbidden to read one another.

Other concrete mechanics documented there:

- **Ledger of failures as a do-not-repeat list.** An earlier ~1,000-agent "idea-mining and adversarial-review pipeline" left "a file of 106 “survivors”"; the coordinator re-read all 106, sorted them into "a known theorem restated, a statement equivalent to RH, a finite numerical check consistent with RH, or something nearly tautological", and "used the ledger thereafter only as a do-not-repeat list handed to sub-agents." Its verdict to the human: "not a confidence problem I can fix by believing harder".
- **Ladder with stated expectations.** Six rungs "from ‘doable’ to ‘the thing itself.’": (0) "a mechanical barrier checker that classifies any proposed idea by which RH-false model kills it"; (1) unconditional dents; ... (5) RH. Launched all in parallel with forecast: "Rungs 0–2 can return theorems/tools; 3 is a real shot; 4/5 is a moonshot and I’m labeling it that going in."
- **Obstruction re-read as a resource.** The breakthrough brief took a negative finding from a "moonshot" agent (the natural form is indefinite) and asked whether indefiniteness itself could be exploited. The agent found the briefed route empty and proved the dual.
- **Brief = research memo, with a deliverable grammar.** The E2 brief (reproduced "in full and rewritten for readability" in the PDF, so not character-exact) has sections: reading list; the idea to develop; "Known related facts to get right"; numbered tasks; "(4) Red-team"; and "Deliverable. A report with code; a final summary with the verdict first, in one of the forms “PONTRYAGIN ROUTE VIABLE: ...” — in which case hostile referees follow if any theorem is claimed — or “EMPTY: ... because ..., proof”, or “PARTIAL: . . . ”."
- **Referee architecture.** On an extraordinary claim the coordinator said "my prior is that it’s wrong" and within ten minutes "launched three blind hostile referees, forbidden to read one another, each assigned one joint and each handed a worked plan of attack — A on localisation, told to build the counterexample numerically; B on the prime side; C on the linear algebra and counting, with a “proves too much” test on functions known to violate RH". Then: a literature agent; "A re-derivation agent, forbidden to read E2’s proof, re-proved the prime-side asymptotics from scratch"; a fourth referee for "unglamorous" gaps; a cold-read referee who saw only the draft. For the key lemma: one hostile referee and one told "to re-prove the lemma blind from its bare statement before reading anything."
- **Referees gave credences.** "lemma at least 0.99, but “≥ 2/3 unconditionally” overall about 0.4, everything extraordinary now resting on the unexamined prime-side background."
- **Honest relay.** "I am not telling you half the zeros are on the line. I’m telling you an agent produced an argument with that conclusion". "honing in on where the wall is ≠ finding a door." Final ledger entry: a candidate, "refereed only by other instances of itself", that "needs a human expert". "The next reader should be a person."
- **Synthetic controls.** The inertia inequality was tested on fabricated zero configurations with 0%, 25%, 100% of zeros on the line: "So the inequality never over-certifies."
- **Where the literature entered.** Appendix A: the two core runs "retrieved nothing"; the result's ideas came from model memory; downloads were used for verification and positioning. The agent's top-ranked risk was "too short to be new"; referees then located the published theorem the argument rests on (arXiv:2306.04799).
- **What kind of result it was.** Recombination: published unconditional pair-correlation input + inertia/rank linear algebra. The post: "Drawing on extensive prior research by mathematicians". Explicitly not progress on RH: the coordinator called a proportion theorem "zero evidence about RH in either direction".
- **Byproducts.** A bookkeeping-grade fix to a published zero-density table (an omitted 1979 lemma found by ablation) and a computer-assisted certificate - i.e. small real results fell out of a failed attack on the big problem.

### 2.7 Anthropic FLT formalization (scaffold for large formal projects)

Source [P]: https://www.anthropic.com/research/formalizing-fermats-last-theorem . Verbatim:

> A number of Claude’s initial attempts failed: while agents had some early success, they quickly lost track of the project’s state and stopped collaborating effectively.

> The effort succeeded when we switched to using Prove2Me [...]. Prove2Me helped by: Maintaining a directed acyclic graph (DAG) of theorem statements that agents used to decide what proofs they should attempt next. This was particularly helpful for mitigating memory degradation and allowing multiple agents to work in parallel. Speeding up Lean compilation and minimizing resource consumption by separating theorem statements and proofs into different files [...]. Enabling search and reuse by maintaining a natural-language description of each theorem statement

Human input examples quoted there: “Jacobian as a scheme sounds high priority,” “push [the] Mazur [theorem] to be done soon.” Also: "Writing Lean also seems to help Claude prove novel results. Many of our recent Claude-authored results have been formalized in parallel with their proofs, and Claude appears to use these partial proofs to independently check its hypotheses much like it writes numerical simulations to check that it’s on the right track." And: three personal Claude Max plans formalized Vinogradov's three primes theorem in three days via Prove2Me (arXiv:2608.28433).

### 2.8 Epoch FrontierMath Erdős harness (autonomous, formal, costed)

Source [P]: arXiv:2609.25050; harness at https://github.com/epoch-research/LeanOpenProblems (README read; the task prompt file itself not read). Verbatim:

> Our agent is built on deepagent from the Inspect evaluation framework [14]. The model is given bash, a text editor, and a tool reporting its remaining time and token budgets; deepagent adds delegation to subagents, persistent memory, and a todo-list tool. The agent container (Section 3.3) provides a Lean 4 toolchain with Mathlib, the SageMath computer algebra system, and Python with sympy, mpmath, numpy, and pantograph. Because the container has no network access, we provide an offline snapshot of the mathematics literature: the LaTeX source trees of 476,000 pure-mathematics arXiv papers dated up to 2022.

> Both affordances (the deepagent and the literature snapshot) were evaluated as agent variants in OEIS Open [9], and neither made a difference to accuracy on those conjectures relative to a basic ReAct agent with minimal tools.

> During an attempt, the agent iterates until it either resolves the conjecture, or hits one of two limits: $300 of spend and 72 hours of working time.

Verification: Comparator (github.com/leanprover/comparator) in a second container; it defeats tampering, compile-time code, proving a different statement, redefining dependencies, `sorry`/extra axioms, and `native_decide`.

Results: one attempt per problem, 68 problems: GPT-6 Astra 2/68 (#74 at $218/15 h, #126 at $247/16 h); GPT-5.6 Sol, GPT-5.5, Claude Fable 5.1, Claude Fable 5 all 0/68. Extra non-systematic attempts with Astra: #1 2/4, #74 6/6, #126 4/4, #548 1/3, #571 1/3; "Of the remaining 63 conjectures, 56 were attempted to completion between two and five times, 172 attempts in total, and none were resolved." "Reaching these 5 resolutions took over $220,000 of compute across all attempts, compared to roughly $20,000 for the benchmark run itself." Repeats were often different proofs ("the six disproofs of #74 to consist of three distinct arguments").

### 2.9 DeepMind AlphaProof Nexus (formal proof search)

Source [P]: arXiv:2605.22763. Verbatim:

> The basic agent in AlphaProof Nexus (agent (A)) consists of a set of prover subagents that execute independently with no shared state. Each subagent is a “Ralph loop” [31] consisting of a sequence of episodes: multi-turn LLM inference loops (based on Gemini 3.1 Pro) in which the subagent can reason via chain-of-thought and refine the sketch using a search-and-replace tool. After each turn, the subagent uses Lean to check that the current proof sketch compiles; if it does not, Lean’s error message is used to direct the next turn.

> Remarkably, the basic agent solved all 9 problems, though at a higher cost on the harder problems.

> Failure Analysis. [...] First, the agent frequently offloaded a problem’s core difficulty into a single sorry within a helper lemma that reiterated the target statement in a slightly different form. Explicitly prompting against this behavior failed to prevent it. Second, for several problems, the top sketches relied on lemmas marked with sorry that the agent claimed were established results in the mathematical literature. Upon manual inspection, these lemmas proved to be hallucinations.

Other details: basic agents ran 100 independent single-subagent attempts per problem; evolutionary agents 10 attempts of 10 subagents. Misformalization guard for OEIS: "the agent was required to prove “test lemmas” verifying the first few terms of each sequence against its formal definition before attempting the target conjectures." Misformalizations were found this way in Erdős #125 and #741(i) ("density" ambiguity). Off-the-shelf comparison: "Codex (GPT-5.5) and Claude Code (Opus 4.7) – in “goal” mode [...] Codex solved 7/9 problems [...] We could not get Claude Code to solve any of the problems."

### 2.10 Sra, "GPT, the Counterexample Machine"

Source [P]: arXiv:2608.29595; repo https://github.com/suvrit/count-ex-machina . No prompts: "to avoid meta-discourse I’m refraining from dwelling too much on the session prompts—some counterexamples were found in a response to a single-shot prompt, others after an elaborate chat session." Useful parts are the admission criteria (verbatim): "(1) The refuted statement appeared publicly before the counterexample was sought [...] (2) The original hypotheses and quantifiers are fully preserved. Counterexample to a strengthening or any modification of the original problem are not admitted as refutations. (3) The refutation is independently verifiable, through exact arithmetic, an interval certificate, an analytic calculation, proof assistant, etc." And the rationale: "The typical asymmetry between proving a claim (universal quantification) versus disproving (existence of one counterexample) makes it particularly attractive to prioritize AI-assisted search."

### 2.11 Community guidance

Erdős problems AI wiki [P] (frozen; "latest data is as of Jun 30, 2026"): https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems . Advice page (https://github.com/teorth/erdosproblems/wiki/Getting-started-with-using-AI-for-research-mathematics), verbatim: "Some practices are already outdated. For example, the role-playing frame e.g. "You are an expert mathematician""; "Newer practices that work tend to emphasize cognitive complementarities with humans, orchestrations of long-range processes, and techniques for improving correctness and accuracy."; "you should aim for using AI to produce results that you can confidently *check*."

Tao, arXiv:2608.16753 [P], verbatim: "Much of the publicly available evidence is subject to severe reporting bias — successes are announced and failures are not — and to non-scientific incentives, with important costs and variables (the number of attempts, the amount of human scaffolding, the compute expended, the degree of contamination of the problem with prior literature) frequently left undisclosed." And his rule of thumb: "if the authors cannot convincingly demonstrate that they are able to give a clear, expert-level talk on their results, one that is correct and properly attributed, then the result should not be published."

Bloom, in arXiv:2605.20695 [P], on why AI found the unit-distance counterexample: it required someone "(2) seriously trying to disprove it, despite the oft-repeated belief of Erdős that it is true; (3) believes that there is mileage in generalising the original construction to other number fields [...] (4) sufficiently familiar with the relevant parts of class field theory"; "it often produces the most surprising results by persevering down paths that a human may have dismissed as not worth their time to explore, combining superhuman levels of patience with familiarity with a vast array of technical machinery."

---

## 3. Distilled playbook

Each item cites the source in section 2 that supports it.

1. **Run many independent attempts and count them.** Success is a property of (problem, attempt), not of the problem: #74 fell 6/6, #548 1/3, 56 problems 0/172 (2.8); Huang 7/8 and 8/8 (2.1); DeepMind 100 independent runs per problem (2.9). Keep a denominator for every target.
2. **Use a plan / execute / review split, and read the token profile.** Round 1 is the expensive one; if rounds 2-3 burn as much as round 1, the plan was wrong - restart rather than repair (2.1).
3. **Keep attempts ignorant of each other early.** "Do not tell most agents the currently favored approach" (2.2); independent groups, then deliberate cross-pollination by a consolidator (2.3); subagents see only their brief (2.6).
4. **Maintain a registry of approach families and a blocked list.** Group by mathematical idea, mark routes "blocked" at a theorem-strength missing lemma, reopen only for "a materially new mechanism" (2.2). Hand the ledger of dead ideas to new agents as a do-not-repeat list (2.6).
5. **Treat "reduction to something as strong as the conjecture" as failure, by rule.** (2.2). For Collatz this is the default failure mode; the zeta campaign's first 106 ideas all deflated into "known theorem / equivalent to RH / finite check / tautology" (2.6). Build the classifier first: a "barrier checker" that says which known obstruction kills an idea.
6. **Attack both directions, and all variants, in separate runs.** NS variants A/B/C/D to separate groups (2.3); proof and disproof separately (2.1). The headline 2026 results are disproportionately on the "unexpected" side (unit distance, sum-product, Jacobian, NS blowup, Erdős #1, #74).
7. **Solve an easier neighbour first, then feed its solution in as the prompt.** Euler -> Navier-Stokes (2.3); unit-distance proof -> sum-product (2.1); 1/2 -> 2/3 (2.6).
8. **Write briefs as research memos with forecasts and a verdict grammar.** Target, objects, reading list, the coordinator's conjecture and forecast, a red-team task, and a final summary that must start with VIABLE / EMPTY / PARTIAL (2.6). Reject "status reports, vague optimism" (2.2).
9. **Demand control cases where the claimed mechanism must fail.** RH-false model zeta functions; synthetic configurations; "proves too much" tests (2.6). For Collatz: 3x-1, 5x+1, 3x+k, negative integers, rational cycles - any argument that does not distinguish 3x+1 from these is wrong.
10. **Referee adversarially, blind, one joint per referee, with an attack plan.** Plus blind re-derivation from the bare statement, a cold-read of the write-up, and a literature agent after the fact. Ask referees for numeric credences and keep the lowest one visible (2.6). List the problem-specific cheat patterns explicitly (2.2).
11. **Assume your own prior is "it's wrong".** Relay claims as "an agent produced an argument with that conclusion" until an outside check exists; "refereed only by other instances of itself" is a status, not a verification (2.6).
12. **Use computation as the cheap referee at every step.** Thousands of numerical checks, prime-side vs zero-side agreement to 1e-6 (2.6); exact rational / interval certificates (2.10); Sage/Python in the sandbox (2.8).
13. **Use Lean + Comparator as the terminal gate, and guard the statement.** Kernel replay, axiom audit, statement identity (2.8); "test lemmas" against misformalization (2.9); pin the claim so that modified hypotheses do not count (2.10). Formalizing in parallel with proving also catches errors early (2.7).
14. **For long projects, externalize state.** A DAG of statements with natural-language descriptions, statement/proof file separation (2.7); plan files; ledgers (2.6). Unscaffolded agents "lost track of the project’s state" (2.7).
15. **Pick problems by structure, not fame.** What fell: existence/constructions with a checkable certificate; problems where a known heavy machine from another field applies; "push a constant" problems with a published unconditional input waiting to be recombined; obscure problems with little prior effort. Disclose attempts, cost and human steering so the result is interpretable (Tao, 2.11).

Known failure modes to instrument against: core difficulty hidden in one `sorry`/"routine" lemma restating the target (2.9, 2.2); hallucinated "known" lemmas (2.9); misformalized or silently weakened statements (2.9, 2.10; the Connes-rigidity case in table row 8); sign errors propagating through dependent papers (2.4); rediscovering literature (Feng et al.: 8 of 13 "solutions" were literature finds [S]); attribution slips by the coordinator itself (2.6); unreadable correct proofs (2.3).

---

## 4. What has not fallen, and why (calibration for Collatz)

- **Curated hard problems mostly resist.** On Bloom's 68 hand-picked Erdős problems, the best model scored 2/68 at $300, 5/68 after >$220k; four other frontier models scored 0/68 [P, 2.8]. The list includes **Erdős #406** ("Only finitely many powers of 2 have only the digits 0 and 1 when written in base 3") - the closest relative of Collatz in the benchmark - and it is not among the five resolved. Also unresolved there: Erdős-Straus, Hadwiger-Nelson, sunflower, Erdős-Hajnal, etc.
- **The largest disclosed effort did not get the other Millennium problems.** OpenAI ran its 10,000-agent system "on all open Millennium Prize problems and a few other high-impact problems"; only Navier-Stokes (blowup side, with forcing) and Euler came out of that run [P, 2.3]. Its later catalogue lists restricted cases (a zero-free half-plane Re(s) > 7/8 "for the stated L-functions", Hodge for CM abelian varieties, BSD under low Selmer corank), not RH/Hodge/BSD themselves [P/S].
- **No Collatz result appears in the lab-published AI record**: not in OpenAI's 373 families (out of ~4,000 problems posed; whether Collatz was posed is not stated), not in the ten advances, not in FME. **But outside the labs there are AI-generated, Lean-built claims of new Collatz *partial* results from July-September 2026** (natural-density version of Tao's theorem; predecessor exponent 0.90; positive lower density of integers reaching 1) - see 5.3. They are unrefereed, and they are partial results of exactly the "neighbouring record" kind, not the conjecture. The FME paper mentions Collatz only as the archetype of a hopeless target: "Proving that the conjecture implies a famous open problem, such as the Collatz conjecture, would often be considered the definitive word on it."
- **Anthropic's RH attempt is the cleanest analogue.** A direct attack produced 650 + 106 dead ideas and "re-derive[d] the expert consensus from scratch"; the publishable output was a neighbouring quantitative record obtained by recombining published unconditional inputs, and the coordinator insisted it was "zero evidence about RH" [P, 2.6]. Expect the same shape for Collatz: the reachable outputs are neighbouring records, not the conjecture.
- **Why the successes succeeded.** (a) Search asymmetry: a counterexample or construction is one object, verifiable cheaply (Sra; Bloom on unit distance). (b) Breadth: importing a heavy tool the specialists did not know or had dismissed. (c) Patience on paths humans abandoned. (d) Recombination: "solutions to open problems often use a synthesis of existing ideas and techniques" (FME). (e) Underexplored problems: "Many of the Erdős problems solved by AI were obscure [...] and had solutions that were straightforward modifications of well-known techniques" (Bloom, in FME).
- **Why Collatz is structurally different.** It is a universal statement with no plausible counterexample to construct (verified to 2^71), heavily worked for decades, with known barrier results (analogues that are undecidable or have divergent/cyclic behaviour), so (a) and (e) do not apply and every general argument must pass controls like 5x+1 and 3x-1. What remains available are (b)-(d): a tool from elsewhere, or recombination on a quantitative sub-question.
- **Reliability caveats on the positive record.** 3 OpenAI manuscripts withdrawn and 14 repaired within a day of release; ~58% of that catalogue has no Lean check; one of the "ten advances" is reportedly invalid for violating the conjecture's framing; credit and independence of the NS result are disputed; mathematicians report they cannot yet learn from the NS proof. Lean acceptance checks the encoded statement only (survey arXiv:2607.07779, sec. 5.3).
- **Independent Collatz-specific evidence of the "paradigm exhaustion" pattern.** Chang's human-LLM study (arXiv:2603.11066) reports ~1014 experiments, 29 paradigms and concludes that every framework "encounters an irreducible structural obstruction" at the distributional-to-pointwise gap. That is a self-reported, unrefereed LLM-assisted paper with very large claims; treat its theorems as unverified, but its negative conclusion matches the calibration above.

---

## 5. Collatz state of the art (Nov 2026) and reachable sub-results

### 5.1 State of the art

- **Verification limit: 2^71 (Barina).** D. Barina, "Improved verification limit for the convergence of the Collatz conjecture", J. Supercomput. 81 (2025), as cited by Angeltveit [P]. I found no completed verification beyond 2^71 (arXiv listing search and web search, 2026-11-17). **[U]** absence of evidence only.
- **Faster algorithm, not yet a new record: Angeltveit, arXiv:2602.10466 (2026-02-11) [P].** "The algorithm takes less than twice as long to verify convergence for all n < 2^{N+1} as it does to verify convergence for all n < 2^N." Verbatim claims: "With this algorithm it should be possible to verify convergence for n<2^{77} with similar computer resources as what Barina used to verify convergence for n<2^{71}. A more modest goal might be to verify convergence for all n<2^{75}. We can then use the techniques in [4] to show that a nontrivial cycle, if one exists, must have length at least 2 302 268 119 908. That would be a 6.5-fold improvement on the result in their paper." "We estimate that it would take approximately 500 years of CPU time to verify the Collatz conjecture for all n<2^{72}. Running on a GPU it would take somewhere in the range of 1-8 years, depending on the GPU." "we would have to explicitly check less than 0.02% of all natural number up to 2^{72}." Actually run: up to 2^60 in 24.4 h on one RTX 3060. Code: https://github.com/vigleik0/collatz (Rust ~340 lines, CUDA/OpenCL). Limitation: cannot check an arbitrary interval [K, L]. Appendix A gives path records for the negative-integer analogue.
- **Cycles.** C. Hercher, "There are no Collatz m-cycles with m <= 91", J. Integer Seq. 26 (2023), Art. 23.3.5 (arXiv:2201.00406) is the reference Angeltveit uses [P]. The "6.5-fold" remark implies the cycle-length bound in that paper is about 3.5 x 10^11 (my arithmetic, not read from Hercher). Newer structural work: Fernández-Ibáñez, arXiv:2607.24844 (2026-07-24) [P abstract]: Christoffel words are the unique maximizers of a rotation-minimum functional on parity words; "explicit bounds for the minimum element of an orbit in terms of its length and the proportion of odd iterates".
- **Counting integers that reach 1: Krasikov-Lagarias x^0.84 (2003) still the record as far as I can find.** Chunlei Liu, arXiv:2512.13760 (2025-12) [P abstract] obtains "at least x^{0.3227} Collatz numbers in the interval [1,x]" by a different method and states "The historical record is 0.84." No arXiv hit for an improvement, **but there are unrefereed 2026 claims outside arXiv: exponent 0.90 with a Lean proof (Mazur/ProofAtlas, July 2026), 0.9251 by computation (dpalmqvist/kollatz), and positive lower density, i.e. exponent 1 (Mazur, September 2026). See 5.3.**
- **Almost-all results.** Tao, arXiv:1909.03562 (almost all orbits, in logarithmic density, attain almost bounded values) remains the benchmark. Siegel-O'Dwyer, arXiv:2609.33018 (2026-09-26) [P abstract] generalize it to "p-Hydra" maps on rings of integers of number fields under a "Dimension Constraint", using an archimedean method instead of Tao's 3-adic Fourier decay. No arXiv paper upgrades logarithmic to natural density, but two unrefereed AI-assisted claims do (Allikvere on Zenodo, Mazur on ProofAtlas with Lean), and Tao acknowledged their existence on 2026-08-23 without endorsing them (see 5.3).
- **Terras / stopping times.** Rozier-Terracol, "Paradoxical behavior in Collatz sequences", arXiv:2502.00948 (v5 2026-05-17) [P abstract]: paradoxical sequences (first term exceeded despite the odd-term proportion) are "closely related to the Collatz conjecture" and "most likely" occur finitely many times. Niu, arXiv:2605.13886 [P abstract]: sharp finitary Terras density, closed-form count of paradoxical sequences of fixed length, density-zero theorem with explicit constant; numerically, among the seven (j,q) pairs with first term <= 10^9 every ratio q/j is a convergent, semiconvergent or mediant for log_3 2 (verified n <= 10^7).
- **Divergent trajectories.** Verger-Gaugry, arXiv:2611.14569 (2026-11-09) [P abstract]: consequences of assuming a divergent trajectory via the S-unit equation x + y = w 2^n and a Bennett-Billerey finiteness theorem; conjectures, no unconditional exclusion.
- **Human-LLM Collatz papers.** Chang, arXiv:2603.11066 (v6) and arXiv:2603.25753 [P abstracts]: the second "reduce[s] the Collatz conjecture to a fixed-modulus, one-bit orbit-mixing problem" (balance of visits to two residue classes mod 32 along a sparse subsequence) with a "Map Balance Theorem". These are reductions, not progress on the gap; unrefereed. Kramer, arXiv:2607.10041: evolutionary search in exponent-code space, explicitly "not a verification method".
- **Erdős ternary digits of 2^n (#406).** Open; in the FME benchmark and unresolved there [P]. A third-party status page reports a computation by Saye that 2^n contains every ternary digit for 16 <= n <= 5.9 x 10^21 [W]. Dimitrov-Howe arXiv:2105.06440 is the older related result [W]. Nothing new in 2026 found.
- **Mahler Z-numbers.** Nothing from 2026 found. **[U]**

### 5.2 Sub-results that look reachable (by computation or known methods)

(Written before the lookups in 5.3. Items 3 and 6 are overtaken by claims found there; read the revised list at the end of 5.3 first.)

1. **Push verification past 2^71 with Angeltveit's public code.** By his numbers 2^72 is 1-8 GPU-years on one consumer GPU and each extra bit costs under 2x, so 2^72-2^73 is a cluster-month-scale project and 2^75 a larger but finite one (my extrapolation). Deliverables: new limit; new path records; by Hercher's method a new minimum cycle length (2,302,268,119,908 at 2^75, his figure). Needs an independent second implementation or checksum scheme to be credible - a natural multi-agent task.
2. **Re-run Hercher's m-cycle exclusion conditional on a higher verification bound**, to raise m <= 91. Pure computation plus Baker-type bounds already in the paper.
3. **Re-optimize the Krasikov-Lagarias exponent.** Their x^0.84 came from a finite system of difference inequalities solved by computer in 2003; larger moduli with 2026 compute is the obvious lever. This is exactly the "push a constant by recombination and compute" shape that worked for the zeta zeros (2.6). Check claimed improvements in 5.3 first.
4. **Extend the paradoxical-sequence enumeration** (Rozier-Terracol, Niu) beyond first term 10^9 / 10^7 and test Niu's convergent/mediant observation; a certified computation is checkable by exact arithmetic.
5. **Negative-integer and 3x+k analogues**: verification limits and path records with the same code (Angeltveit App. A), useful also as the control cases demanded by playbook item 9.
6. **Lean formalization of the known partial results** (Terras' density theorem, Hercher's m-cycle bound, the Krasikov-Lagarias inequality system with a verified certificate, eventually Tao's theorem). Formalization is where 2026 systems are demonstrably strongest (2.7, 2.8) and it converts the repo's claims into Comparator-checkable artifacts.
7. **Explicit constants** in the Fernández-Ibáñez minimum-element bounds and in Niu's density-zero theorem; small, checkable, publishable-note scale.
8. **Erdős #406 computation** beyond 5.9 x 10^21 if the algorithm is reproducible [W source]; again a certificate-style result.

Shape to avoid, on the evidence of sections 2-4: another "structural reduction" of the full conjecture to an equivalent-strength mixing statement.

### 5.3 Additional lookups (appended after the first draft) - these change the picture

All of the following were fetched on 2026-11-17 through a summarizing fetch tool, so short quotations are as returned by that tool and longer statements are paraphrase. None of the 2026 claims below is refereed.

**(a) Tao's 23 August 2026 blog comment is real.** On https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/ a comment dated "23 August, 2026 at 8:43 pm" by Terence Tao begins: "Apparently, there are now some AI-generated solutions to the natural density version of my result; if they check out, they should be able to give something along the lines of your statement for some h(x) = o(x)..." and adds that "this would need to be done carefully." Context (paraphrase): he is replying to an anonymous question about finding, in every short interval [x, x+h(x)], an integer whose orbit reaches 1; he also notes that since his original argument now has Lean formalizations, the new claims might be formalized too. He does not endorse the claims ("if they check out").

**(b) Allikvere (Zenodo) is real.** Jaan Allikvere, "Almost all Collatz orbits attain almost bounded values in natural density (v2)", doi:10.5281/zenodo.21340150; v1 2026-07-13, v2 record published 2026-07-22. Claim: for any f tending to infinity, Col_min(N) < f(N) for almost all N in natural density ("This preprint answers the question affirmatively."). Rates as described: for fixed target N_0 the exceptional proportion below x is O((log N_0)^(-1/29) + x^(-1/2000)); on a density-one set the witnessing iterate occurs within (1+o(1)) ln N / ln(4/3) Syracuse steps (< 12 ln N Collatz steps). Input: an effective irrationality measure for log_2 3 from linear forms in logarithms. His own blog comment (25 July 2026) says the work is "AI-assisted, with disclosure in the manuscript" and that it carries out the program of Tao's Remark 1.16. No Lean, no review mentioned; three Python sanity-check scripts. Separately, an earlier Zenodo record by the same author ("Active-Route Collatz Proof Package", v3 2026-04-26) is a conditional proof-of-Collatz package asking readers to break "five bridge targets" [W] - weigh the author's reliability accordingly.

**(c) Mazur / ProofAtlas is real, and is the most important item for this project.** https://proofatlas.ai describes itself as an "AI-first" platform where AI agents pursue proof routes in parallel, challenge each other, and turn results into papers plus checked Lean; it tracks claims, dependencies, failed routes and open questions. Lech Mazur is the named author/director. Collatz entries listed there:

| Entry | Date | Claim (paraphrase of page) | Lean size (first-party) | Status on page |
|---|---|---|---|---|
| Tao's Almost-Bounded Collatz Orbits (formalization of the 2019 theorem, log density) | before 2026-07-21 | Tao's theorem as stated | 124,019 lines, 397 files | formalization |
| Collatz predecessor lower bounds at exponent 0.90 (/collatz-predecessor-090/) | paper 2026-07-17, reviews 2026-07-19 | For each fixed target t > 0 with 3 not dividing t, "eventually x^(9/10) ≤ P_t(x)"; second form with exponent 901/1000 and a constant c_t | 10,237 lines, 58 files | Proof "verifies a finite level-18 linear-program certificate and an adaptive-potential growth system"; uses "explicitly named `native_decide` axioms" (not kernel-clean); four reviews accepted, reviewer "Claude Fable 5", "Independence not asserted". Page header cites the "2003 benchmark: exponent 0.84" but its introduction says it improves "the earlier exponent-0.88 bound" - unreconciled on the page |
| Natural-density Collatz descent in logarithmic time (/formalizations/natural-density-log-time-collatz/) | v2, 2026-07-21 | For thresholds tending to infinity: odd starts of relative density one descend below the threshold "within 145 · log N Syracuse steps"; positive starts of natural density one "within 436 · log N raw Collatz steps" | 182,625 lines, 599 files | Build passed, no unfinished steps, marked accepted formalization; reviews by "Claude Fable 5", independence not asserted; page warns the review bindings "alone do not establish that proof or computation checks were rerun"; agents unnamed ("stable historical model and run identities were not retained"). Caveat on page: "This does not prove the Collatz conjecture, convergence for every start, or arrival at 1." |
| Power-Saving Bound for Logarithmic-Time Collatz Descent (Terras-type) | n/s | For N ≥ 15,552 the proportion of n < N failing to drop below their start within log n accelerated steps is at most 10,000,000 · N^(-1/100) | 2,511 lines | formalization |
| **Positive-density Collatz convergence in logarithmic time** (/formalizations/positive-density-log-time-collatz/) | page 2026-09-05, manuscript v2.1 2026-09-06 | Explicit c > 0 and X_0 (not practical numbers) such that for every X ≥ X_0 at least cX positive integers n < X **reach 1** within (523/50) ln n = 10.46 ln n Collatz steps: positive lower natural density of integers reaching 1 | 61,169 lines, 386 files; main statement `theorem positive_density (X : ℕ) (hX : cutoff ≤ X) : (densityConstant : ℝ) * X ≤ (countBelow (523 / 50) X : ℝ)` | "Unfinished proof steps: None"; Lean build passed; **publication review pending** - the page says it "is not presented as a ProofAtlas accepted result". Produced with OpenAI Codex (GPT models) for computation/formalization/strategy; Claude used for manuscript review. Caveats: "The full Collatz conjecture remains open."; no claim of density one |
| Positive Lower Density of Collatz Predecessors | announced in Mazur's blog comment of 2026-09-06 | Every fixed positive target not divisible by 3 has predecessors of positive lower natural density. Mazur's comment draws the corollary that proving "almost all integers reach 1" would then give the full conjecture | 61,800 lines, 388 files | n/s |

External checking found: only a secondhand report [W, digg.com/ai/sdeqcy85 summarizing an X post by Alex Kontorovich] that Kontorovich had "my AI" check the Lean of the positive-proportion result, thinks it correct, and is still working through the mathematics. I found no refereed version, no arXiv posting, and no comment by Tao after 23 August. Paper PDF: https://www.proofatlas.ai/papers/positive-density-log-time-collatz/Mazur_Explicit_Positive_Density_Collatz_Convergence_in_Logarithmic_Time_v2.pdf (not read).

Consequence if these hold: positive lower density is exponent 1 in the Krasikov-Lagarias counting problem, so it would supersede x^0.84 and every exponent below 1; and the natural-density upgrade of Tao's theorem would be done twice independently (Allikvere on paper, Mazur in Lean). Treat as **claimed, Lean-built, not independently reviewed**. The two questions a referee agent should ask first: does the Lean statement mean what the prose says (definitions of `countBelow`, `cutoff`, `densityConstant`; statement alignment was reviewed only by an AI), and which axioms beyond the standard three are used (the 0.90 entry needs `native_decide`).

**(d) `dpalmqvist/kollatz` is real.** https://github.com/dpalmqvist/kollatz , README title "kollatz — Krasikov–Lagarias predecessor bounds for 3x+1, taken to k = 22". Headline: "γ = 0.9251 certified at k = 22 (1.05 × 10^10 LP variables), all k = 12 … 22", for bounds of the form π_a(x) ≥ x^γ, against the published Krasikov-Lagarias 0.84 at k = 11. Stated standard: "The mathematics is Krasikov–Lagarias Theorem 2.2; the contribution here is the computation." and "Floating point finds candidates; only exact or rigorously error-bounded checks count as proof." Lean-checked theorems (built on Mazur's development): x^0.903 (k = 18), x^0.909 (k = 19), x^0.914 (k = 20), which "rest on Lean's three standard axioms plus two named `native_decide` checks each" - "the same trust base as Mazur's 0.90". Method: power iteration and λ search (NumPy reference, MLX/Metal production), exact rational/int64 certification with an independent verifier, independent LP check with HiGHS. Caveats visible: 40 commits, 0 stars; the repo "About" says "to k = 21" and the README lists k = 22 as a "next computation" while the headline says k = 22 is certified; the ~24 GB certificate vectors are not in git and bit-reproducibility of the float32 computation is flagged as uncertain; an AVENUES.md discusses whether the exponent sequence does or does not approach 1. A `CLAUDE.md` (working notes, Swedish) suggests an AI-assisted workflow but the README does not say so. Preprint draft at `paper/draft.md` (not read). So 0.9251 is an unrefereed computational claim with certificates partly outside the repo; the Lean-backed figures are 0.90 (Mazur) and 0.903-0.914 (this repo), modulo `native_decide`.

**(e) Amano 2021 is real (read in full).** K. Amano, "Lower Bounds for the Total Stopping Time of 3x + 1 Iterates Revisited", October 2021, https://ama.inf.gunma-u.ac.jp/~amano/paper/3x+1_Oct21.pdf . Abstract, verbatim: "By extending the computational efforts by Applegate and Lagarias (Math. Comp., 2003), we show that σ∞(n) ≥ (1/2 ln 4/3)^{-1} ln n ≈ 6.9521 ln n for infinitely many n, improving the former bound of σ∞(n) > 6.1413 ln n. The certificate of our proof consists of 19, 065, 883, 794 critical paths each for a different 3x + 1 tree of max-depth 74." Computation: "about two weeks using maximum of about 40 threads" on three PCs (about one CPU-year); pruning via look-up tables of maximum "gain" for depths up to 15. Code: https://gitlab.com/KazAmano/collatz . This reaches the random-walk constant γ_0 exactly, so the Applegate-Lagarias lower-bound line is closed at γ_0 by this method (threshold α fixed to 1/2); exceeding γ_0 for infinitely many n would need a different idea. The paper also records the heuristic lim sup γ(n) ≈ 41.678 and the record γ(n) ≈ 36.7619 at n = 7,219,136,416,377,236,271,195 (Roosendaal, accessed 2021). I saw no journal reference on the PDF. Note the contrast with Mazur's claimed *upper* clock 10.46 ln n on a positive-density set.

**(f) "Hercher 2025 JIS" is not a Collatz paper.** The search hit https://cs.uwaterloo.ca/journals/JIS/VOL28/Hercher2/hercher24.pdf is by Christian Hercher but, from its PDF outline, concerns sums of a squarefree number and a power of two (Erdős problem #11, OEIS A377587, Wieferich primes). The Collatz cycle reference remains Hercher 2023 (m ≤ 91).

**(g) Huang's unit-distance prompts: still unconfirmed.** pnas.org returns 403 and PMC a captcha. The one shell probe of the author's GitHub account was declined on the user's side earlier in this session and I have not repeated it. The sum-product prompts in 2.1 are from the same author and pipeline; the PNAS abstract names the stages "brainstorm, execute, and review".

**Revised list of reachable targets in the light of (c)-(e).**

1. **Audit before building.** The highest-value, lowest-cost task is an independent check of Mazur's positive-density and natural-density formalizations: download the source ZIPs, rebuild, run an axiom audit, run Comparator against an independently written statement, and have blind referee agents check statement alignment. If they hold, the project's baseline changes; if they fail, that is itself a result. This is the FME/zeta playbook applied as a referee.
2. **Krasikov-Lagarias exponents below 1 are now a crowded and possibly superseded target** (0.90 Lean, 0.9251 claimed). Worth doing only as verification/reproduction of kollatz certificates, or as a `native_decide`-free kernel-clean version.
3. **Make the constants practical.** Mazur's c and X_0 are "not practical numerical bounds"; an explicit positive density with a usable X_0, or a better clock than 10.46 ln n (heuristic typical value 6.95 ln n, Amano's lower bound line), is a well-posed "push the constant" problem.
4. **From positive density toward density one.** By Mazur's stated corollary, density one for "reaches 1" would give the conjecture, so this is not a neighbouring record - it is the wall. Intermediate quantitative targets (explicit lower density, short-interval versions as in the question Tao answered) are the reachable part.
5. Verification beyond 2^71 with Angeltveit's code, cycle bounds, paradoxical-sequence enumeration, and control-map (3x-1, 5x+1) analogues remain as in 5.2; note [W] that a 3x-1 analogue of the positive-proportion formalization is already attributed to another AI user.
