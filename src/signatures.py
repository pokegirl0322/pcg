# all 12 fixed bounds
BOUNDS_CONSTS = [
    "min_entities", "max_entities",
    "min_resources", "max_resources",
    "min_outcomes", "max_outcomes",
    "min_timers", "max_timers",
    "min_end_outcomes", "max_end_outcomes",
    "max_resource_change_per", "max_conditions_per",
]

#complete set of reading qualities, with compound readings listed how they would appear in asp
READING_QUALITIES = {
    "good", "bad", "help", "hurt", "chases", "flees", "sharing",
    "produces", "consumes", "costs", "survive", "dodge", "defend_against",
    "difficulty", "risk", "risk_reward", "hand_eye_coordination", "tradeoff",
    "maintenance", "grinding", "organization", "outcome_helps", "outcome_hurts",
    "stakes(high)", "stakes(low)", "goal(produce)", "goal(reduce)",
}

#colors, clear being the special empty amount
COLORS = {"red", "blue", "green", "yellow", "magenta", "orange"}

#mode changes
MODES = {"narrative_gating", "narrative_progress", "game_loss", "game_win"}

#control schemes
CONTROL_SCHEMES = {
    # indirect
    "click_and_drag", "orbit_the_cursor", "drawn_to_cursor",
    "repeled_from_cursor", "click_to_spin", "click_to_move",
    # direct
    "asteroids", "tank", "vertical", "horizontal", "cardinal",
}

#resource label visibility modes
VISIBILITIES = {"write", "private", "read", "read_only"}

#predicate arities; used to check for anomalies/unknown predicates
PREDICATE_ARITY = {
    "reading": 2, "required": 1, "label": None,  # label is 2 or 3
    "cooldown": 3, "monotonic": 2, "controlScheme": 2, "palette": 1,
    "initialize": 1, "synced": 2, "total_count": 2, "pool": 4,
    "precondition": 2, "result": 2, "action": 1, "allowed": 1,
    "entity_spawn_ok_loc": 1, "player_controls": 1, "computer_controls": 1,
    "player_controls_outcome": 1, "many": 1, "static": 1, "constant": 1,
    "frivolous": 1, "super_trivial": 1, "overlaps": 3,
}