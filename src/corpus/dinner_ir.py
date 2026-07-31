#dinner_intent.lp but handwritten as an ir
#currently skipping conditional labels, label_enum, and is_consumed block to test full pipline
#TODO LATER

from schema.models import Intent, Bounds, Label, ReadingRequirement

dinner = Intent(
    bounds=Bounds(
        min_entities=1, max_entities=2,
        min_resources=1, max_resources=2,
        min_outcomes=2, max_outcomes=6,
        min_timers=0, max_timers=2,
        min_end_outcomes=1, max_end_outcomes=1,
        max_resource_change_per=2, max_conditions_per=2,
    ),
    labels=[
        Label(target_kind="entity", index=1, name="food"),
        Label(target_kind="entity", index=2, name="friend"),
    ],
    reading_requirements=[
        ReadingRequirement(quality="sharing", mode="required"),
        ReadingRequirement(quality="maintenance", mode="required"),
        ReadingRequirement(quality="good", target="resource(r(1))", mode="constraint"),
        ReadingRequirement(quality="sharing",
                           target="relation(entity(e(1)),entity(e(2)))", mode="constraint"),
        ReadingRequirement(quality="maintenance", target="resource(r(1))", mode="constraint"),
    ],
)