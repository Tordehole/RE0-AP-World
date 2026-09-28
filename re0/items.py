from BaseClasses import Item, ItemClassification

from .data import GAME_NAME, ITEM_DEFS


class RE0Item(Item):
    game = GAME_NAME


CLASSIFICATIONS = {
    "progression": ItemClassification.progression,
    "useful": ItemClassification.useful,
    "filler": ItemClassification.filler,
}


ITEM_TABLE = {item.name: item for item in ITEM_DEFS}
ITEM_NAME_TO_ID = {item.name: item.code for item in ITEM_DEFS}

PROGRESSION_ITEMS = {item.name for item in ITEM_DEFS if item.classification == "progression"}
USEFUL_ITEMS = {item.name for item in ITEM_DEFS if item.classification == "useful"}
FILLER_ITEMS = {item.name for item in ITEM_DEFS if item.classification == "filler"}
