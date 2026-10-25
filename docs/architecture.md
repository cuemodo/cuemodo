# Architecture

Cuemodo is one Python show server that holds the show, runs a fixed-rate engine, and talks to the
outside world through drivers. Every client (web, TUI, later native apps) is a thin view over one
versioned API. Lighting is the first domain plugged into a domain-neutral core, so audio, video and
projection mapping can arrive later on the same clock, cue list and API.

## Principles

- **Headless server, many clients.** The server never draws UI. Anything a client can do, the API
  can do, so web, TUI, OSC and MIDI are equals.
- **Runs anywhere Python runs.** macOS, Windows, Linux, and a Raspberry Pi 4 (2 GB+) or Pi 5 as a
  dedicated node. No native build step for the core.
- **The show file is plain data.** Versioned JSON that diffs in git and opens without the app.
- **Output never stutters.** The engine computes frames at a fixed rate (44 Hz for DMX) in its own
  loop, isolated from clients, disk and network.
- **Domain-neutral core.** Cues, timing, the clock, undo and the API know nothing about DMX.
- **Permissive licenses only.** MIT, with MIT/BSD/Apache/public-domain dependencies.

## Audience

Amateur and low-budget shows: dance recitals, community and school theatre, small circus. It should
run on hardware people already own (a laptop, a Pi, a cheap USB DMX dongle), and it teaches the real
concepts (patch, groups, palettes, tracking, HTP/LTP) so a designer can later move to a professional
desk without relearning the basics. Thousands of universes, touring-grade timecode or redundant
backup consoles are not goals.

## Show model

The show is a tree of plain objects with stable IDs. All edits go through commands, so every change
is undoable, journaled and broadcast to clients.

| Object | What it is |
| --- | --- |
| Fixture type | A light model from the library: modes, parameters |
| Channel | What the operator types to select a light: number, name, one or more fixtures |
| Fixture | A patched device inside a channel: type + mode, universe, address, position |
| Group | An ordered selection of channels (order drives fans and effects) |
| Programmer | The live editing buffer: selection plus values. One, shared by all clients |
| Preset | Reusable values for one parameter family (Position, Colour, Beam, Focus) |
| Look | A stored state, possibly referencing presets |
| Cue | A look plus timing (in/out/delay, follow, wait) in a cue list |
| Cue list | Ordered cues with tracking; per-list cue-only switch; Assert and Block flags |
| Playback | A cue list or look on a fader or button |
| Effect | A generator over time (sine, chase, fan) on a parameter |

**Values and priority.** Parameter values are normalized (0.0 to 1.0, or a named slot such as a
gobo) and become DMX bytes only at output. Intensity merges HTP (highest wins) across playbacks;
everything else merges LTP (latest wins). The programmer sits on top, then grand master and
blackout.

**Per-frame pipeline.**

1. Advance the show clock, fades, follows and effects.
2. Ask each active playback for its contribution (tracked state plus fade progress).
3. Merge (HTP intensity, LTP the rest), apply the programmer, then masters.
4. Hand the merged state to the lighting domain to build universes.
5. Send universes to every output driver; publish diffs to clients at a lower rate (~20 Hz).

Fades are evaluated from start time and curve, not stepped, so a slow client or a dropped frame
never shifts a cue.

## Familiar vocabulary, original platform

Designers who know common pro desks should be productive in the first hour, so the working
vocabulary follows conventions shared across many desks: a typed command line (`1 thru 10 @ 50
enter`, `record cue 5`), tracking by default, palettes by parameter family, record/update options,
playbacks on faders, blind editing, ordered groups, waveform and step effects, and USITT ASCII / CSV
/ MVR import. The grammar and parser are our own, and every command maps to one API call.

Where Cuemodo differs on purpose: no proprietary hardware or dongle, any browser is a console wing,
several people can connect at once, the show file is readable JSON, and the same cue list will later
fire audio, video and mapping cues.

## Fixtures

Dimmers, LED fixtures and moving heads share one model: a fixture type declares parameters, and each
parameter maps to one or more DMX channels in a given mode. Engine needs include dimmer curves,
colour models (RGB/HSI/CIE xy resolved to emitters), virtual intensity, multi-cell fixtures, 16-bit
pan/tilt with invert/swap, wheel slots as named values, and move-in-black.

The fixture library is the Open Fixture Library (MIT): ship a curated subset, fetch the rest on
demand. QLC+ fixture files can be imported too. Our own types use the same JSON shape so they can be
contributed upstream. Parameter families (Intensity, Position, Colour, Beam, Focus, Control) drive
presets, programmer tabs and the default HTP/LTP rule.

## I/O drivers

Every peripheral is a driver with the same small interface: start, stop, status, and either
`send(universes)` for outputs or an event stream for inputs. Drivers run outside the engine loop so a
stuck device never stalls output.

| Driver | Direction | Library |
| --- | --- | --- |
| Art-Net 4 | out + in | own code, stdlib only (`drivers/artnet.py`) |
| sACN (E1.31) | out + in | `sacn` (MIT) |
| Enttec DMX USB Pro | out | pyserial (BSD); the Pro appears as a serial port |
| MIDI | in + out | mido + python-rtmidi (MIT) |
| OSC | in + out | python-osc (public domain) |
| Timecode (later) | in | MTC via MIDI, LTC via audio |

MIDI and DMX controllers plug into the server by default (e.g. USB into the Pi) so they work with no
client open. One mapping layer turns any input event (MIDI CC, OSC address, key, web button) into an
API command. Motorized-fader feedback will be prototyped on a Mackie Control surface such as the
Behringer X-Touch. If raw USB access is ever needed, use `libusb-package` for a cross-platform libusb
backend.

## Clients and API

One API, two transports: REST for commands and queries (`POST /api/v1/cues/12/go`) and a WebSocket
for live state (subscribe to topics such as `playbacks`, `programmer`, `dmx/universe/1`; receive
diffs). The same commands are exposed over OSC. An OpenAPI schema is generated by the server.

- **Web app** (Svelte): the main operator UI, served by the server, touch-first, works offline on a
  show LAN.
- **TUI** (Textual): for SSH, a Pi with a small screen, or keyboard-first users.
- **Native iOS / iPadOS / macOS** (later): SwiftUI over the same API.

All clients share one live programmer, since there is one show and one rig. Optional roles
(operator, viewer, locked show mode) come later.

## Suite tools

Separate listen-only apps that double as debuggers and work with any console:

- **Network monitor**: Art-Net/sACN sources, universes, a 512-cell grid per universe with change
  highlighting, packet rate and node discovery.
- **Show visualizer**: a 2D plan view first (fixtures tinted by colour and intensity, drag to place),
  then a simple Three.js 3D view.

## Plugins and the wider suite

The core treats lighting as a plugin from day one. Four plugin kinds: **domain** (targets,
parameters, merge, render), **driver**, **input mapping**, and **client panel**. Plugins are
discovered as Python entry points.

The suite is one product made of separate engine processes (lighting, audio, video, later mapping)
behind one show file, one cue list and one web UI shell. Engines are separate because their needs
differ, they may run on different machines, and a crash in one must not stop the others. Shared from
day one: the control protocol (WebSocket + OSC, written down as a spec), the cue model (a cue is a
list of actions, each targeting an engine), one show clock, and the UI shell.

Until our own engines exist, cue actions can drive existing tools over OSC (QLab, MadMapper,
Resolume, OBS). Engine order: lighting + cue list, OSC/MIDI action targets, audio, video, projection
mapping.

**Language.** Python for the lighting engine and cue list until the model and protocol settle. Rust
is the natural fit for audio and video engines; lighting is ported only if Python actually limits
it.

## Tech stack

| Layer | Choice |
| --- | --- |
| Server | Python 3.13+, asyncio, FastAPI (REST + WebSocket), Pydantic models |
| Engine loop | Dedicated thread with a monotonic clock |
| Web client | TypeScript, Svelte, Vite |
| TUI | Textual |
| 3D | Three.js |
| Packaging | pipx, a flashable Pi image later, desktop bundles later |
