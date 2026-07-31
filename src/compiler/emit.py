# one per schema family. ir object --> list[Line].

from schema.models import Bounds, Label, ReadingRequirement
from compiler.provenance import Line
from signatures import BOUNDS_CONSTS

def emit_bounds(b: Bounds) -> list[Line]:
    return [Line(f"#const {name} = {getattr(b, name)}.", f"bounds.{name}")
            for name in BOUNDS_CONSTS]

def emit_label(lb: Label) -> list[Line]:
    prefix = "e" if lb.target_kind == "entity" else "r"
    target = f"{lb.target_kind}({prefix}({lb.index}))"
    if lb.visibility:
        text = f"label({target},{lb.name},{lb.visibility})."
    else:
        text = f"label({target},{lb.name})."
    return [Line(text, f"label.{lb.target_kind}{lb.index}")]

def emit_reading(rr: ReadingRequirement) -> list[Line]:
    if rr.mode == "required":
        return [Line(f"required({rr.quality}).", f"reading:{rr.quality}:required")]
    if rr.mode == "asserted":
        return [Line(f"reading({rr.quality},{rr.target}).", f"reading:{rr.quality}:asserted")]
    # default: constraint
    return [Line(f":- not reading({rr.quality},{rr.target}).", f"reading:{rr.quality}:constraint")]