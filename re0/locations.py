from BaseClasses import Location

from .data import GAME_NAME, LOCATION_DEFS


class RE0Location(Location):
    game = GAME_NAME


LOCATION_TABLE = {location.name: location for location in LOCATION_DEFS}
LOCATION_NAME_TO_ID = {location.name: location.code for location in LOCATION_DEFS}

REGION_LOCATIONS = {}
for location in LOCATION_DEFS:
    REGION_LOCATIONS.setdefault(location.region, {})[location.name] = location.code
