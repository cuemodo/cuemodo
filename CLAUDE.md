# Cuemodo

Cuemodo is an open-source lighting desk: a headless Python show server with web (and later TUI and
native) clients. It is built for amateur shows (dance recitals, school and community theatre, small
circus) and as a learning step towards professional desks. Lighting comes first; audio, video and
projection mapping join later as separate engines driven by the same cue list.

Read these before larger changes:

- [docs/architecture.md](docs/architecture.md): how the system fits together
- [docs/roadmap.md](docs/roadmap.md): milestones, the chunk plan and current progress
- [docs/decisions.md](docs/decisions.md): dated log of decisions already made (don't reopen them
  without a reason)

## Dev setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Python 3.13+ (Raspberry Pi OS Trixie ships 3.13). CI runs pytest on 3.13 and 3.14 across macOS,
Windows and Linux, so code must stay cross-platform (paths, sockets, line endings).

## Layout

- `src/cuemodo/`: the package (`cli.py`, `drivers/` for output drivers, `show/` for the show model
  and file format)
- `tests/`: pytest, one file per module area
- `examples/`: sample show files
- `rust/`: placeholder crate only; Rust is for future audio/video engines

## Conventions

- **Small, readable changes.** One chunk of work is one reviewable commit, under about 1000 lines
  including tests. Many small changes beat one big drop.
- **Explain domain terms.** Readers may be new to lighting desks. Module docstrings define the
  lighting words they use (see `show/model.py`).
- **Python first.** Server, engine and cue list are Python. Keep the fade/effects engine behind a
  small interface so it can be optimized or ported later.
- **Web UI is Svelte** (TypeScript + Vite), served by the server.
- **Tracking cues.** A cue stores only what changed; everything else carries forward from earlier
  cues.
- **Show file is versioned JSON**, one file per show, starting with
  `"format": "cuemodo-show", "version": N`. Users don't hand-edit it, but keep it diff-friendly.
- **Values are normalized** (0.0 to 1.0) in the model and only become DMX bytes at output.
  Universes are numbered from 1; drivers map to protocol numbering.
- **Headless server.** Anything a client can do goes through the API; the server never draws UI.

## Dependencies and license

The project is MIT. Only add dependencies under permissive licenses (MIT, BSD, Apache 2.0, public
domain). No GPL or LGPL in the core (e.g. pyartnet and DMXEnttecPro are GPL-3.0, so they're out).
Prefer a maintained existing library over writing our own, and say why when adding one.

## Originality

Everything is our own work. Adopt a convention only when many desks share it (e.g. `1 thru 10 @
50`, tracking, HTP/LTP). Never copy another product's code, manuals, screen layouts, artwork or
distinctive syntax. When in doubt about IP, take the safe side.

## Naming

Write "Cuemodo" in prose (never "CueModo"). Use all-lowercase `cuemodo` for the package, CLI,
logo and domains.
