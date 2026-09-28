from BaseClasses import ItemClassification
from worlds.generic.Rules import add_item_rule, set_rule

from .data import (
    FIRE_KEY_LOCATION,
    FIRE_KEY_SAFE_FILLER,
    GOAL_ITEM,
    GOAL_LOCATION,
    HANDLE_SAFE_LOCATIONS,
    ITEM_DEFS,
    LOCATION_REQUIREMENTS,
)

LOCAL_PROGRESSION_AREA = {
    item.name: item.area_index
    for item in ITEM_DEFS
    if item.classification == "progression" and item.area_index is not None
}


def _is_progression(item) -> bool:
    return bool(item.classification & ItemClassification.progression)


def set_re0_rules(world) -> None:
    player = world.player
    active_defs = world.get_active_location_defs()
    active_names = {loc.name for loc in active_defs}

    for location_name, required_items in LOCATION_REQUIREMENTS.items():
        if location_name not in active_names:
            continue
        set_rule(
            world.multiworld.get_location(location_name, player),
            lambda state, items=required_items: state.has_all(items, player),
        )

    # RE0 story-area ceiling: local RE0 progression may move earlier, but never
    # later than its own section. Foreign-world items are not constrained here.
    for location_def in active_defs:
        location = world.multiworld.get_location(location_def.name, player)
        loc_area = location_def.area_index
        add_item_rule(
            location,
            lambda item, area=loc_area: (
                item.player != player
                or item.name not in LOCAL_PROGRESSION_AREA
                or area <= LOCAL_PROGRESSION_AREA[item.name]
            ),
        )

    # Blue Herbs are poison insurance for the spider-heavy early game. Keep the
    # player's Blue Herbs local and inside Train / Facility+Basement (areas 0/1).
    # generate_early() also marks Blue Herb local so another world cannot delay it.
    for location_def in active_defs:
        location = world.multiworld.get_location(location_def.name, player)
        add_item_rule(
            location,
            lambda item, area=location_def.area_index: (
                item.player != player or item.name != "Blue Herb" or area <= 1
            ),
        )

    # Pre-Billy safety: Conductor's Key cannot appear before the Dining route and
    # Billy join state. Runtime delivery has an additional Billy-live gate.
    for location_def in active_defs:
        if location_def.region != "Train Start":
            continue
        add_item_rule(
            world.multiworld.get_location(location_def.name, player),
            lambda item: item.player != player or item.name != "Conductor's Key",
        )

    # Service Room trap safety.
    service_escape_items = {"Ice Pick", "Conductor's Key"}
    service_entry = world.multiworld.get_location(
        "Train - Service Room - Conductor's Key", player
    )
    add_item_rule(
        service_entry,
        lambda item, safe=service_escape_items: (
            not _is_progression(item)
            or (item.player == player and item.name in safe)
        ),
    )

    for location_name in (
        "Train - Service Room - Green Herb",
        "Train - Service Room - Handgun Ammo",
    ):
        set_rule(
            world.multiworld.get_location(location_name, player),
            lambda state: (
                state.has("Ice Pick", player)
                or state.has("Conductor's Key", player)
            ),
        )

    # Timed one-way end of Train: no progression from ANY world/player.
    for location_name in (
        "Train - Engine Cab - Ammo Under Cabinet",
        "Train - Engine Cab - Ammo Northeast Corner",
    ):
        add_item_rule(
            world.multiworld.get_location(location_name, player),
            lambda item: not _is_progression(item),
        )

    # Centurion cage becomes unavailable after the MO Disk / sword-door state.
    # Keep it as a genuine random check but only allow safe local RE0 consumables.
    add_item_rule(
        world.multiworld.get_location(FIRE_KEY_LOCATION, player),
        lambda item: item.player == player and item.name in FIRE_KEY_SAFE_FILLER,
    )

    # Stinger post-boss Panel Opener location has a rare missable-state edge case.
    # The Panel Opener ITEM remains randomized; only this physical check is filler-safe.
    add_item_rule(
        world.multiworld.get_location("Train - Bar Lounge - Panel Opener", player),
        lambda item: item.player == player and item.name in FIRE_KEY_SAFE_FILLER,
    )

    # Exact Lab Dial self-lock exclusions retained from mapped routing tests.
    for location_name in (
        "Lab - Cable Car - Magnum",
        "Lab - Machine Room 1F - Output Regulator Coil",
        "Lab - Church Back Room - Shotgun Ammo",
    ):
        add_item_rule(
            world.multiworld.get_location(location_name, player),
            lambda item: item.player != player or item.name != "Dial",
        )

    # Factory forced-character split safety. Both keys are local to this RE0 world
    # (generate_early) and stay inside the Factory. Up Key must be pre-Up; Elevator
    # Key may be pre-Up or post-Up but never behind its own Factory End gate.
    for location_def in active_defs:
        location = world.multiworld.get_location(location_def.name, player)
        add_item_rule(
            location,
            lambda item, region=location_def.region, area=location_def.area_index: (
                item.player != player
                or item.name not in {"Up Key", "Elevator Key"}
                or (
                    area == 3
                    and (
                        (item.name == "Up Key" and region == "Factory Start")
                        or (item.name == "Elevator Key" and region in {"Factory Start", "Factory Up"})
                    )
                )
            ),
        )

    # Treatment Plant Handle has an intentionally narrow safe-location set. In
    # particular Generator Room 2F is post-Handle and must never hold the Handle.
    for location_def in active_defs:
        if location_def.area_index != 4:
            continue
        location = world.multiworld.get_location(location_def.name, player)
        add_item_rule(
            location,
            lambda item, loc_name=location_def.name: (
                item.player != player
                or item.name != "Handle"
                or loc_name in HANDLE_SAFE_LOCATIONS
            ),
        )

    # Belt-and-braces Treatment Plant side-chain / endgame restrictions.
    final_tp = {
        location.name for location in active_defs if location.region == "TP Final"
    }
    keycard_ledge = "Treatment Plant - Maintenance Area - Keycard"
    for location_def in active_defs:
        if location_def.area_index != 4:
            continue
        location = world.multiworld.get_location(location_def.name, player)
        add_item_rule(
            location,
            lambda item, loc_name=location_def.name: (
                item.player != player
                or item.name not in {"Keycard", "Empty Battery", "Industrial Water"}
                or (
                    loc_name not in final_tp
                    and not (
                        item.name in {"Empty Battery", "Industrial Water"}
                        and loc_name == keycard_ledge
                    )
                )
            ),
        )

    goal_location = world.multiworld.get_location(GOAL_LOCATION, player)
    goal_location.place_locked_item(world.create_event(GOAL_ITEM))
    world.multiworld.completion_condition[player] = lambda state: state.has(GOAL_ITEM, player)
