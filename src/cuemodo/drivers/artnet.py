"""
Art-Net output (ArtDmx) of one or more DMX universes.

Originates from ConsoleLink's artnet.py (same author, MIT); generalised here from the console's
two universes to any number of consecutive ones.

Stdlib only. Art-Net receivers and nodes expect a periodic refresh (the spec asks for a keep-alive
at least every ~4 s), so ArtNetSender re-sends the last frame itself: immediately on change (capped
at `rate_hz`), otherwise every `keepalive_s` seconds.

Universe i of each frame goes out as Art-Net port-address start_universe + i (Art-Net numbers
universes from 0, so some visualisers label universe 0 as "1").
"""
import socket
import struct
import sys
import threading
import time

ARTNET_PORT = 6454
DEFAULT_DEST = "127.0.0.1"
DEFAULT_RATE_HZ = 40.0
DEFAULT_KEEPALIVE_S = 1.0
UNIVERSE_SIZE = 512
_ERROR_LOG_INTERVAL_S = 5.0


def build_artdmx(universe, levels, sequence=0):
    """One ArtDmx packet: `levels` (up to 512 values, 0-255) on 15-bit port-address `universe`.

    `sequence` 1-255 lets receivers reorder packets; 0 disables that. Data length is padded to an
    even number as the spec requires (512 already is).
    """
    if not 0 <= universe <= 0x7FFF:
        raise ValueError(f"Art-Net universe out of range: {universe}")
    data = bytes(levels)
    if len(data) > UNIVERSE_SIZE:
        raise ValueError(f"too many DMX levels: {len(data)}")
    if len(data) % 2:
        data += b"\x00"
    return (b"Art-Net\x00"
            + struct.pack("<H", 0x5000)             # OpCode ArtDmx, little-endian
            + struct.pack(">H", 14)                 # protocol version, hi byte first
            + bytes([sequence & 0xFF, 0,            # Sequence, Physical
                     universe & 0xFF, universe >> 8])  # SubUni (low byte), Net (bits 8-14)
            + struct.pack(">H", len(data))          # Length, big-endian
            + data)


def resolve_dest(dest):
    """'broadcast' -> the limited broadcast address; anything else is used as given."""
    return "255.255.255.255" if dest.lower() == "broadcast" else dest


class ArtNetSender:
    def __init__(self, dest=DEFAULT_DEST, start_universe=0, rate_hz=DEFAULT_RATE_HZ,
                 keepalive_s=DEFAULT_KEEPALIVE_S, port=ARTNET_PORT):
        if rate_hz <= 0 or keepalive_s <= 0:
            raise ValueError("Art-Net rate and keepalive must be positive")
        self.addr = (resolve_dest(dest), port)
        self.start_universe = start_universe
        self.min_interval = 1.0 / rate_hz
        self.keepalive = keepalive_s
        self.packets_sent = 0
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._cond = threading.Condition()
        self._frame = None  # latest list of universes, or None before the first update
        self._dirty = False
        self._stopped = False
        self._sequence = {}  # port-address -> last sequence number sent
        self._last_error_log = 0.0
        self._thread = threading.Thread(target=self._run, name="artnet", daemon=True)

    def start(self):
        self._thread.start()
        return self

    def _log_error(self, addr, error):
        now = time.monotonic()
        if now - self._last_error_log >= _ERROR_LOG_INTERVAL_S:
            self._last_error_log = now
            print(f"[artnet] send to {addr[0]}:{addr[1]} failed: {error}", file=sys.stderr)

    def update(self, *universes):
        """Queue a new frame (one level sequence per universe); never blocks on the network."""
        with self._cond:
            self._frame = [bytes(levels) for levels in universes]
            self._dirty = True
            self._cond.notify()

    def stop(self):
        with self._cond:
            self._stopped = True
            self._cond.notify()
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._sock.close()

    def _run(self):
        last_sent = float("-inf")
        while True:
            with self._cond:
                while True:
                    if self._stopped:
                        return
                    now = time.monotonic()
                    if self._dirty:
                        wait = last_sent + self.min_interval - now
                    elif self._frame is not None:
                        wait = last_sent + self.keepalive - now
                    else:
                        wait = None
                    if wait is not None and wait <= 0:
                        break
                    self._cond.wait(wait)
                frame = self._frame
                self._dirty = False
            last_sent = time.monotonic()
            self._send(frame)

    def _send(self, frame):
        for i, levels in enumerate(frame):
            universe = self.start_universe + i
            sequence = self._sequence.get(universe, 0) % 255 + 1  # 1..255, never 0
            self._sequence[universe] = sequence
            packet = build_artdmx(universe, levels, sequence)
            try:
                self._sock.sendto(packet, self.addr)
                self.packets_sent += 1
            except OSError as e:
                self._log_error(self.addr, e)
