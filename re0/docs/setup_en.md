# Resident Evil 0 Setup

1. Install `re0.apworld` into Archipelago 0.6.7 or newer.
2. Install the separate Resident Evil 0 Client package on the RE0 player's PC.
3. Generate a Resident Evil 0 YAML/seed and connect with the Resident Evil 0 Client.
4. Launch Resident Evil 0 HD Remaster (Steam/PC) and load/start a Normal New Game.

No ASI, DLL bridge, `dinput8.dll`, debugger, or executable patch is required.
The client reads/writes RE0 directly from Python.

## Persistent journal

The client keeps its per-seed save/delivery journal in the Windows temporary folder:

`%TEMP%\RE0_AP_full_journal_<seed>_slot<slot>_<player>.json`

The diagnostic log is also written to `%TEMP%`. Do not delete the journal while a
seed is in progress; it is part of the save/load reconciliation system.
