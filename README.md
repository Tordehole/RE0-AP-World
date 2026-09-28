# Resident Evil 0 Archipelago

Unofficial Archipelago world for **Resident Evil 0 HD Remaster (Steam/PC)**.

This repository contains the Archipelago world/generation side only.

## Current support

- Normal New Game
- 187 randomized locations by default
- Queen Leech victory condition
- Optional vanilla Ink Ribbons
- Separate client required for game integration

## Repository layout

`re0/`
- world generation
- item/location definitions
- regions and logic
- options
- Archipelago metadata
- bundled game/setup documentation

## Client

The game integration is intentionally kept in a separate repository.

The standalone RE0 client handles:
- connecting to the Archipelago server
- reading/writing Resident Evil 0 process memory
- detecting checks
- receiving items
- save/load reconciliation
- journal handling
- victory reporting

## Current scope

| Area | Checks |
| --- | ---: |
| Train | 30 |
| Training Facility + Basement | 78 |
| Laboratory | 26 |
| Factory | 12 |
| Treatment Plant | 41 |
| **Total** | **187** |

Easy, Hard and other modes are not supported yet.

## Ink Ribbon option

`randomize_ink_ribbons: true` (default)
- Ink Ribbon pickups are included in the Archipelago item/location pool.

`randomize_ink_ribbons: false`
- Ink Ribbon pickups remain vanilla.

## Development note

This project was developed with substantial AI assistance. Game mapping, progression design,
testing, bug reproduction and validation were carried out through repeated in-game testing.
