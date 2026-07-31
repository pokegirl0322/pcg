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
    return CompiledProgram(lines)