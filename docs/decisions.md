# Decisions

A dated log of project decisions. Add new entries at the bottom; if a decision is reversed, add a
new entry rather than editing the old one.

| Date | Decision |
| --- | --- |
| 2026-10-14 | License is MIT. Dependencies must be MIT, BSD, Apache 2.0 or public domain; no GPL in the core. |
| 2026-10-14 | Cues use **tracking** (store only changes, carry forward), with a per-list cue-only switch. |
| 2026-10-14 | One unified cue list for the whole show; a cue is a list of actions targeting engines (QLab-style). |
| 2026-10-14 | Show file format is JSON (users won't hand-edit it). MVR noted for patch/position interop. |
| 2026-10-14 | Minimum Raspberry Pi target: Pi 4 with 2 GB or more; Pi 5 supported. |
| 2026-10-14 | Reuse existing libraries where practical (Open Fixture Library for fixtures; permissive DMX/MIDI/OSC libraries). |
| 2026-10-14 | Originality: our own work only. Adopt conventions shared across many desks; never copy one vendor's distinctive syntax, design, manuals or artwork. |
| 2026-10-14 | Native iOS/macOS clients will use the same open API; the server and web client stay fully MIT. |
| 2026-10-15 | Project name is **Cuemodo** (cuemodo.io, github.com/cuemodo). |
| 2026-10-15 | Web UI framework is **Svelte** (TypeScript + Vite). |
| 2026-10-15 | Language: Python first for the lighting engine and cue list; Rust later for audio/video engines. |
| 2026-10-19 | One programmer shared by all clients (one show open on the server). |
| 2026-10-19 | MIDI controllers plug into the server by default. First test controller: Akai LPD8 mk2. |
| 2026-10-20 | Work proceeds in small chunks, each one commit under ~1000 lines (see [roadmap](roadmap.md)). |
| 2026-10-20 | CI runs tests on Python 3.13 and 3.14 across macOS, Windows and Linux; `requires-python >= 3.13`. |
| 2026-10-20 | Pydantic is the first runtime dependency (show model validation, later API schemas). |
| 2026-10-20 | Show file: universes numbered from 1; "fixture number" (not "channel") is what the operator types; each file embeds the fixture types it uses. |
| 2026-10-20 | If raw USB access is needed, use `libusb-package` for a cross-platform libusb backend. |
| 2026-10-22 | Name style: "Cuemodo" in prose, lowercase `cuemodo` for package, CLI, logo and domains. Tagline: "Big-show control for small stages." |
| 2026-10-23 | Channel layer in the patch (replaces the 2026-10-20 "fixture number"): the operator types a channel number; a channel holds one or more fixtures (parts), each fixture in exactly one channel. Lights controlled together but set apart use groups. "DMX address" for the wire side. |
