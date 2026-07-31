import json
import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[1]
ENGINE = REPO / "external" / "Gemini" / "asp" / "generation" / "gemini.lp"


def clingo_version() -> str:
    r = subprocess.run(["conda", "run", "-n", "gemini-2020", "clingo", "--version"],
                       capture_output=True, text=True)
    return r.stdout.strip()


def solve(intent_lp: pathlib.Path, models: str = "1") -> str:
    # return sat or unsat
    r = subprocess.run(
        ["conda", "run", "-n", "gemini-2020", "clingo",
         str(ENGINE), str(intent_lp), models, "--outf=2"],
        capture_output=True, text=True,
    )
    data = json.loads(r.stdout)
    return data["Result"]


if __name__ == "__main__":
    print(clingo_version())