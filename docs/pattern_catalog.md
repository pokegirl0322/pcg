# Gemini Intent Pattern Catalog

Derived from analysis of the intent files in upstream Gemini (external/Gemini/asp/intents/, commit e6ab676). Illustrative snippets are quoted minimally from the upstream repo for analysis purposes.

---

## Pattern: bounds  
**Description:** Declares the numeric generation bounds every intent sets.  
**Shape:** `#const <name> = <int>.`  
**Varies:** the integer values only.  
**Fixed:** the 12 constant names themselves (min/max entities, resources, outcomes, timers, end_outcomes, resource_change_per, conditions_per). Need to confirm if all files set all 12.  
**Occurrences:** dinner_intent (12/12), dummy_intent(12/12), dean_intent(12/12), lecture_intent(12/12), lecture_intent_attract(12/12)  

## Pattern: required_quality   
**Description:** Requires a named reading-quality to hold somewhere in the generated game.   
**Shape:** `required(<quality>).`   
**Varies:** the quality name which drawn from the readings.lp vocabulary (~25 values, e.g. sharing, maintenance, help, hurt, tradeoff...).   
**Occurrences:** dinner_intent (sharing, maintenance), dean_intent(survive, help, maintenance), lecture_intent(hand_eye_coordination, risk_reward, maintenance), lecture_intent_attract(maintenance)   

## Pattern: entity_label / resource_label  
**Description:** Assigns a display label, resources adds a visibility mode.  
**Shape:** `label(<entity_id>, <label>).` / `label(<resource_id>, <label>, <visibility>).`  
**Varies:** id, label; visibility (resource only: write | private | read | read_only(interpreter does not include)).  
**Occurrences:** dinner_intent (food, friend; satiation/write, though note the satiation label here is *conditional*, see label_rule), dean_intent (yourself, help, harm; composure/write, tension/read_only), lecture_intent(concentration/write; e1), lecture_intent_attract(e1)  

## Pattern: label_rule   
**Description:** Derive this label when this reading holds   
**Shape:** `label(<resource_id>, <label>, <visibility>) :- reading(<quality>, <target>). `  
**Varies:** resource_id, label, visibility, quality and target. resource form only seen so far, no conditional entity.    
**Occurrences:** dinner_intent(r(1),satiation,write,good,r(1)), lecture_intent(r(1),concentration,write,good,r(1)), lecture_intent_attract(r(1), concentration, write, good, r(1))   

## Pattern: forbidden_condition   
**Description:** No outcome in the generated game may be triggered by any comparison against the amount of the named color   
**Shape:** `:- condition(compare(_,amount(<color>),_)).`   
**Varies:** color, only clear observed so far.   
**Occurrences** dinner_intent(clear)   

## Pattern: required_reading   
**Description:** Requires a specific reading on a specific target.   
**Shape:** `:- not reading(<quality>, <target>).`    
**Varies:** quality; unary over resource/entity, special constants (game; player within relations), relational, and wildcard condition targets (control_event(_)).  
**Occurrences:** dinner_intent: good/resource (unary), sharing/relation (relational), maintenance/resource (unary), dean_intent: maintenance/resource (unary), survive/entity(unary), help/relation(relational), good/resource (unary), difficulty/resource (unary), lecture_intent: hand_eye_coordination/game (unary), risk_reward/`control_event(_)` (unary), good/resource (unary), maintenance/resource (unary); lecture_intent_attract: good/resource (unary), maintenance/resource (unary)   
**Note:** compound readings (goal(produce), stakes(high)) exist in readings.lp but no instance seen yet in files cataloged so far.   

## Pattern: label_enum   
**Description:** Three-line idiom that declares allowed labels, forbid any outside the set, require one to be assigned.   
**Shape:** `acceptable_labels(<a>;<b>).` + two enforcement constraints.   
**Varies:** the label set; the target resource.   
**Occurrences:** dinner_intent (appetite/bites on r(2)).  
**Note:** one schema entry → three emitted lines. Compiler owns all three.  

## Pattern: count_requirement   
**Description:** Pins how many instances of an entity exist.   
**Shape:** `:- total_count(<entity>, N), N <comparator> <value>.`   
**Varies:** entity, comparator (!=, >, < seen in comments), value.   
**Occurrences:** dinner_intent (e(2) != 3; commented-out >/< suggest range form intended by original authors).   

## Pattern: property_constraint   
**Description:** Requires or forbids named engine-derived property to hold for the entity   
**Shape:** `:- not <property>(entity(<entity>)).` \ `:- <property>(entity(<entity>)).`  
**Varies:** entity, property, polarity    
**Occurrences:** dinner_intent (require/constant/e(2)), dean_intent (forbid/many/e(1), require/computer_controls(e(2)))    

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
**Occurrences:** dinner_intent (require/narrative_gating), dean_intent (forbid/game_win) x2, lecture_intent(require/game_loss), lecture_intent_attract (require/game_loss) both lecture & dinner & attract appeared with mode_change_cap   

## Pattern: mode_change_cap   
**Description:** caps mode_change actions (of any mode) at <low> − 1.   
**Shape:** `:- <low> {action(mode_change(N))}.`   
**Varies:** low   
**Occurrences:** dinner_intent (2), lecture_intent (2), lecture_intent_attract(2) all appeared together with mode_change_constraint   

## Pattern: control_scheme_constraint  
**Description:** Forbids a generated game from using a given control scheme.  
**Shape:** `:- controlScheme(_,<control_scheme>).`  
**Varies:** control_scheme (listed in generation_atoms.lp: indirectControls: click_and_drag, orbit_the_cursor, drawn_to_cursor, repeled_from_cursor, click_to_spin, click_to_move; directControls: asteroids, tank, vertical, horizontal, cardinal)  
**Occurrences:** lecture_intent(orbit_the_cursor, repeled_from_cursor), lecture_intent_attract (orbit_the_cursor, repeled_from_cursor), both paired with forbidden_scheme_outcome  

## Pattern: forbidden_scheme_outcome  
**Description:** Forbids a generated game from having an outcome associated with a given control scheme.  
**Shape:** `:- outcome(outcome(<control_scheme>(_))).`  
**Varies:** control_scheme  
**Occurrences** lecture_intent(orbit_the_cursor, repeled_from_cursor), lecture_intent_attract (orbit_the_cursor, repeled_from_cursor) both paired with control_scheme_constraint  

## Pattern: forbidden_control_result  
**Description:** Forbids control events with a result modifying a resource in a given direction.  
**Shape:** `:- precondition(control_event(_),O), result(O,modify(<direction>,resource(<resource>))).`   
**Varies:** direction, resource   
**Occurrences** lecture_intent(increase/r(1)), lecture_intent_attract(increase/r(1))   

## Pattern: forbidden_trivial_result  
**Description:** Defines a named resource as not being able to be modified in a given direction by any free/trivial outcome  
**Shape:** `:- result(O, modify(<direction>,resource(<resource>))), super_trivial(O).`
**Varies:** direction, resource
**Occurrences:** lecture_intent_attract(increase/r(1))

## No pattern yet   
revisit if more than 2 files show these shapes.   
- **dinner_intent is_consumed block:** invents a new predicate (4 lines: 1 derivation + 3 enforcement constraints) encoding "resource gain must coincide with consuming the food entity."  
- **dinner_intent cooldown-conditioned label rules:** label assignment conditioned on cooldown() + a player_model. Could be a candidate for a future conditional label_rule variant.  
- **dean_intent opposite_results_on_overlap block** creates a supporting vocabulary fact, a derived predicate (based on two overlap preconditions and two result predicates) encoding that e(1) overlaps both e(2) and e(3) and that those overlaps produce opposite modifications to the same resource, and an integrity constraint requiring the derived predicate to hold.  
- **dean_intent outcome-cap block**: invents outcomes/1 using an aggregate assignment (`N = {outcome(O)}`) to count all generated outcomes, then enforces that the total does not exceed max_outcomes. The engine already bounds numbered outcomes through max_outcome(M), so this block captures all outcomes, including those outside the numbered series like control-scheme outcomes.
- **lecture_intent_attract attract_mode block**: Defines a required condition for an outcome where two entities positively overlap, the outcome has a good reading, and does not have a bad reading. The generated game is invalid unless this condition is satisfied. Interestingly similar to help rule in readings.lp beyond computer_controls condition?

## Anomalies  
dummy_intent: `:- not cooldown(_,_).` is an arity mismatch (engine defines cooldown/3); renders the file permanently UNSAT against current engine (verified by direct run, 0.00s solve). Possibly stale from an older engine version, or a deliberate scratch file as the name 'dummy' could support either. Will be considering required_existence style pattern if working file contains.   

## Coverage tracker
| File | Status |
|---|---|
| dinner_intent.lp | done |
| dummy_intent.lp | done |
| dean_intent.lp | done |
| lecture_intent.lp | done |
| lecture_intent_attract.lp | done |
