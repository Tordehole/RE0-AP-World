# Resident Evil 0

Resident Evil 0 HD Remaster (Steam/PC) item randomizer integration for Archipelago.

Current supported route: Normal difficulty, New Game.

The default ruleset contains 187 Archipelago checks. The Crank Handle and
Sterilizing Agent remain completely vanilla because direct randomized delivery
can break character-split progression. Maps/files, Rebecca's chemical mixing
system, derived puzzle-result items, and bonus/NG+ content also remain vanilla.

## Ink Ribbon option

`randomize_ink_ribbons` is enabled by default. Disable it to leave every Ink
Ribbon pickup completely vanilla and remove those locations/items from the AP
pool.

## Safety rules

The world contains placement rules for known one-way, missable, character-split
and self-lock cases. In particular, Factory keys remain local to safe Factory
checks, Blue Herbs remain local to Train/Facility/Basement checks, and the
Centurion-cage/Bar-Lounge edge-case locations can only contain safe local RE0
filler.
