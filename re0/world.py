from collections import Counter

from BaseClasses import ItemClassification, Region
from worlds.AutoWorld import World

from .data import (
    GAME_NAME,
    GOAL_LOCATION,
    ITEM_DEFS,
    LOCATION_DEFS,
    REGION_CONNECTIONS,
    REGIONS,
)
from .items import CLASSIFICATIONS, ITEM_NAME_TO_ID, RE0Item
from .locations import LOCATION_NAME_TO_ID, RE0Location
from .options import RE0Options
from .rules import set_re0_rules


class RE0World(World):
    """Resident Evil 0 Normal New Game item randomizer.

    Default build: 187 physical AP checks.
    Train 30, Training Facility/Basement 78, Laboratory 26,
    Factory 12, Treatment Plant 41.
    """

    game = GAME_NAME
    topology_present = True
    options_dataclass = RE0Options
    required_client_version = (0, 6, 7)

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    item_name_groups = {
        "Progression": {item.name for item in ITEM_DEFS if item.classification == "progression"},
        "Useful": {item.name for item in ITEM_DEFS if item.classification == "useful"},
        "Filler": {item.name for item in ITEM_DEFS if item.classification == "filler"},
    }

    def generate_early(self) -> None:
        # Character-split safety: these items must physically exist in the local
        # RE0 world rather than being sent from another player's game. Blue Herbs
        # are also kept local so the early poison-safety rule is actually useful.
        self.options.local_items.value.update({"Up Key", "Elevator Key", "Blue Herb"})

    def get_active_location_defs(self):
        if self.options.randomize_ink_ribbons.value:
            return list(LOCATION_DEFS)
        return [loc for loc in LOCATION_DEFS if not loc.vanilla_item.startswith("Ink Ribbon")]

    def create_item(self, name: str) -> RE0Item:
        item_def = next(item for item in ITEM_DEFS if item.name == name)
        return RE0Item(name, CLASSIFICATIONS[item_def.classification], item_def.code, self.player)

    def create_event(self, name: str) -> RE0Item:
        return RE0Item(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        # Build the pool from the active checks rather than the static catalog so
        # option-disabled vanilla checks (currently Ink Ribbons) disappear from
        # both sides of the AP pool cleanly.
        active_counts = Counter(location.vanilla_item for location in self.get_active_location_defs())
        for item_def in ITEM_DEFS:
            for _ in range(active_counts.get(item_def.name, 0)):
                self.multiworld.itempool.append(self.create_item(item_def.name))

    def get_filler_item_name(self) -> str:
        filler_names = [item.name for item in ITEM_DEFS if item.classification == "filler"]
        if not self.options.randomize_ink_ribbons.value:
            filler_names = [name for name in filler_names if not name.startswith("Ink Ribbon")]
        return self.random.choice(filler_names)

    def create_regions(self) -> None:
        regions = {name: Region(name, self.player, self.multiworld) for name in REGIONS}
        self.multiworld.regions += list(regions.values())

        for location in self.get_active_location_defs():
            regions[location.region].add_locations({location.name: location.code}, RE0Location)

        # Logic-only completion event. The live client reports CLIENT_GOAL from
        # the proven final-state signature (roomCur=165, roomNext=165, menuId=21).
        goal_region = regions["Victory"]
        goal_region.locations.append(RE0Location(self.player, GOAL_LOCATION, None, goal_region))

        for source_name, target_name, required_items in REGION_CONNECTIONS:
            source = regions[source_name]
            entrance_name = f"{source_name} -> {target_name}"
            if required_items:
                source.add_exits(
                    {target_name: entrance_name},
                    {target_name: lambda state, items=required_items: state.has_all(items, self.player)},
                )
            else:
                source.add_exits({target_name: entrance_name})

    def set_rules(self) -> None:
        set_re0_rules(self)

    def fill_slot_data(self) -> dict:
        active_count = len(self.get_active_location_defs())
        return {
            "build": "normal-split-client-v1.20",
            "normal_location_count": active_count,
            "randomize_ink_ribbons": bool(self.options.randomize_ink_ribbons.value),
        }
