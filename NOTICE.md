# NOTICE — Provenance & Attribution

## Gemini (upstream dependency)

This project builds on **Gemini**, an intent-based abstract game generator from the
Expressive Intelligence Studio (UC Santa Cruz).

- **Upstream:** https://github.com/ExpressiveIntelligence/Gemini
- **Included as:** a git submodule at `external/Gemini`, pinned to commit
  `e6ab676e99d303e6d44292a0d66a1e3c7ba5808b`.
- Gemini's source is **not** copied into this repository — it is referenced only.

At the time of writing, the upstream Gemini repository does **not** include an explicit
open-source license. All rights in Gemini are retained by its authors. This project
references Gemini for academic research and does not redistribute its source. Anyone
reusing this project must obtain Gemini independently from upstream and comply with the
authors' terms.

## Third-party libraries bundled inside Gemini

Gemini's interpreter bundles third-party code under its own licenses. These live in the
submodule, not in this repository, but apply when running Gemini:

| Library | License |
|---------|---------|
| ANTLR4 runtime (`interpreter/antlr4/`) | BSD 3-clause |
| Phaser (`interpreter/lib/phaser.js`) | MIT |
| Smoothie / `require.js` (Flowy Apps) | LGPL v3 |
