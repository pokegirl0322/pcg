from typing import Literal, Optional
from pydantic import BaseModel


class Bounds(BaseModel):
    min_entities: int
    max_entities: int
    min_resources: int
    max_resources: int
    min_outcomes: int
    max_outcomes: int
    min_timers: int
    max_timers: int
    min_end_outcomes: int
    max_end_outcomes: int
    max_resource_change_per: int
    max_conditions_per: int


class Label(BaseModel):
    target_kind: Literal["entity", "resource"]
    index: int                       # e(1) -> 1,  r(2) -> 2
    name: str                        # "food", "composure"
    visibility: Optional[Literal["write", "private", "read", "read_only"]] = None


class ReadingRequirement(BaseModel):
    quality: str                     # e.g. "good", "sharing"  (validated later vs signatures)
    target: Optional[str] = None     # e.g. "resource(r(1))"; unused when mode == "required"
    mode: Literal["required", "constraint", "asserted"] = "constraint"


class Intent(BaseModel):
    bounds: Bounds
    labels: list[Label] = []
    reading_requirements: list[ReadingRequirement] = []