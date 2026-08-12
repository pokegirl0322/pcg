from schema.models import Intent
from compiler.emit import emit_bounds, emit_label, emit_reading
from compiler.provenance import CompiledProgram


def compile_intent(intent: Intent) -> CompiledProgram:
    lines = []
    lines += emit_bounds(intent.bounds)
    for lb in intent.labels:
        lines += emit_label(lb)
    for rr in intent.reading_requirements:
        lines += emit_reading(rr)
    for mc in intent.mode_changes:      
        lines += emit_mode_change(mc)
    for cap in intent.mode_change_caps: 
        lines += emit_mode_change_cap(cap)
    for c in intent.counts:             
        lines += emit_count(c)
    for pc in intent.pool_counts:       
        lines += emit_pool_count(pc)
    for p in intent.properties:         
        lines += emit_property(p)
    return CompiledProgram(lines)