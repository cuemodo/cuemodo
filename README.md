<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/cuemodo-lockup-horizontal-on-dark.svg">
  <img src="docs/images/cuemodo-lockup-horizontal-on-light.svg" alt="Cuemodo" width="400">
</picture>

Open-source show control: light, sound, video (early development)

The goal for this project is to create a modular show control system. 

Some of the goals:
- cross platform back-end: python based, it can run on macOS, linux (Pi), Windows
- use existing devices for I/O: DMX and MIDI interfaces, etc.
- one cuelist for the entire show
- web and terminal clients (on the same machine, or on the same local network)

## Install (Developers)

- Install in a virtual environment, with Python 3.13+
- `[dev]` also install pytest
- `-e` makes edits takes effect without reinstalling.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
cuemodo --version
```

## Show files

A show is saved as one JSON file (format version 1 holds the patch: the fixture types used and
each fixture's number, universe and DMX address). See
[examples/dance-recital.json](examples/dance-recital.json): six dimmers, four RGB LED pars and two
RGBW fixtures over two universes.

## License

MIT, see [LICENSE](LICENSE).
