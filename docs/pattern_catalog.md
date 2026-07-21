# Gemini Intent Pattern Catalog

Derived from analysis of the intent files in upstream Gemini (external/Gemini/asp/intents/, commit e6ab676). Illustrative snippets are quoted minimally from the upstream repo for analysis purposes.

---

## Pattern: bounds  
**Description:** Declares the numeric generation bounds every intent sets.  
**Shape:** `#const <name> = <int>.`  
**Varies:** the integer values only.  
**Fixed:** the 12 constant names themselves (min/max entities, resources, outcomes, timers, end_outcomes, resource_change_per, conditions_per). Need to confirm if all files set all 12.  
**Occurrences:** dinner_intent (12/12), dummy_intent(12/12), dean_intent(12/12), lecture_intent(12/12), lecture_intent_attract(12/12), lecture_intent_avoid(12/12), lecture_intent_avoid_diff (12/12), lecture_intent_avoid_sim(12/12), lecture_intent_clear(12/12), lecture_intent_clear_diff (12/12), lecture_intent_drop(12/12)  

## Pattern: required_quality   
**Description:** Requires a named reading-quality to hold somewhere in the generated game.   
**Shape:** `required(<quality>).`   
**Varies:** the quality name which drawn from the readings.lp vocabulary (~25 values, e.g. sharing, maintenance, help, hurt, tradeoff...).   
**Occurrences:** dinner_intent (sharing, maintenance), dean_intent(survive, help, maintenance), lecture_intent(hand_eye_coordination, risk_reward, maintenance), lecture_intent_attract(maintenance), lecture_intent_avoid (hand_eye_coordination, maintenance), lecture_intent_avoid_diff (hand_eye_coordination, maintenance, risk_reward), lecture_intent_avoid_sim (hand_eye_coordination, maintenance, risk_reward), lecture_intent_clear (hand_eye_coordination), lecture_intent_clear_diff (hand_eye_coordination)     

## Pattern: entity_label / resource_label  
**Description:** Assigns a display label, resources adds a visibility mode.  
**Shape:** `label(<entity_id>, <label>).` / `label(<resource_id>, <label>, <visibility>).`  
**Varies:** id, label; visibility (resource only: write | private | read | read_only(interpreter does not include)).  
**Occurrences:** dinner_intent (food, friend; satiation/write, though note the satiation label here is *conditional*, see label_rule), dean_intent (yourself, help, harm; composure/write, tension/read_only), lecture_intent(concentration/write; e1), lecture_intent_attract(e1), lecture_intent_avoid(e1), lecture_intent_avoid_diff (e1), lecture_intent_avoid_sim (e1), lecture_intent_clear (e1), lecture_intent_clear_diff (e1), lecture_intent_drop (e1, concentration/write)   

## Pattern: label_rule   
**Description:** Derive this label when this reading holds   
**Shape:** `label(<resource_id>, <label>, <visibility>) :- reading(<quality>, <target>). `  
**Varies:** resource_id, label, visibility, quality and target. resource form only seen so far, no conditional entity.    
**Occurrences:** dinner_intent(r(1),satiation,write,good,r(1)), lecture_intent(r(1),concentration,write,good,r(1)), lecture_intent_attract(r(1), concentration, write, good, r(1)), lecture_intent_avoid(r(1), concentration, write, good, r(1)), lecture_intent_avoid_diff (r(1), concentration, write, good, r(1)), lecture_intent_avoid_sim (r(1), concentration, write, good, r(1))   

## Pattern: forbidden_condition   
**Description:** No outcome in the generated game may be triggered by any comparison against the amount of the named color   
**Shape:** `:- condition(compare(_,amount(<color>),_)).`   
**Varies:** color, only clear observed so far.   
**Occurrences** dinner_intent(clear), lecture_intent_avoid_diff (clear, believed to be legacy versions and likely dead under current engine.)   

## Pattern: required_reading   
**Description:** Requires a specific reading on a specific target.   
**Shape:** `:- not reading(<quality>, <target>).`    
**Varies:** quality; unary over resource/entity, special constants (game; player within relations), relational, and wildcard condition targets (control_event(_)).  
**Occurrences:** dinner_intent: good/resource (unary), sharing/relation (relational), maintenance/resource (unary), dean_intent: maintenance/resource (unary), survive/entity(unary), help/relation(relational), good/resource (unary), difficulty/resource (unary), lecture_intent: hand_eye_coordination/game (unary), risk_reward/`control_event(_)` (unary), good/resource (unary), maintenance/resource (unary); lecture_intent_attract: good/resource (unary), maintenance/resource (unary), lecture_intent_avoid: hand_eye_coordination/game (unary), good/resource (unary), maintenance/resource (unary), lecture_intent_avoid_diff: hand_eye_coordination/game (unary), risk_reward/`control_event(_)` (unary), good/resource (unary), maintenance/resource (unary), lecture_intent_avoid_sim: hand_eye_coordination/game (unary), risk_reward/`control_event(_)` (unary), good/resource (unary), maintenance/resource (unary); lecture_intent_clear: hand_eye_coordination/game (unary), lecture_intent_clear_diff: hand_eye_coordination/game (unary);   
**Note:** compound readings (goal(produce), stakes(high)) exist in readings.lp but no instance seen yet in files cataloged so far.   

## Pattern: label_enum   
**Description:** Three-line idiom that declares allowed labels, forbid any outside the set, require one to be assigned.   
**Shape:** `acceptable_labels(<a>;<b>).` + two enforcement constraints.   
**Varies:** the label set, the target resource.   
**Occurrences:** dinner_intent (appetite/bites on r(2)).  
**Note:** one schema entry produces 3 compiler lines.

## Pattern: count_requirement   
**Description:** Pins how many instances of an entity exist.   
**Shape:** `:- total_count(<entity>, N), N <comparator> <value>.`   
**Varies:** entity, comparator (!=, >, < seen in comments), value.   
**Occurrences:** dinner_intent (e(2) != 3; commented-out >/< suggest range form intended by original authors).   

## Pattern: property_constraint   
**Description:** Requires or forbids named engine-derived property to hold for the entity   
**Shape:** `:- not <property>(entity(<entity>)).` \ `:- <property>(entity(<entity>)).`  
**Varies:** entity, property, polarity    
**Occurrences:** dinner_intent (require/constant/e(2)), dean_intent (forbid/many/e(1), require/computer_controls(e(2))), lecture_intent_clear (require/player_controls(e(1)), require/computer_controls(e(2))), lecture_intent_clear_diff (require/player_controls(e(1)), require/computer_controls(e(2))), lecture_intent_drop(require/player_controls(e(1)), require/computer_controls(e(2)))    

## Pattern: entity_relationship_requirement  
**Description:** Defines a required binary relationship between entities  
**Shape:** `:- not <relationship>(entity(<entity>),entity(<entity>)).`  
**Varies:** relationship, entities (only same_movement observed so far)  
**Occurrences:** dean_intent (same_movement/e(2)/e(3))  

## Pattern: forbidden_pool_count   
**Description:** Forbids the named entity's number of spawn pools from falling within [<low>, <high>], inclusive. Observed use: low = high = 1, i.e., never exactly one pool, must be zero or several   
**Shape:** `:- <low> {pool(entity(<entity>),_,_,_)} <high>.`   
**Varies:** low, entity, high   
**Occurrences:** dinner_intent (e(1), 1..1)   

## Pattern: mode_change_constraint   
**Description:** Requires or forbids the game to contain the named mode change.   
**Shape:** `:- not action(mode_change(<mode>)).` \ `:- action(mode_change(<mode>)).`  
**Varies:** mode: can consist of narrative_gating, narrative_progress, game_loss, game_win (as in generation_atoms.lp)   
**Occurrences:** dinner_intent (require/narrative_gating), dean_intent (forbid/game_win) x2, lecture_intent(require/game_loss), lecture_intent_attract (require/game_loss), lecture_intent_avoid (require/game_loss), lecture_intent_avoid_diff (require/game_loss), lecture_intent_avoid_sim (require/game_loss), lecture_intent_clear(require/game_loss), lecture_intent_clear_diff (require/game_loss), lecture_intent_drop(require/game_loss) all but dean_intent appeared with mode_change_cap   
**Note:** shape is similar to require_draw and require_clear, and could be abstracted to `:- not action(<action_term>)` including polarity. Choice was made to not abstract considering different arities.

## Pattern: require_draw  
**Description:** Requires a given entity to be drawn  
**Shape:** `:- not action(draw(entity(<entity>),_)).`  
**Varies:** entity  
**Occurrences:** lecture_intent_clear (e(2)), lecture_intent_clear_diff (e(2)), lecture_intent_drop(e(1))   

## Pattern: require_clear  
**Description:** Requires a given entity to be cleared.  
**Shape:** `:- not action(clear(entity(<entity>))).`  
**Varies:** entity   
**Occurrences:** lecture_intent_clear (e(1)), lecture_intent_drop (e(2))   

## Pattern: mode_change_cap   
**Description:** caps mode_change actions (of any mode) at <low> − 1.   
**Shape:** `:- <low> {action(mode_change(N))}.`   
**Varies:** low   
**Occurrences:** dinner_intent (2), lecture_intent (2), lecture_intent_attract(2), lecture_intent_avoid (2), lecture_intent_avoid_diff (2), lecture_intent_avoid_sim (2), lecture_intent_clear(2), lecture_intent_clear_diff (2), lecture_intent_drop(2) all appeared together with mode_change_constraint   
**Note:** similar to forbidden pool count and similarity checking predicates in lecture_intent_avoid_diff, consider generalizing? (could be something like forbid the count of matching atoms from reaching N)

## Pattern: control_scheme_constraint  
**Description:** Forbids a generated game from using a given control scheme.  
**Shape:** `:- controlScheme(_,<control_scheme>).`  
**Varies:** control_scheme (listed in generation_atoms.lp: indirectControls: click_and_drag, orbit_the_cursor, drawn_to_cursor, repeled_from_cursor, click_to_spin, click_to_move; directControls: asteroids, tank, vertical, horizontal, cardinal)  
**Occurrences:** lecture_intent(orbit_the_cursor, repeled_from_cursor), lecture_intent_attract (orbit_the_cursor, repeled_from_cursor), lecture_intent_avoid (orbit_the_cursor, repeled_from_cursor), lecture_intent_clear (orbit_the_cursor, repeled_from_cursor), lecture_intent_drop (orbit_the_cursor, repeled_from_cursor) all paired with forbidden_scheme_outcome  

## Pattern: forbidden_scheme_outcome  
**Description:** Forbids a generated game from having an outcome associated with a given control scheme.  
**Shape:** `:- outcome(outcome(<control_scheme>(_))).`  
**Varies:** control_scheme  
**Occurrences** lecture_intent(orbit_the_cursor, repeled_from_cursor), lecture_intent_attract (orbit_the_cursor, repeled_from_cursor), lecture_intent_avoid (orbit_the_cursor, repeled_from_cursor), lecture_intent_clear (orbit_the_cursor, repeled_from_cursor), lecture_intent_drop (orbit_the_cursor, repeled_from_cursor) all paired with control_scheme_constraint  

## Pattern: forbidden_control_result  
**Description:** Forbids control events with a result modifying a resource in a given direction.  
**Shape:** `:- precondition(control_event(_),O), result(O,modify(<direction>,resource(<resource>))).`   
**Varies:** direction, resource   
**Occurrences** lecture_intent(increase/r(1)), lecture_intent_attract(increase/r(1)), lecture_intent_avoid (increase/r(1)), lecture_intent_clear (increase/r(1)), lecture_intent_drop (increase/r(1))   

## Pattern: forbidden_trivial_result  
**Description:** Defines a named resource as not being able to be modified in a given direction by any free/trivial outcome   
**Shape:** `:- result(O, modify(<direction>,resource(<resource>))), super_trivial(O).`  
**Varies:** direction, resource  
**Occurrences:** lecture_intent_attract(increase/r(1)), lecture_intent_avoid (increase/r(1)), lecture_intent_clear (increase/r(1)), lecture_intent_drop (increase/r(1))    

## Pattern: result_form_constraint  
**Description:** Forbids any generated game from containing a result that sets some value to a given color  
**Shape:** `:- result(_, set_value(_,amount(<color>))).`  
**Varies:** color  
**Occurrences:** lecture_intent_avoid_diff (clear)  

## Pattern: palette_assignment  
**Description:** Assigns a color palette based on given color.  
**Shape:** `palette(<color>)`  
**Varies:** color  
**Occurrences:** lecture_intent_clear (blue), lecture_intent_clear_diff (blue), lecture_intent_drop (blue)  

## Pattern: initialize_action
**Description:** defines a declarative initialization rule that binds a resource to a baseline numeric constant at the game's initial state  
**Shape:** `initialize(set_value(resource(<resource>),scalar(<value>)))`  
**Varies:** resource, value  
**Occurrences:** lecture_intent_clear (r(1)/0), lecture_intent_clear_diff (r(1)/0), lecture_intent_drop (r(1)/10)

## Pattern: allowed_frivolous  
**Description:** Whitelists a given frivolous never-compared resource  
**Shape:** `allowed(frivolous(resource(<resource>)))`  
**Varies:** resource
**Occurrences:** lecture_intent_clear (r(1)), lecture_intent_clear_diff (r(1)), lecture_intent_drop (r(1))

## Pattern: require_synced
**Description:** requires a given resource and color amount to be synced.
**Shape:** `:- not synced(resource(<resource>),amount(<color>))`
**Varies:** resource, color
**Occurrences:** lecture_intent_clear(r(1)/clear), lecture_intent_clear_diff (r(1)/clear), lecture_intent_drop (r(1)/blue)

## No pattern yet   
revisit if more than 2 files show these shapes.   
- **dinner_intent is_consumed block:** invents a new predicate (4 lines: 1 derivation + 3 enforcement constraints) encoding "resource gain must coincide with consuming the food entity."  
- **dinner_intent cooldown-conditioned label rules:** label assignment conditioned on cooldown() + a player_model. Could be a candidate for a future conditional label_rule variant.  
- **dean_intent opposite_results_on_overlap block** creates a supporting vocabulary fact, a derived predicate (based on two overlap preconditions and two result predicates) encoding that e(1) overlaps both e(2) and e(3) and that those overlaps produce opposite modifications to the same resource, and an integrity constraint requiring the derived predicate to hold.   
- **dean_intent outcome-cap block**: invents outcomes/1 using an aggregate assignment (`N = {outcome(O)}`) to count all generated outcomes, then enforces that the total does not exceed max_outcomes. The engine already bounds numbered outcomes through max_outcome(M), so this block captures all outcomes, including those outside the numbered series like control-scheme outcomes.  
- **lecture_intent_attract attract_mode block**: Defines a required condition for an outcome where two entities positively overlap, the outcome has a good reading, and does not have a bad reading. The generated game is invalid unless this condition is satisfied. Interestingly similar to help rule in readings.lp beyond computer_controls condition?  
- **lecture_intent_avoid attract_mode block**: cross-referencing attract_mode block in lecture_intent_attract as this is simply a variation that differs only in the required reading-condition block. seen a second time in lecture_intent_avoid_diff and lecture_intent_avoid_sim. considering turning into a pattern once all other lecture_intent files have been read through.
- **lecture_intent_clear out_of_players_control block**: Invents the predicate, derivation + enforcement, encoding that a game element is considered out of the player's control if it relies on a specific outcome, and the player has no control over that outcome. This block appears in lecture_intent_clear_diff as well.
- **lecture_intent_clear lose_if_too_high block**: Also invents a predicate, derivation and enforcement. Encodes the triggering of an automatic loss if a specific tracked value becomes too high. This block appears in lecture_intent_clear_diff as well.
- **lecture_intent_drop lose_if_too_low block** same shape as lose_if_too_high block, encoding triggering of automatic loss if specific value becomes too low.

## Anomalies  
dummy_intent: `:- not cooldown(_,_).` is an arity mismatch (engine defines cooldown/3); renders the file permanently UNSAT against current engine (verified by direct run, 0.00s solve). Possibly stale from an older engine version, or a deliberate scratch file as the name 'dummy' could support either. Will be considering required_existence style pattern if working file contains.    

## Generated Constructs   
The `_diff` intent family likely appears to contain machine-generated variation rather than hand-authored intent specifications (checked with simulate.py & resulting generated game files). These files include a serialized transcription of a previously generated game through old_* predicates, along with similarity-checking predicates (same_init, same_tick, same_cause_effect), constraints on the new game that reference mangled names and cardinality constraints that are meant to limit overlap between the previous and new generated game. lecture_intent_avoid_sim only has the constraints on the new game referencing mangled names.  

These constructs are excluded from the prompt schema because they are produced by the generation pipeline rather than derived from natural language intent descriptions. The schema only models constructs that an LLM could reasonably generate from a prompt.  

## Coverage tracker
| File | Status |
|---|---|
| dinner_intent.lp | done |
| dummy_intent.lp | done |
| dean_intent.lp | done |
| lecture_intent.lp | done |
| lecture_intent_attract.lp | done |
| lecture_intent_avoid.lp | done |
| lecture_intent_avoid_diff.lp | done |
| lecture_intent_avoid_sim.lp | done |
| lecture_intent_clear.lp | done |
| lecture_intent_clear_diff.lp | done |
| lecture_intent_drop | done |
