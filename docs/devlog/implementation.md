# Implementation Devlog
**Date:** 6.21.26  
Cloned Gemini onto local desktop, downloaded clingo, and troubleshooted Anaconda (issues running with my Windows Powershell, later switched to Anaconda Powershell and worked).

**Date:** 6.23.26  
Set up of 2020 environment (including installing python 3.7, clingo 5.4, numpy 1.19 and deap 1.3.1, all other dependencies limited to Python standard library or out of scope (untouched server/ node packages)) to  mimic original repository's execution state without modifications. Nothing in Gemini has been edited.

Environment:
- OS: Windows 11 (Windows PowerShell 5.1)
- Conda env: `gemini-2020`
- clingo: **5.4.0** (CLI; `--outf=2` JSON is consumed by `simulate.py`)
- Python: `3.7`
- numpy: `1.19` · deap: `1.3.1`
- Resolved env captured in: `environment-gemini-2020.yml`
- Run date: `6.23.26`
- Working dir: `asp/` (required `gemini.lp` resolves its `#include` relative to its own folder)
- Full console logs: `<path to the teed .log files>`

Commands (verbatim):
clingo generation/gemini.lp intents/dinner_intent.lp  
python simulate.py temp 5 generation/gemini.lp intents/dinner_intent.lp 10 --project

Results:
| Command | Expected | Actual | Status |
|---------|----------|--------|--------|
| `clingo …` | SATISFIABLE + ground facts | `Answer: 1` + full fact set → `SATISFIABLE` (~9.3 s total, 4.2 s solving) | green |
| `simulate.py …` | `temp_1.lp … temp_N.lp` | `JSON LOADED 10` → GA over `GAME 0…4` → `temp_1.lp … temp_5.lp` | green |

`JSON LOADED 10` confirms `simulate.py` parsed clingo 5.4.0's `--outf=2` JSON with no mismatch: the version-sensitive coupling between the solver output and the Python parser held on the period-correct clingo.

Benign output (NOT failures):
Logged so the raw console capture isn't misread as errors:
- `info: atom does not occur in any rule head` (×~20) - clingo **INFO**: atoms used in rule bodies but never derived in a head. Version-independent; not a breakage warning.
- `b'…generation\\generation.lp:264…'` - `simulate.py` echoing clingo's captured stderr (the INFO lines above) as a bytestring; its own debug print.
- `AFTERB …`, `(500,)`, `PLAYER CONTROLS …`, `GAME N` - `simulate.py`'s genetic-algorithm progress/debug output.

Observations (recorded, not fixed):
- **File count:** produced **5** files (`temp_1`–`temp_5`, one per `m=5`), not the "25" mentioned in `asp/README.md`. That README note ties the 25-file duplication to the ClimateChange project's `Coordinator.js`, so its absence here is expected and irrelevant to this project.
- **Non-determinism:** `simulate.py` uses `random` + DEAP with no fixed seed, so re-runs yield different games; outputs are not bit-reproducible across runs.

success!!

**Date:** 7.5.26

Started Stage B: bumping Python 3.7→3.9 first, holding clingo/numpy/deap at their 2020 baseline versions to isolate the axis. Isolation was done to ensure that if regression happened, I could pinpoint it on a specific dependency upgrade. Took three tries to get a valid environment, failures listed below, not code related:

1. `conda install -n <env> python=3.9` (no channel flag) silently failed to solve - `LibMambaUnsatisfiableError` on `numpy-base`, because it was resolving against the `defaults` channel only, not `conda-forge` where the original env's packages actually came from. A failed solve doesn't touch the env, so always re-check `python --version` after as I nearly treated a no-op as a successful bump.

2. Adding `-c conda-forge` still failed: the cloned env had leftover Python-3.7-specific builds (`pip`, `setuptools`, `wheel`, `wincertstore`, all `py37`-tagged) from the original `defaults`-channel install, and `conda install` won't proactively upgrade packages it wasn't asked to touch, making an upgrade to 3.9 impossible.

3. Fix: abandoned the clone for this hop and built a fresh env from scratch (`conda create -n gem-step1-py39 -c conda-forge python=3.9 numpy=1.19.5 deap=1.3.1 clingo=5.4.1 pip`).

Verified versions: `python 3.9.23, numpy 1.19.5, deap 1.3.1, clingo 5.4.1`

Smoke test: `clingo generation/gemini.lp intents/dinner_intent.lp` → `SATISFIABLE`, one model, same benign "atom does not occur in any rule head" grounding warnings as the 2020 baseline (pre-existing, unrelated to the version bump). Then `python simulate.py temp 5 generation/gemini.lp intents/dinner_intent.lp 10 project` ran to completion including clingo subprocess call, JSON parse, DEAP genetic-algorithm loop, and file write all succeeded for all 5 games, no tracebacks. No `typing` import failure, no DEAP `creator.create` reimport error, no clingo output-format issue observed.

Step 2: clingo 5.4.1→5.7.1, holding python=3.9, numpy=1.19.5, deap=1.3.1 from Step 1. Hit the missing-channel error a third time (`conda install -n gem-step1-py39 clingo=5.7` with no `-c conda-forge` → `PackagesNotFoundError`); fixed with `-c conda-forge` and it resolved cleanly since this was a clone-forward from an already-conda-forge-only env, no ABI conflicts this time.

Smoke test: `clingo generation/gemini.lp intents/dinner_intent.lp` → `SATISFIABLE`, same grounding warnings as baseline. `python simulate.py temp 5 generation/gemini.lp intents/dinner_intent.lp 10 --project` completed all 5 games, no errors.

**Notable, not a break:** solve time went from ~9-11s (clingo 5.4) to ~30s (clingo 5.7) on the identical `dinner_intent.lp` run. Likely noise between runs, as I reran when upgrading numpy and solve time went to ~15s (clingo and numpy are independent).

Step 3: numpy 1.19.5→1.26.4, holding python=3.9, clingo=5.7.1, deap=1.3.1. Clean solve (clingo alone doesn't exercise numpy, so this only confirms clingo/grounding still fine). `python simulate.py temp 5 generation/gemini.lp intents/dinner_intent.lp 10 --project` completed all 5 games, no errors. numpy 1.26.4 is the practical ceiling while deap stays at 1.3.1 (which pins numpy <2.0a0).

Step 4: deap 1.3.1→1.4.2. Could not reach deap 1.4.3/1.4.4 without a further Python bump: deap's newest releases have moved their own Python floor up, so "latest deap" and "stay on Python 3.9" are mutually exclusive right now.

Smoke test clean: `clingo generation/gemini.lp intents/dinner_intent.lp` → `SATISFIABLE`; `python simulate.py temp 5 generation/gemini.lp intents/dinner_intent.lp 10 --project` completed all 5 games, no tracebacks. Notably, the anticipated `creator.create` reimport error did not occur here.

**All four planned Stage B axes are now bumped and green**: Python 3.7→3.9, clingo 5.4→5.7.1, numpy 1.19.5→1.26.4, deap 1.3.1→1.4.2.

**Date:** 7.9.26  

I decided against a one-shot translation for the prompt --> intent layer, going with a solver-feedback repair loop instead. The one-shot translation layer was too unpredictable 

**LLM→ASP Failure Modes and Design Response** (rooted in paper synthesis)
1. General pre-trained LLMs generating raw ASP can achieve high syntactic accuracy (compiles, runs), but inconsistent  semantic accuracy (wrong answer sets). Fine-tuning can solve for this, but is out of project's scope. Therefore, as part of my design, the LLM will not generate raw ASP, instead filling in a structured schema with a deterministic compiler narrowing risk to schema-field selection. While AMR and CNL were both valid intermediaries, a schema was ultimately chosen because AMR is general purpose with no specific knowledge of Gemini's specific predicate vocaburary, needing a general to specific mapping regardless, adding complexity with no clear benefit for this project. CNL was also considered, but its restricted vocabulary and grammar run counter to my goal of exploring how unconstrained natural language can be translated into game mechanics and design intent, and would also again require a translation layer to Gemini's specific predicate vocabuary.
2. Existing pipeline translation (fact→rule→constraint→assembly) had no mechanisms to catch errors introduced early and the AMR parsing mistakes directly are represented onto wrong constraints with nothing to stop them. The design response was to choose a solver-feedback repair loop over one-shot translation specifically so clingo's actual output could be the check with UNSAT triggering a loop back to the LLM for revision (with the use of `debug_rules.py`'s binary-search localization and a provenance map to point at a specific schema field).
3.  LLMs struggle to construct complete correct answer sets(specifically when facts change, but logic remains the same), especially on complex/real-world programs but perform relatively better on direct logical reasoning/classification-style tasks. I'm ensuring that the LLM never computes an answer set with its role (schema-filling, and in the repair loop, schema revision given a specific error) being deliberately closer to extraction and verification-style reasoning than to open-ended answer-set generation, using it's strengths.
4.  Open gap: none of the three papers address fuzzy/creative intent (only specific subsets, like generic programming patterns, bounded combinatorial puzzles, benchmarch ASP problems). Game design inherently is open-ended and because of that, has no single right answer to evaluate the ability of the generator without subjective human viewpoints. UNSAT can catch structural errors, but ultimately cannot tell whether the resulting program follows the human intent. This can be partially addressed by Gemini's own bidirectional proceduralist-reading analysis and the existing human-evaluation protocol but there is no automated fix for prompt to schema mistranslation.

**Pipeline (as of now)**  
Full pipeline as currently designed:  
(1) user provides a Natural Language(NL) design intent.  
(2) A pretrained general-use LLM, via API with structured-output/schema enforcement, translates the NL into a Gemini-specific structured schema (Entities, Resources, Relations, and a fixed library of constraint patterns derived from cataloging the existing intent files).  
(3) A deterministic Python compiler (no LLM involved) translates the validated schema into Gemini intent .lp syntax with one function per constraint pattern, recording a provenance map from each emitted ASP line back to its source schema entry.   
(4) The compiled intent runs through clingo alongside generation.lp/generation_constraints.lp.   
(5) If UNSAT: binary-search localization (debug_rules.py) identifies the offending rule(s) --> possible error here if UNSAT is due to instructions from two constraints merged together, almost undetectable by binary-search (will need to find solution/add to list of banned constraints?), the provenance map traces this back to the responsible schema entry, and a feedback prompt (original NL intent + previous schema + localized failure) goes back to the LLM for a revised schema --> loop back to step 3   
(6) If SAT: run Gemini's own bidirectional proceduralist-reading analysis on the result and diff the deduced readings against the schema's declared readings as a second consistency check. A feedback prompt (original intent + declared readings + deduced readings) goes back to LLM to produce a revised schema if it does not match with a loop back to step 3. Otherwise, move to step 7.  
(7) The final compiled intent proceeds unchanged into the existing pipeline.  

**Evaluation/Verification Methodology (as of now)**
Mechanical correctness (compiler output, clingo SAT/UNSAT) is fully automated. Testing the compiler against hand-built schema instances, checked against existing known-good intent files (dinner_intent.lp, dummy_intent.lp, etc.) is another valid option and is what I plan to do as I build the schema one category at a time, going through existing intents. Testing with the full document is something that will happen likely before I hook up the LLM. Semantic fidelity (aka did the LLM's schema extraction capture what the NL prompt meant) can be tested with a handwritten set of NL-prompt/schema pairs with correct answers (same idea as LLASP's template pairs) (currently unsure if this is in scope, question of whether my semantic reading is the same as others), otherwise will require running the compiled intent through the existing downstream pipeline (generation.lp/clingo → simulate.py's GA → interpreter/'s Phaser renderer) and playing the result. I am not building new visualization tooling, since interpreter/ (and server/+Germinate, if needed later) already exist for this. Playability/design quality is a human-judgment layer and cannot be evaluated autonomously (yet). Osborn et al.'s player-study protocol, already validated on Gemini, will be adaptated if a rigorous evaluation becomes necessary. 

**Build order**: catalog the vocabulary across all 17 intent files → design the schema → write the compiler + provenance map → test the compiler alone against known-good intents before adding the LLM (this should be done one by one with each category of intents + additional escape hatch in case natural language prompt does not fit into any existing categories; consider anomalies & bespoke)→ wire up the LLM/structured-output layer → run a baseline end-to-end test → adapt UNSAT localization → wire the repair loop → iterate against varied prompts.

Will need to see if LLM prompting will cause it to choose escape hatch over existing categories if doesn't easily match.

In this order, I hope to ensure that any errors from the testing runs will result due to a LLM translation to schema issue rather than a schema to asp intent (reducing unknowns when something breaks down, especially considering LLM debugging can involve varied outputs). 

**Date:** 7.14.26  

**The below is the initial hypothesis based upon a preliminary viewing of the intent files and related documents, but the schema will be based on the pattern cataloging done across all of the intent files.**  

**Categories of schema** (based on intents/other related files):  
1. Bounds --> the 12 #const fields  
2. Entity / Resource --> would include id + label(s). entity only has id and label, but resource has an additional visibility field  
3. RequiredFact --> either a reading-type quality (from the ~25-value vocabulary above, unary/relational/compound as applicable) or a bare entity reference  
4. LabelRule --> target, label, visibility, triggering condition  
5. LabelEnum --> target + acceptable-label list (enumeration/enforcement)  
6. CountComparison --> target, comparator, value (the total_count pattern)  
7. RawASP --> escape hatch. A possible solution is to give it a generic pattern, something like: a head (predicate name + list of argument values) and a body (a list of conditions, each also predicate name + arguments, optionally negated) but no syntax. Another thing that could be considered is adding logging (like saying that this doesn't fit with current categories, and letting a human decide later whether to add it as a new category). However, it likely will require further investigation because designing a sufficiently expressive but constrained ASP representation depends on deeper understanding of Gemini's predicate structure and ASP semantics. For the current implementation, I will start with just logging unmatched cases and returning that to the LLM.
