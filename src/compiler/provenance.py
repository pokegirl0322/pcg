#compiler output types. every emitted line should know where it came from.

from dataclasses import dataclass


@dataclass
class Line:
    text: str        # the ASP line
    source: str      # provenance tag composed of what was plugged into the emittor.


@dataclass
class CompiledProgram:
    lines: list[Line]

    def text(self) -> str:
        #asp ready to write into a .lp file.
        return "\n".join(l.text for l in self.lines) + "\n"

    def provenance(self) -> dict[int, str]:
        # line number to source tag.
        return {i: l.source for i, l in enumerate(self.lines)}