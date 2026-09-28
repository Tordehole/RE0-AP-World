from dataclasses import dataclass
from Options import DefaultOnToggle, PerGameCommonOptions


class RandomizeInkRibbons(DefaultOnToggle):
    """Randomize Ink Ribbon pickups as normal Archipelago checks.

    When disabled, every vanilla Ink Ribbon pickup is left completely vanilla
    and removed from the AP location/item pool so saving is never gated by
    randomizer placement.
    """

    display_name = "Randomize Ink Ribbons"


@dataclass
class RE0Options(PerGameCommonOptions):
    randomize_ink_ribbons: RandomizeInkRibbons
