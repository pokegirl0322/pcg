import pathlib

from compiler import compile_intent
from solver import solve
from corpus.dinner_ir import dinner

REPO = pathlib.Path(__file__).resolve().parents[1]


def test_dinner_roundtrips_to_sat():
    program = compile_intent(dinner)
    out = REPO / "generated" / "dinner_test.lp"
    out.parent.mkdir(exist_ok=True)
    out.write_text(program.text())
    assert solve(out) == "SATISFIABLE"