# Roadmap

Each milestone ends with something you can run a real (small) show on. Each chunk below is one
reviewable commit, under about 1000 lines including tests. Sizes are rough estimates of new lines.

**Status (2026-10-23):** the skeleton (src layout, `cuemodo --version`, Art-Net sender, CI) and
chunk 1 (show file v1) are done. Next up: chunk 2.

## Milestones

- **M0 Skeleton.** Show file v1, 44 Hz engine loop, Art-Net and sACN out, API with WebSocket state,
  minimal web page with faders. Runs on a Pi.
- **M1 Dimmer desk.** Patch, groups, programmer, looks, one cue list with timed fades and GO/Back,
  Enttec Pro output, network monitor. Enough for a theatre with conventional lights.
- **M2 LED and movers.** OFL import, colour models, 16-bit pan/tilt, presets by family,
  move-in-black, 2D plan visualizer.
- **M3 Live control.** Multiple playbacks with HTP/LTP merge, MIDI and OSC mapping with feedback
  (first on an Akai LPD8 mk2), effects, TUI, OSC cue actions to QLab/MadMapper/Resolume/OBS,
  motorized-fader prototype.
- **M4 Polish and suite.** 3D visualizer, timecode, show file versioning and backups, roles, first
  release.
- **M5 Second domain.** Audio engine as a separate process (likely Rust), then video, then
  projection mapping.

## M0: skeleton you can run on a Pi

| # | Chunk | Size | Status |
| --- | --- | --- | --- |
| 1 | **Show file v1: patch model.** Pydantic models for Show, FixtureType (built-in dimmer, RGB, RGBW), Channel, Fixture; versioned JSON load/save; validation; sample show | ~450 | done |
| 2 | **Rendering levels to DMX.** Normalized values to 512-byte universes: 8/16-bit, RGB, dimmer curves. Pure functions | ~350 | |
| 3 | **Engine loop and driver interface.** Fixed 44 Hz loop on its own thread; driver interface (start, stop, status, send); Art-Net adapted to it | ~400 | |
| 4 | **`cuemodo run show.json`.** First runnable server: load, run engine, output Art-Net, stop on Ctrl+C. Plus `cuemodo patch show.json` | ~250 | |
| 5 | **sACN output driver** via `sacn` (MIT), multicast per universe, priority | ~250 | |
| 6 | **Command bus and undo.** Every edit is a command: applied, journaled, undoable, announced | ~450 | |
| 7 | **HTTP API v1.** FastAPI inside `cuemodo run`: show, patch, levels, health; token header and Host/Origin guard | ~500 | |
| 8 | **WebSocket live state.** Topic subscriptions, diffs at ~20 Hz | ~400 | |
| 9 | **Web client skeleton.** Svelte + TypeScript + Vite in `web/`, served by the server, CI build | ~400 | |
| 10 | **Web faders page.** Touch-friendly fader per fixture, live over WebSocket | ~400 | |

Dependencies: 2 needs 1; 3 is independent; 4 needs 2 and 3.

## M1: dimmer desk

| # | Chunk | Size | Status |
| --- | --- | --- | --- |
| 11 | **Programmer and selection.** Server-side, shared by all clients | ~400 | |
| 12 | **Command line parser.** Our own grammar for shared conventions (`1 thru 10 @ 50 enter`, `+`, `-`, `@ full`, `out`) | ~500 | |
| 13 | **Groups.** Ordered selections in the show file, usable on the command line | ~250 | |
| 14 | **Looks.** Record the programmer into a numbered look, recall, update | ~350 | |
| 15 | **Cue list model with tracking.** Changes only; full state at any cue; Assert, Block, cue-only switch | ~500 | |
| 16 | **Fade engine.** Timed fades with curves, in/out/delay, GO, Back, follow, wait; isolated interface | ~500 | |
| 17 | **Playback merge and masters.** HTP/LTP, programmer, grand master, blackout | ~350 | |
| 18 | **Web: patch panel** | ~500 | |
| 19 | **Web: programmer and command line panel** | ~500 | |
| 20 | **Web: cue list and GO** | ~500 | |
| 21 | **Enttec DMX USB Pro driver** via pyserial | ~300 | |
| 22 | **Network monitor 1: Art-Net input.** ArtDmx/ArtPoll, sources, rate | ~350 | |
| 23 | **Network monitor 2: web grid.** 512 cells per universe, change highlighting | ~450 | |

## After M1

M2 and M3 will be split into chunks once M1 is in.

## Glossary

- **DMX universe**: one cable's worth of control, 512 addresses (slots) of 0 to 255.
- **Fixture type / mode**: the definition of a light model; a mode is one parameter layout it offers.
- **Channel**: the number you type to select a light; it can hold several fixtures that act as one.
- **Patch**: the list of channels and their fixtures, each with a type, mode, universe and start
  address.
- **Programmer**: the scratchpad where you select lights and set levels before recording.
- **Look / cue**: a stored state; a cue is a look plus timing in a cue list.
- **Tracking**: a cue stores only what changed; the rest carries over.
- **HTP / LTP**: Highest Takes Precedence (intensity) / Latest Takes Precedence (everything else).
