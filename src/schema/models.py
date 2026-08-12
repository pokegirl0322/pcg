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
    @model_validator(mode="after")          # <-- THE VALIDATOR GOES HERE
    def _target_required(self):
        if self.mode != "required" and self.target is None:
            raise ValueError("target is required unless mode == 'required'")
        return self


class ModeChange(BaseModel):
    mode: Optional[Literal["narrative_gating", "narrative_progress", "game_loss", "game_win"]] = None   # None => wildcard "_"
    polarity: Literal["require", "forbid"] = "require"


class ModeChangeCap(BaseModel):
    at_least: int


class Count(BaseModel):
    target: str
    comparator: Literal["!=", "<", ">"]
    value: int


class PoolCount(BaseModel):
    entity_index: int
    low: int
    high: int


class Property(BaseModel):
    property_name: str
    entity_index: int
    polarity: Literal["require", "forbid"] = "require"


class Intent(BaseModel):
    bounds: Bounds
    labels: list[Label] = []
    reading_requirements: list[ReadingRequirement] = []
    mode_changes: list[ModeChange] = []
    mode_change_caps: list[ModeChangeCap] = []
    counts: list[Count] = []
    pool_counts: list[PoolCount] = []
    properties: list[Property] = []
