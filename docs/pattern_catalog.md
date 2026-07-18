# Gemini Intent Pattern Catalog

Derived from analysis of the intent files in upstream Gemini (external/Gemini/asp/intents/, commit e6ab676). Illustrative snippets are quoted minimally from the upstream repo for analysis purposes.

---

## Pattern: bounds  
**Description:** Declares the numeric generation bounds every intent sets.  
**Shape:** `#const <name> = <int>.` 
**Varies:** the integer values only.  
**Fixed:** the 12 constant names themselves (min/max entities, resources, outcomes, timers, end_outcomes, resource_change_per, conditions_per). Need to confirm if all files set all 12.
**Occurrences:** dinner_intent (12/12)

## Pattern: required_quality  
**Description:** Requires a named reading-quality to hold somewhere in the generated game. Engine defines the semantics; intent supplies only the name.  
**Shape:** `required(<quality>).`  
**Varies:** the quality name — drawn from the readings.lp vocabulary (~25 values, e.g. sharing, maintenance, help, hurt, tradeoff...).  
**Fixed:** everything else.  
**Occurences:** dinner_intent (sharing, maintenance).  

## Pattern: entity_label / resource_label  
**Description:** Assigns a display label, resources adds a visibility mode.  
**Shape:** `label(<entity_id>, <label>).` / `label(<resource_id>, <label>, <visibility>).`  
**Varies:** id, label; visibility (resource only: write | private | read).  
**Occurences:** dinner_intent (food, friend; satiation/write, though note the satiation label here is *conditional*, see label_rule).  

## Pattern: label_rule  
**Description:** Derive this label when this reading holds  
**Shape:** label(<resource_id>, <label>, <visibility>) :- reading(<quality>, <target>).  
**Varies:** resource_id, label, visibility, quality and target. resource form only seen so far, no conditional entity.   
**Occurences:** dinner_intent(r(1),satiation,write,good,r(1)), reading is forced to hold in dinner_intent.lp with following line.  

## Pattern: forbidden_condition  
**Description:** No outcome in the generated game may be triggered by any comparison against the amount of the named color  
**Shape:** `:- condition(compare(_,amount(<color>),_)).`  
**Varies:** color, only clear observed so far.  
**Occurences** dinner_intent(clear)  

## Pattern: required_reading   
**Description:** Requires a specific reading on a specific target.  
**Shape:** `:- not reading(<quality>, <target>).`  
**Varies:** quality; target: which has two shapes so far: unary (`resource(r(1))`) and relational (`relation(entity(e(1)),entity(e(2)))`).  
**Fixed:** the `:- not reading(...)` frame.  
**Occurences:** dinner_intent: good/resource (unary), sharing/relation (relational), maintenance/resource (unary).  
**Note:** compound readings (goal(produce), stakes(high)) exist in readings.lp but no instance seen yet in files cataloged so far.  

## Pattern: label_enum  
**Description:** Three-line idiom that declares allowed labels, forbid any outside the set, require one to be assigned.  
**Shape:** `acceptable_labels(<a>;<b>).` + two enforcement constraints.  
**Varies:** the label set; the target resource.  
**Fixed:** the two constraint lines' structure.  
**Occurences:** dinner_intent (appetite/bites on r(2)).  
**Note:** one schema entry → three emitted lines. Compiler owns all three.  

## Pattern: count_requirement  
**Description:** Pins how many instances of an entity exist.  
**Shape:** `:- total_count(<entity>, N), N <comparator> <value>.`  
**Varies:** entity, comparator (!=, >, < seen in comments), value.  
**Occurences:** dinner_intent (e(2) != 3; commented-out >/< suggest range form intended by original authors).  

## Pattern: required_property  
**Description:** Requires the named engine-derived property to hold for the entity  
**Shape:** `:- not <property>(entity(<entity>)).`  
**Varies:** entity, property  
**Occurences:** dinner_intent (constant/e(2)), only property observed so far is constant.  

## Pattern: forbidden_pool_count  
**Description:** Forbids the named entity's number of spawn pools from falling within [<low>, <high>], inclusive. Observed use: low = high = 1, i.e., never exactly one pool, must be zero or several  
**Shape:** `:- <low> {pool(entity(<entity>),_,_,_)} <high>.`  
**Varies:** low, entity, high  
**Occurences:** dinner_intent (e(1), 1..1)  

## Pattern: required_mode_change  
**Description:** Requires the game to contain the named mode change.  
**Shape:** `:- not action(mode_change(<mode>)).`  
**Varies:** mode: can consist of narrative_gating, narrative_progress, game_loss, game_win (as in generation_atoms.lp)  
**Occurences:** dinner_intent (narrative_gating), appeared with mode_change_cap  

## Pattern: mode_change_cap  
**Description:** caps mode_change actions (of any mode) at <low> − 1.  
**Shape:** `:- <low> {action(mode_change(N))}.`  
**Varies:** low  
**Occurences:** dinner_intent (2), appeared together with required_mode_change  

## No pattern yet  
revisit if more than 2 files show these shapes.  
- **dinner_intent is_consumed block:** invents a new predicate (4 lines: 1 derivation + 3 enforcement constraints) encoding "resource gain must coincide with consuming the food entity."  
- **dinner_intent cooldown-conditioned label rules:** label assignment conditioned on cooldown() + a player_model. Could be a candidate for a future conditional label_rule variant.  

## Coverage tracker
| File | Status |
|---|---|
| dinner_intent.lp | done |
