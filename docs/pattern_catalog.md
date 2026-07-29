# Gemini Intent Pattern Catalog

Derived from analysis of the intent files in upstream Gemini (external/Gemini/asp/intents/, commit e6ab676). Illustrative snippets are quoted minimally from the upstream repo for analysis purposes.

---

## Pattern: bounds
**Description:** Declares the numeric generation bounds every intent sets.  
**Shape:** `#const <name> = <int>.`  
**Varies:** the integer values only.  
**Fixed:** the 12 constant names themselves (min/max entities, resources, outcomes, timers, end_outcomes, resource_change_per, conditions_per). Need to confirm if all files set all 12.  
**Occurrences:** dinner_intent (12/12), dummy_intent(12/12), dean_intent(12/12), lecture_intent(12/12), lecture_intent_attract(12/12), lecture_intent_avoid(12/12), lecture_intent_avoid_diff (12/12), lecture_intent_avoid_sim(12/12), lecture_intent_clear(12/12), lecture_intent_clear_diff (12/12), lecture_intent_drop(12/12), new_dean_intent (12/12), new_un_intent (12/12), scrubbing_intent (12/12), scrubbing_intent_diff (12/12), travel_intent (12/12)  

## Pattern: required_quality
**Description:** Requires a named reading-quality to hold somewhere in the generated game.  
**Shape:** `required(<quality>).`  
**Varies:** the quality name which drawn from the readings.lp vocabulary (~25 values, e.g. sharing, maintenance, help, hurt, tradeoff...).  
**Occurrences:** dinner_intent (sharing, maintenance), dean_intent(survive, help, maintenance), lecture_intent(hand_eye_coordination, risk_reward, maintenance), lecture_intent_attract(maintenance), lecture_intent_avoid (hand_eye_coordination, maintenance), lecture_intent_avoid_diff (hand_eye_coordination, maintenance, risk_reward), lecture_intent_avoid_sim (hand_eye_coordination, maintenance, risk_reward), lecture_intent_clear (hand_eye_coordination), lecture_intent_clear_diff (hand_eye_coordination), new_un_intent(maintenance), scrubbing_intent(maintenance), scrubbing_intent_diff(maintenance), travel_intent(tradeoff)  

## Pattern: entity_label / resource_label
**Description:** Assigns a display label, resources adds a visibility mode.  
**Shape:** `label(<entity_id>, <label>).` / `label(<resource_id>, <label>, <visibility>).`  
**Varies:** id, label; visibility (resource only: write | private | read | read_only(interpreter does not include)).  
**Occurrences:** dinner_intent (food, friend; satiation/write, though note the satiation label here is conditional, see label_rule), dean_intent (yourself, help, harm; composure/write, tension/read_only), lecture_intent(concentration/write; e1), lecture_intent_attract(e1), lecture_intent_avoid(e1), lecture_intent_avoid_diff (e1), lecture_intent_avoid_sim (e1), lecture_intent_clear (e1), lecture_intent_clear_diff (e1), lecture_intent_drop (e1, concentration/write), new_dean_intent(tension/read_only, power/write), new_un_intent(e1, e2, e3; confidence/write), scrubbing_intent(effort/write on r(1)), scrubbing_intent_diff(effort/write on r(1)), travel_intent(money/write on r1, co2/write on r2, fame/write on r3)

## Pattern: label_rule
**Description:** Derive this label when this reading holds  
**Shape:** `label(<resource_id>, <label>, <visibility>) :- reading(<quality>, <target>).`   
**Varies:** resource_id, label, visibility, quality and target. resource form only seen so far, no conditional entity.  
**Occurrences:** dinner_intent(r(1),satiation,write,good,r(1)), lecture_intent(r(1),concentration,write,good,r(1)), lecture_intent_attract(r(1), concentration, write, good, r(1)), lecture_intent_avoid(r(1), concentration, write, good, r(1)), lecture_intent_avoid_diff (r(1), concentration, write, good, r(1)), lecture_intent_avoid_sim (r(1), concentration, write, good, r(1)),

## Pattern: many_label_constraint
**Description:** Derive this label when the many condition holds  
**Shape:** `label(entity(<entity>), <label>) :- many(entity(<entity)).` / `label(entity(<entity>), <label>) :- not many(entity(<entity)).`  
**Varies:** polarity, entity, label  
**Occurrences:** new_dean_intent(required/e(1)/emma, forbid/e(1)/argument, required/e(2)/dean, forbid/e(2)/argument)  

## Pattern: forbidden_compare_precondition  
**Description:** Forbids outcomes from containing comparison preconditions against a specified target.  
**Shape:** `:- precondition(compare(_,<target>),_).` / `:- precondition(compare(_,<target>,_),_).` / `:- precondition(compare(_,_,<target>),_).`  
**Varies:** comparison target (currently `amount(<color>)` and `resource(<resource>)`), argument position.  
**Occurrences:** dinner_intent(amount(clear)), lecture_intent_avoid_diff(amount(clear)), new_dean_intent(resource(r(2)))  

## Pattern: required_reading
**Description:** Requires a specific reading on a specific target.  
**Shape:** `:- not reading(<quality>, <target>).`  
**Varies:** quality; unary over resource/entity, special constants (game; player within relations), relational, and wildcard condition targets (`control_event(_)`).  
**Occurrences:** dinner_intent: good/resource (unary), sharing/relation (relational), maintenance/resource (unary), dean_intent: maintenance/resource (unary), survive/entity(unary), help/relation(relational), good/resource (unary), difficulty/resource (unary), lecture_intent: hand_eye_coordination/game (unary), risk_reward/`control_event(_)` (unary), good/resource (unary), maintenance/resource (unary); lecture_intent_attract: good/resource (unary), maintenance/resource (unary), lecture_intent_avoid: hand_eye_coordination/game (unary), good/resource (unary), maintenance/resource (unary), lecture_intent_avoid_diff: hand_eye_coordination/game (unary), risk_reward/`control_event(_)` (unary), good/resource (unary), maintenance/resource (unary), lecture_intent_avoid_sim: hand_eye_coordination/game (unary), risk_reward/control_event(_) (unary), good/resource (unary), maintenance/resource (unary); lecture_intent_clear: hand_eye_coordination/game (unary), lecture_intent_clear_diff: hand_eye_coordination/game (unary); new_dean_intent: difficulty/resource (unary), , new_un_intent: produces/relation (relational), consumes/relation (relational)    
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
**Occurrences:** dinner_intent (require/constant/e(2)), dean_intent (forbid/many/e(1), require/computer_controls(e(2))), lecture_intent_clear (require/player_controls(e(1)), require/computer_controls(e(2))), lecture_intent_clear_diff (require/player_controls(e(1)), require/computer_controls(e(2))), lecture_intent_drop(require/player_controls(e(1)), require/computer_controls(e(2))), new_dean_intent(forbid/computer_controls(e(1))), new_un_intent(forbid/many/e(1), require/player_controls(e1), forbid/player_controls(e2), forbid/player_controls(e3), forbid/frivolous/r(1))  

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
**Shape:** `:- not action(mode_change(<mode>)).` \ `:- action(mode_change(<mode>)).` \ `:- action(mode_change(_)).`  
**Varies:** mode: can consist of narrative_gating, narrative_progress, game_loss, game_win (as in generation_atoms.lp) or a wildcard forbidding any mode change.    
**Occurrences:** dinner_intent (require/narrative_gating), dean_intent (forbid/game_win) x2, lecture_intent(require/game_loss), lecture_intent_attract (require/game_loss), lecture_intent_avoid (require/game_loss), lecture_intent_avoid_diff (require/game_loss), lecture_intent_avoid_sim (require/game_loss), lecture_intent_clear(require/game_loss), lecture_intent_clear_diff (require/game_loss), lecture_intent_drop(require/game_loss), scrubbing_intent(forbid/wildcard), travel_intent(forbid/wildcard) all but dean_intent, scrubbing_intent and travel_intent appeared with mode_change_cap  
**Note:** shape is similar to require_draw and require_clear, and could be abstracted to :- not action(<action_term>) including polarity. Choice was made to not abstract considering different arities.

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
**Occurrences:** lecture_intent(orbit_the_cursor, repeled_from_cursor), lecture_intent_attract (orbit_the_cursor, repeled_from_cursor), lecture_intent_avoid (orbit_the_cursor, repeled_from_cursor), lecture_intent_clear (orbit_the_cursor, repeled_from_cursor), lecture_intent_drop (orbit_the_cursor, repeled_from_cursor), new_dean_intent (orbit_the_cursor), new_un_intent (orbit_the_cursor) all paired with forbidden_scheme_outcome

## Pattern: forbidden_scheme_outcome
**Description:** Forbids a generated game from having an outcome associated with a given control scheme.  
**Shape:** `:- outcome(outcome(<control_scheme>(_))).`  
**Varies:** control_scheme  
**Occurrences:** lecture_intent(orbit_the_cursor, repeled_from_cursor), lecture_intent_attract (orbit_the_cursor, repeled_from_cursor), lecture_intent_avoid (orbit_the_cursor, repeled_from_cursor), lecture_intent_clear (orbit_the_cursor, repeled_from_cursor), lecture_intent_drop (orbit_the_cursor, repeled_from_cursor), new_dean_intent(orbit_the_cursor), new_un_intent (orbit_the_cursor) all paired with control_scheme_constraint

## Pattern: forbidden_trigger_result
**Description:** Forbids outcomes triggered by a given precondition type from modifying a resource in a specified direction.  
**Shape:** `:- precondition(<trigger>,O), result(O,modify(<direction>,resource(<resource>))).` / `:- precondition(<trigger>,O), result(O,modify(<direction>,resource(<resource>),_)).`  
**Varies:** trigger, direction, resource (resource may be a specific id or wildcard `_`, forbidding modification of any resource).  
**Occurrences:** lecture_intent(`control_event(_)`/increase/r(1)), lecture_intent_attract(`control_event(_)`/increase/r(1)), lecture_intent_avoid (`control_event(_)`/increase/r(1)), lecture_intent_clear (`control_event(_)`/increase/r(1)), lecture_intent_drop (`control_event(_)`/increase/r(1)), new_dean_intent(`control_event(_)`/decrease/r(2), control_event(`click(_))`/`_`/r(2), tick/decrease/r(2))), new_un_intent(control_event(click(entity(e(2))))/decrease/r(2), `control_event(_)`/decrease/r(1), control_event(_)/increase/r(1)), scrubbing_intent(`control_event(_)`/increase/wildcard)    
**Note:** the `tick` trigger's precondition is `precondition(tick,tick) :- outcome(tick).` — a trivial self-reference — so intent files write the collapsed form `:- result(tick,modify(...))` instead of the full `precondition(tick,O), result(O,modify(...))` form.

## Pattern: forbidden_trivial_result
**Description:** Defines a named resource as not being able to be modified in a given direction by any free/trivial outcome  
**Shape:** `:- result(O,modify(<direction>,resource(<resource>))), super_trivial(O).` / `:- result(O,modify(<direction>,resource(<resource>),_)), super_trivial(O).`  
**Varies:** direction, resource  
**Occurrences:** lecture_intent_attract(increase/r(1)), lecture_intent_avoid (increase/r(1)), lecture_intent_clear (increase/r(1)), lecture_intent_drop (increase/r(1)), new_dean_intent(increase/r(2))  

## Pattern: result_form_constraint
**Description:** Forbids any generated game from containing a result of a given form affecting a given target, unconditionally.  
**Shape:** `:- result(_, set_value(_,amount(<color>))).` / `:- result(_,modify(_,<target>)).`  
**Varies:** result form (set_value | modify), color/target.  
**Occurrences:** lecture_intent_avoid_diff (set_value/clear), new_un_intent(modify/property(_,health))

## Pattern: entity_spawn_location_allowlist
**Description:** Grants a named entity special permission to be used as a spawn location.  
**Shape:** `entity_spawn_ok_loc(entity(<entity>)).`  
**Varies:** entity.  
**Occurrences:** new_un_intent(e(2))

## Pattern: required_existence
**Description:** Requires the generated game to contain at least one instance of a given generation-bound type.  
**Shape:** `:- not <type>(_).`  
**Varies:** type (entity | resource | outcome | timer).  
**Occurrences:** new_un_intent(resource)

## Pattern: palette_assignment
**Description:** Assigns a color palette based on given color.  
**Shape:** `palette(<color>)`  
**Varies:** color  
**Occurrences:** lecture_intent_clear (blue), lecture_intent_clear_diff (blue), lecture_intent_drop (blue), scrubbing_intent(orange), scrubbing_intent_diff(orange)

## Pattern: initialize_action
**Description:** defines a declarative initialization rule that binds a resource to a baseline numeric constant at the game's initial state  
**Shape:** `initialize(set_value(resource(<resource>),scalar(<value>))).`  
**Varies:** resource, value  
**Occurrences:** lecture_intent_clear (r(1)/0), lecture_intent_clear_diff (r(1)/0), lecture_intent_drop (r(1)/10), scrubbing_intent(r(1)/0), scrubbing_intent_diff(r(1)/0)

## Pattern: allowed_property
**Description:** Whitelists a target as having a given permissive property, opting it out of default engine restrictions.  
**Shape:** `allowed(<property>(<target>)).`  
**Varies:** property (frivolous | monotonic | superfluous | frivolous_color, so far), target (resource(<id>) or bare color).  
**Occurrences:** lecture_intent_clear(frivolous/r(1)), lecture_intent_clear_diff(frivolous/r(1)), lecture_intent_drop(frivolous/r(1)), new_dean_intent (frivolous/r(1), frivolous/r(2)), scrubbing_intent(frivolous/resource(r1), monotonic/orange, monotonic/resource(r1), superfluous/resource(r1), frivolous_color/orange, frivolous_color/clear), scrubbing_intent_diff(monotonic/orange, monotonic/resource(r1), monotonic/r1(bare), superfluous/resource(r1)), travel_intent(monotonic/resource(r1), monotonic/resource(r2), monotonic/resource(r3)) 

## Pattern: label_mutex  
**Description:** Prevents two specified entities from simultaneously being assigned the same label.  
**Shape:** `:- label(entity(<entity1>),<label>), label(entity(<entity2>),<label>).`  
**Varies:** entities, label.  
**Occurrences:** new_dean_intent(argument)

## Pattern: precondition_type_mutex
**Description:** Forbids a single outcome from having preconditions of two specified types simultaneously.  
**Shape:** `:- precondition(<type1>(_),O), precondition(<type2>(...),O).`  
**Varies:** the two precondition-type constructors involved. Closed enumeration per generation.lp: `control_event(button(_,_))`, `control_event(click(_))`, compare(Polarity,RESOURCE), compare(Polarity,amount(Color),R), compare(Polarity,amount(Color),scalar(A)), overlaps(E1,E2,P), timer_elapsed(Timer), tick.  
**Occurrences:** new_dean_intent(`control_event(_)`/`overlaps(_,_,_))`  

## Pattern: result_direction_constraint  
**Description:** Requires or forbids the existence of an outcome modifying a given target in a specified direction.  
**Shape:** `:- not goes_up(<target>).` / `:- not goes_down(<target>).` / `:- goes_up(<target>).` / `:- goes_down(<target>).`  
**Varies:** polarity (require | forbid), direction (increase | decrease), target (currently `resource(<resource>)` and `property(_,<property>)`).  
**Occurrences:** new_dean_intent(require/increase/resource(r(2)), require/decrease/resource(r(2)), forbid/increase/property(`_,health`), forbid/decrease/property(`_,health`))  
**Note:** `goes_up/1` and `goes_down/1` are helper predicates and implementation detail; the schema-visible construct is the integrity constraint.  

## Pattern: global_property_constraint  
**Description:** Requires or forbids an engine-derived property for every entity in the generated game.  
**Shape:** `:- entity(E), <property>(E).` / `:- entity(E), not <property>(E).`  
**Varies:** property, polarity.  
**Occurrences:** new_dean_intent(forbid/static)  

## Pattern: require_synced
**Description:** requires a given resource and color amount to be synced.  
**Shape:** :- not synced(resource(<resource>),amount(<color>))  
**Varies:** resource, color  
**Occurrences:** lecture_intent_clear(r(1)/clear), lecture_intent_clear_diff (r(1)/clear), lecture_intent_drop (r(1)/blue)

## Pattern: forbidden_controlled_spawn
**Description:** Forbids a player-controlled outcome from adding (spawning) an entity.  
**Shape:** `:- outcome(O), result(O,add(<entity>,_,_)), player_controls_outcome(O).`  
**Varies:** entity  
**Occurrences:** new_un_intent (x2, generic form)  

## Pattern: forbidden_trigger_delete
**Description:** Forbids deletion of a given entity when a specified precondition holds on the triggering outcome.  
**Shape:** `:- result(O,delete(entity(<entity>))), precondition(<condition>,O).`  
**Varies:** entity, condition.  
**Occurrences:** new_un_intent(e(3)/le(resource(r(1)),_))  
**Note:** the observed occurrence uses bare le(...) as a precondition type, which doesn't match generation.lp's enumerated precondition constructors (compare((ge;le),...) is the real form). Likely legacy/dead under current engine. Pattern shape may still recur with a valid precondition form.

## Pattern: forbidden_frivolous
**Description:** Forbids a named resource from being derived as frivolous.  
**Shape:** `:- frivolous(resource(<resource>)).`  
**Varies:** resource.  
**Occurrences:** new_un_intent(r(1))  
**Note:** merge with allowed frivolous??

## Pattern: monotonic_requirement
**Description:** Requires a target to change monotonically in a specified direction over the course of the game.  
**Shape:** `:- not monotonic(<target>,<direction>).`  
**Varies:** target (resource(<id>) or bare color), direction (increase | decrease).  
**Occurrences:** scrubbing_intent(orange/decrease, resource(r(1))/increase), scrubbing_intent_diff(orange/decrease, resource(r(1))/increase)  

## Pattern: required_initialize
**Description:** Requires or forbids a specific initialize fact.  
**Shape:** `:- not initialize(<term>).` / `:- initialize(<term>).`  
**Varies:** polarity (require | forbid), the initialize term (may contain wildcards).  
**Occurrences:** scrubbing_intent(require/fill(all,orange)), scrubbing_intent_diff(require/fill(all,orange), forbid/set_draggable(_,true))

## Pattern: asserted_reading
**Description:** Directly asserts that a reading holds, as a fact, rather than requiring or deriving it conditionally.  
**Shape:** `reading(<quality>,<target>).`  
**Varies:** quality, target.  
**Occurrences:** scrubbing_intent(bad/orange), scrubbing_intent_diff(bad/orange)  
**Note:** only target observed thus far is a color.

## Pattern: required_property_existence
**Description:** Requires that some object in the generated game have a given property.  
**Shape:** `:- not <property>(_).`  
**Varies:** property.  
**Occurrences:** scrubbing_intent(player_controls), scrubbing_intent_diff(player_controls)  

## Pattern: forbidden_action
**Description:** Forbids any outcome from having a given action/result form, expressed via the action/1 predicate rather than result/2.  
**Shape:** `:- action(<action_term>).`  
**Varies:** action term with modify(<direction>,<target>) observed in both 2-arity (direction fixed) and 3-arity (direction wildcard, second resource wildcard) forms.  
**Occurrences:** travel_intent(modify(decrease,resource(r2)), modify(decrease,resource(r3)), modify(`_`,resource(r1),`_`), modify(`_`,resource(r2),`_`), modify(`_`,resource(r3),`_`))  
**Note:** possible future merge with result_form_constraint.

## No pattern yet
revisit if more than 2 files show these shapes.  
- dinner_intent is_consumed block: invents a new predicate (4 lines: 1 derivation + 3 enforcement constraints) encoding "resource gain must coincide with consuming the food entity."
- dinner_intent cooldown-conditioned label rules: label assignment conditioned on cooldown() + a player_model. Could be a candidate for a future conditional label_rule variant.
- dean_intent opposite_results_on_overlap block creates a supporting vocabulary fact, a derived predicate (based on two overlap preconditions and two result predicates) encoding that e(1) overlaps both e(2) and e(3) and that those overlaps produce opposite modifications to the same resource, and an integrity constraint requiring the derived predicate to hold.
- dean_intent outcome-cap block: invents outcomes/1 using an aggregate assignment (N = {outcome(O)}) to count all generated outcomes, then enforces that the total does not exceed max_outcomes. The engine already bounds numbered outcomes through max_outcome(M), so this block captures all outcomes, including those outside the numbered series like control-scheme outcomes.
- lecture_intent_attract attract_mode block: Defines a required condition for an outcome where two entities positively overlap, the outcome has a good reading, and does not have a bad reading. The generated game is invalid unless this condition is satisfied. Interestingly similar to help rule in readings.lp beyond computer_controls condition?
- lecture_intent_avoid attract_mode block: cross-referencing attract_mode block in lecture_intent_attract as this is simply a variation that differs only in the required reading-condition block. seen a second time in lecture_intent_avoid_diff and lecture_intent_avoid_sim. considering turning into a pattern once all other lecture_intent files have been read through.
- lecture_intent_clear out_of_players_control block: Invents the predicate, derivation + enforcement, encoding that a game element is considered out of the player's control if it relies on a specific outcome, and the player has no control over that outcome. This block appears in lecture_intent_clear_diff as well.
- lecture_intent_clear lose_if_too_high block: Also invents a predicate, derivation and enforcement. Encodes the triggering of an automatic loss if a specific tracked value becomes too high. This block appears in lecture_intent_clear_diff as well.
- lecture_intent_drop lose_if_too_low block same shape as lose_if_too_high block, encoding triggering of automatic loss if specific value becomes too low.
- scrubbing_intent result co-occurrence pair: `:- result(O,modify(increase,_)), not result(O,clear(_)). / :- result(O,clear(_)), not result(O,modify(increase,_)).` is a biconditional pair requiring that any outcome modifying-increase also clears, and vice versa, on the same outcome. Only one occurrence (as a matched pair),
- scrubbing_intent player_model-conditioned result requirement: `:- player_model(O,player_must_do), not result(O,modify(increase,resource(r(1)))).` requires that any outcome tagged player_must_do also increases r(1). This is also present in scrubbing_intent_diff.lp.
- travel_intent choice/tradeoff block: A large bespoke mechanic (~13 lines) defining two mutually-exclusive derived labels, `choice(O,higher)` and `choice(O,lower)`, both nondeterministically assignable to any outcome matching the same body (decrease r1, increase r2, increase r3). Enforces the mutual exclusion between the two labels on one outcome with exactly one outcome having carry each label (upper-bound-1 and lower-bound-1 cardinality constraints together); any outcome increasing r2 or r3 must carry a choice label; a derived `similar_conditions` predicate requiring the higher- and lower-labeled outcomes to share a trigger type (both control_event(`click(_)`) or both `overlaps(_)`), which is then required to hold; and a requirement that both choice-labeled outcomes be player-controlled (via player_controls_outcome/1). Also produces three `constraint(ge/eq, result(...), result(...))` facts ordering the higher/lower outcomes' resource changes relative to each other


### Overlap-family candidates
**overlap vs. overlaps predicate name:** generation.lp only generates the plural form `overlaps(ENTITY1,ENTITY2,P)`. new_un_intent.lp independently uses `overlaps(Entity1,Entity2,true)` (plural), matching generation.lp. dean_intent and new_dean_intent's catalog entries use the singular `overlap(A,B,true)`; this is likely a catalog transcription error rather than an engine mismatch.
Overlap preconditions combined with resource-modification across four constructs. Not yet promoted because the exact shape varies across self- vs. distinct-entity overlap, required vs. forbidden modification, and single vs. duplicate outcome.
- **dean_intent opposite_results_on_overlap block:** derived predicate encoding that e(1) overlaps both e(2) and e(3), and those overlaps produce opposite modifications to the same resource; integrity constraint requires the derived predicate to hold.
- **new_dean_intent self-overlap block:** forbids outcomes with a self-overlap precondition (A overlaps A) from modifying the tracked resource.
- **new_dean_intent overlap/result block:** requires outcomes with a distinct-entity overlap precondition to also contain a resource-modification result.
- **new_dean_intent overlap uniqueness block:** forbids two distinct outcomes with identical overlap preconditions from both modifying the tracked resource.
- - **new_un_intent consumes-reading block:** `{ reading(consumes,relation(Entity1,Entity2)) } :- precondition(overlaps(Entity1,Entity2,true),Outcome), result(Outcome,delete(Entity2)).` derives a `consumes` reading from an overlap-then-delete pattern. 

## Anomalies
**dummy_intent:** :- not cooldown(_,_). is an arity mismatch (engine defines cooldown/3); renders the file permanently UNSAT against current engine (verified by direct run, 0.00s solve). Possibly stale from an older engine version, or a deliberate scratch file as the name 'dummy' could support either. Will be considering required_existence style pattern if working file contains.
**new_un_intent resource(r(2)) reference:** file bounds fix `min_resources = max_resources = 1`, so only r(1) can ever exist. The constraint `:- outcome(O), precondition(control_event(click(entity(e(2)))),O), result(O,modify(decrease,resource(r(2)))).` references r(2) and is permanently vacuous.
**scrubbing_intent monotonic(r(1)) bare-constant usage:** `allowed(monotonic(r(1))).` uses r(1) unwrapped, while every other occurrence in this file and elsewhere wraps resource ids as `resource(r(1))`. Likely an authoring typo producing a vacuous fact (r(1) as a bare constant is not the same term as resource(r(1))).

## Generated Constructs
The `_diff` intent family appears to contain machine-generated variation rather than hand-authored intent specifications (checked with simulate.py & resulting generated game files). These files include a serialized transcription of a previously generated game through old_* predicates, along with similarity-checking predicates (same_init, same_tick, same_cause_effect), constraints on the new game that reference mangled names and cardinality constraints that are meant to limit overlap between the previous and new generated game. lecture_intent_avoid_sim only has the constraints on the new game referencing mangled names.

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
| lecture_intent_drop.lp | done |
| new_dean_intent.lp | done |
| new_un_intent.lp | done |
| scrubbing_intent.lp | done |
| scrubbing_intent_diff.lp | done |
| travel_intent.lp | done |
