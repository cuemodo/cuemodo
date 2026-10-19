# CueModo

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

## License

MIT, see [LICENSE](LICENSE).
