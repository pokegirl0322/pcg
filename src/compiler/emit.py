# one per schema family. ir object --> list[Line].

from schema.models import (Bounds, Label, ReadingRequirement, ModeChange,
                           ModeChangeCap, Count, PoolCount, Property)
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

def emit_mode_change(rr: ModeChange) -> list[Line]:
    m = rr.mode if rr.mode is not None else "_"
    head = ":- not " if rr.polarity == "require" else ":- "
    return [Line(f"{head}action(mode_change({m})).", f"mode_change.{rr.polarity}.{rr.mode or 'any'}")]

def emit_mode_change_cap(rr: ModeChangeCap) -> list[Line]:
    return [Line(f":- {rr.at_least} {{action(mode_change(N))}}.", f"mode_change_cap:{rr.at_least}")]

def emit_count(rr: Count) -> list[Line]:
    return [Line(f":- total_count({rr.target}, N), N {rr.comparator} {rr.value}.", f"total_count of {rr.target} {rr.comparator} {rr.value}")]

def emit_pool_count(rr: PoolCount) -> list[Line]:
    return [Line(f":- {rr.low} {{pool(entity(e({rr.entity_index})),_,_,_)}} {rr.high}.", f"pool_count.e{rr.entity_index}.{rr.low}_{rr.high}")]

def emit_property(rr: Property) -> list[Line]:
    head = ":- not " if rr.polarity == "require" else ":- "
    return [Line(f"{head}{rr.property_name}(entity(e({rr.entity_index}))).", f"property.{rr.polarity}.{rr.property_name}.e{rr.entity_index}")]



