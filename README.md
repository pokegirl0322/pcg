# pcg

Research project on the resurrection and augmentation of **Gemini** an Answer Set
Programming (ASP) based abstract game generator with an LLM-driven prompt → intent
layer, applied to procedurally generating Super Mario levels.

This repository contains **only this project's own work**. Gemini itself is referenced as
a pinned git **submodule** (see [`NOTICE.md`](NOTICE.md)); its source is not copied here.

## Repository structure

| Path | Contents |
|------|----------|
| `docs/` | Research devlog — literature review, implementation notes |
| `src/` | This project's LLM intent-layer code |
| `external/Gemini/` | Upstream Gemini, as a pinned submodule (commit `e6ab676`) — **not vendored** |

## Getting the code

Gemini is a submodule, so clone recursively:

```bash
git clone --recurse-submodules <this-repo-url>
# already cloned without --recurse-submodules?
git submodule update --init --recursive
```

## Running Gemini

Full instructions: [`external/Gemini/asp/README.md`](external/Gemini/asp/README.md).
In brief, with the `potassco` conda environment active:

```bash
cd external/Gemini/asp
python simulate.py temp 5 generation/gemini.lp intents/dinner_intent.lp 10 --project
```
