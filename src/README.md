# src/

This project's own code — the LLM-driven prompt → intent layer that generates Gemini
ASP intent files and drives generation.

This layer calls into Gemini via the submodule at `../external/Gemini` (e.g., writing
intent `.lp` files into `external/Gemini/asp/intents/` and invoking `simulate.py`); it
does not modify Gemini's source. If you later need to change Gemini itself, fork it and
repoint the submodule (`git submodule set-url external/Gemini <your-fork-url>`).
