#!/usr/bin/env python3
"""
Proportion Grand Prix — classroom race server.

Serves the game to every device on the same wi-fi and relays the race
between them.  Python 3 only, standard library only, nothing to install.

    python3 race_server.py            # port 8000
    python3 race_server.py 8080       # a different port

Students open the address it prints.  If the internet is down this still
works, because everything is served from this machine.
"""

import base64, functools, hashlib, json, os, random, socket, struct, sys, threading, time, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

print = functools.partial(print, flush=True)      # never buffer: the window must show the address

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = "Proportion Grand Prix.html"
GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ"     # no I or O — they read as 1 and 0
MAX_RACERS = 32                                # a whole class in one room
# Hosting platforms hand you a port and have no terminal. Detect that once.
CLOUD = bool(os.environ.get("PORT"))
MAX_TRACKS = 5                                 # keep in step with TRACKS in the game
SNAP_HZ = 10                                   # merged position broadcasts per second

rooms = {}                # code -> Room
rooms_lock = threading.Lock()


DEVICES = {"n": 0}


def announce_devices(delta):
    DEVICES["n"] = max(0, DEVICES["n"] + delta)
    n = DEVICES["n"]
    print("   >>> DEVICES CONNECTED: %d %s" % (n, "" if n else "(still none - see the checklist above)"))


class Room:
    def __init__(self, code):
        self.code = code
        self.conns = {}           # player id -> WSConn
        self.order = []           # player ids, join order
        self.host = None
        self.cfg = {"track": 0, "laps": 3, "fuel": 1, "topics": [0, 1, 2, 3, 4, 5]}
        self.started = False
        self.touched = time.time()
        self.states = {}          # kart id -> latest position, merged from everyone
        self.dirty = False

    def roster(self):
        out = []
        for pid in self.order:
            c = self.conns.get(pid)
            if c:
                out.append({"id": pid, "name": c.name, "kart": c.kart,
                            "dec": c.dec, "drv": c.drv, "host": pid == self.host})
        return out

    def broadcast(self, msg, skip=None):
        data = json.dumps(msg)
        for pid, c in list(self.conns.items()):
            if pid != skip:
                c.send(data)

    def send_room(self):
        r = self.roster()
        for pid, c in list(self.conns.items()):
            c.send(json.dumps({"t": "room", "code": self.code,
                               "host": pid == self.host, "players": r}))


def new_code():
    with rooms_lock:
        for _ in range(400):
            c = "".join(random.choice(CODE_ALPHABET) for _ in range(4))
            if c not in rooms:
                rooms[c] = Room(c)
                return c
    return None


class WSConn:
    """One websocket connection, living on the request thread."""

    def __init__(self, handler):
        self.h = handler
        self.sock = handler.connection
        self.lock = threading.Lock()
        self.alive = True
        self.pid = None
        self.room = None
        self.name = "Player"
        self.kart = 0
        self.dec = 0
        self.drv = 0

    # ---- framing -------------------------------------------------
    def send(self, text):
        if not self.alive:
            return
        data = text.encode("utf-8")
        n = len(data)
        if n < 126:
            head = struct.pack("!BB", 0x81, n)
        elif n < (1 << 16):
            head = struct.pack("!BBH", 0x81, 126, n)
        else:
            head = struct.pack("!BBQ", 0x81, 127, n)
        try:
            with self.lock:
                self.sock.sendall(head + data)
        except Exception:
            self.alive = False

    def _read(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.h.rfile.read(n - len(buf))
            if not chunk:
                raise ConnectionError("closed")
            buf += chunk
        return buf

    def recv(self):
        """Return one text message, or None when the socket closes."""
        while True:
            b1, b2 = struct.unpack("!BB", self._read(2))
            op = b1 & 0x0F
            masked = b2 & 0x80
            ln = b2 & 0x7F
            if ln == 126:
                ln = struct.unpack("!H", self._read(2))[0]
            elif ln == 127:
                ln = struct.unpack("!Q", self._read(8))[0]
            if ln > 1 << 20:                      # 1 MB is far more than any message
                raise ConnectionError("frame too big")
            mask = self._read(4) if masked else None
            payload = self._read(ln) if ln else b""
            if mask:
                payload = bytes(payload[i] ^ mask[i % 4] for i in range(len(payload)))
            if op == 0x8:                          # close
                return None
            if op == 0x9:                          # ping -> pong
                with self.lock:
                    try:
                        self.sock.sendall(struct.pack("!BB", 0x8A, len(payload)) + payload)
                    except Exception:
                        self.alive = False
                continue
            if op == 0x1:
                return payload.decode("utf-8", "replace")
            # ignore binary and continuation frames

    # ---- protocol ------------------------------------------------
    def leave(self):
        r = self.room
        if not r or not self.pid:
            return
        with rooms_lock:
            r.conns.pop(self.pid, None)
            if self.pid in r.order:
                r.order.remove(self.pid)
            if r.host == self.pid:
                r.host = r.order[0] if r.order else None
            empty = not r.conns
            if empty:
                rooms.pop(r.code, None)
        if not empty:
            r.send_room()
        self.room = None

    def handle(self, msg):
        t = msg.get("t")

        if t == "host":
            code = new_code()
            if not code:
                self.send(json.dumps({"t": "err", "msg": "Too many rooms open."}))
                return
            self.pid = msg.get("id") or os.urandom(4).hex()
            self.name = str(msg.get("name", "Player"))[:12]
            self.kart = int(msg.get("kart", 0)) % 12
            self.dec = int(msg.get("dec", 0)) % 6
            self.drv = int(msg.get("drv", 0)) % 8
            with rooms_lock:
                r = rooms[code]
                r.conns[self.pid] = self
                r.order.append(self.pid)
                r.host = self.pid
            self.room = r
            r.send_room()
            self.send(json.dumps({"t": "cfg", **r.cfg}))
            print("  room %s opened" % code)
            return

        if t == "join":
            code = str(msg.get("room", "")).upper()[:4]
            with rooms_lock:
                r = rooms.get(code)
            if not r:
                self.send(json.dumps({"t": "err", "msg": "No room with the code " + code + "."}))
                return
            if r.started:
                self.send(json.dumps({"t": "err", "msg": "That race has already started."}))
                return
            if len(r.order) >= MAX_RACERS:
                self.send(json.dumps({"t": "err",
                    "msg": "That room is full (%d racers)." % MAX_RACERS}))
                return
            self.pid = msg.get("id") or os.urandom(4).hex()
            self.name = str(msg.get("name", "Player"))[:12]
            self.kart = int(msg.get("kart", 0)) % 12
            self.dec = int(msg.get("dec", 0)) % 6
            self.drv = int(msg.get("drv", 0)) % 8
            with rooms_lock:
                r.conns[self.pid] = self
                r.order.append(self.pid)
            self.room = r
            r.send_room()
            self.send(json.dumps({"t": "cfg", **r.cfg}))
            print("  racer joined room %s (%d in the room)" % (code, len(r.order)))
            return

        r = self.room
        if not r:
            return
        r.touched = time.time()

        if t == "me":
            self.name = str(msg.get("name", self.name))[:12]
            self.kart = int(msg.get("kart", self.kart)) % 12
            self.dec = int(msg.get("dec", self.dec)) % 6
            self.drv = int(msg.get("drv", self.drv)) % 8
            r.send_room()
        elif t == "cfg" and r.host == self.pid:
            r.cfg = {"track": max(0, min(MAX_TRACKS - 1, int(msg.get("track", 0)))),
                     "laps": max(1, min(6, int(msg.get("laps", 3)))),
                     "fuel": max(0, min(2, int(msg.get("fuel", 1)))),
                     "topics": [int(x) for x in msg.get("topics", [0, 1, 2, 3, 4, 5])][:6] or [0]}
            r.broadcast({"t": "cfg", **r.cfg}, skip=self.pid)
        elif t == "start" and r.host == self.pid:
            r.started = True
            r.states.clear()
            r.broadcast({"t": "go", "roster": msg.get("roster", []),
                         "track": msg.get("track", 0), "laps": msg.get("laps", 3),
                         "fuel": msg.get("fuel", 1),
                         "topics": msg.get("topics", [0, 1, 2, 3, 4, 5])}, skip=self.pid)
            print("  room %s: race started with %d human racers" % (r.code, len(r.order)))
        elif t == "reopen" and r.host == self.pid:
            r.started = False                    # let latecomers into the next race
            r.states.clear()
            r.send_room()
            print("  room %s reopened for more racers" % r.code)
        elif t == "state":
            # Merge rather than relay: one snapshot per tick to everyone, so 30
            # racers cost 30 sends a tick instead of 900.
            for st in msg.get("s", []):
                if isinstance(st, dict) and "i" in st:
                    r.states[st["i"]] = st
            r.dirty = True
        elif t == "ev":
            r.broadcast(msg, skip=self.pid)
        elif t == "leave":
            self.leave()


def pump():
    """Broadcast one merged snapshot per room, SNAP_HZ times a second."""
    period = 1.0 / SNAP_HZ
    while True:
        time.sleep(period)
        with rooms_lock:
            live = [r for r in rooms.values() if r.dirty and r.states]
        for r in live:
            r.dirty = False
            try:
                payload = json.dumps({"t": "snap", "s": list(r.states.values())})
            except Exception:
                continue
            for c in list(r.conns.values()):
                c.send(payload)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "GrandPrix/1.0"

    def log_message(self, *a):
        pass                                    # keep the teacher's screen clean

    def _body(self, code, data, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]

        if path == "/favicon.ico":
            # Browsers request this automatically; keep a clean console without
            # adding an external asset to the single-file game.
            return self._body(204, b"", "image/x-icon")

        if path == "/ws":
            return self.websocket()

        if path == "/api/ping":
            # CORS so the game can find this server even when opened from a file
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            body = json.dumps({"ok": True, "ver": 1, "port": self.server.server_address[1]}).encode()
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path in ("/", "/index.html", "/" + GAME.replace(" ", "%20")):
            fn = os.path.join(HERE, GAME)
            if not os.path.exists(fn):
                return self._body(404, b"Game file not found next to the server.", "text/plain")
            with open(fn, "rb") as f:
                return self._body(200, f.read(), "text/html; charset=utf-8")

        self._body(404, b"Not found", "text/plain")

    def websocket(self):
        key = self.headers.get("Sec-WebSocket-Key")
        if not key or "websocket" not in (self.headers.get("Upgrade") or "").lower():
            return self._body(400, b"Expected a websocket upgrade", "text/plain")
        accept = base64.b64encode(hashlib.sha1(key.encode() + GUID).digest()).decode()
        self.wfile.write(("HTTP/1.1 101 Switching Protocols\r\n"
                          "Upgrade: websocket\r\n"
                          "Connection: Upgrade\r\n"
                          "Sec-WebSocket-Accept: " + accept + "\r\n\r\n").encode())
        self.wfile.flush()
        self.close_connection = True
        conn = WSConn(self)
        announce_devices(+1)
        try:
            self.connection.settimeout(None)
            while True:
                raw = conn.recv()
                if raw is None:
                    break
                try:
                    msg = json.loads(raw)
                except Exception:
                    continue
                if isinstance(msg, dict):
                    conn.handle(msg)
        except Exception:
            pass
        finally:
            conn.alive = False
            conn.leave()
            announce_devices(-1)


def pause(msg="   Press Return to close this window. "):
    """Wait for the teacher — but never block a server with no keyboard."""
    if CLOUD or not sys.stdin.isatty():
        return
    try:
        input(msg)
    except (EOFError, KeyboardInterrupt):
        pass


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))         # never actually sends anything
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def bonjour_name():
    """This Mac's .local name. Unlike the IP, it does not change."""
    try:
        import subprocess
        n = subprocess.run(["/usr/sbin/scutil", "--get", "LocalHostName"],
                           capture_output=True, text=True, timeout=3).stdout.strip()
        return (n + ".local") if n else None
    except Exception:
        return None


def all_lan_ips():
    """Every address a phone on the same wi-fi could reach us on, best first."""
    best = lan_ip()
    found = [best] if best != "127.0.0.1" else []
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if ip.startswith("127.") or ip in found:
                continue
            # skip tunnel / link-local ranges a phone cannot use
            if ip.startswith("169.254."):
                continue
            found.append(ip)
    except Exception:
        pass
    return found or ["127.0.0.1"]


def main():
    port = int(os.environ.get("PORT") or (sys.argv[1] if len(sys.argv) > 1 else 8000))
    if not os.path.exists(os.path.join(HERE, GAME)):
        print("\n   Could not find '%s' next to this script." % GAME)
        print("   Keep race_server.py in the SAME folder as the game.\n")
        pause()
        sys.exit(1)
    srv = None
    attempts = 1 if CLOUD else 12          # a host gives you one port; use it or fail loudly
    for attempt in range(attempts):
        try:
            cls = ThreadingHTTPServer
            cls.allow_reuse_address = True      # reclaim a port a previous run left in TIME_WAIT
            srv = cls(("0.0.0.0", port + attempt), Handler)
            port = port + attempt
            break
        except OSError as e:
            if attempt == 0:
                print("\n   Port %d is already in use — trying the next one..." % port)
            continue
    if srv is None:
        print("\n   Could not open a port between %d and %d." % (port, port + 11))
        print("   Is the server already running in another window? Close it and try again.\n")
        pause()
        sys.exit(1)
    srv.daemon_threads = True
    threading.Thread(target=pump, daemon=True).start()
    if CLOUD:
        print("Proportion Grand Prix - race server listening on port %d" % port)
        print("Room capacity %d. Health check: /api/ping" % MAX_RACERS)
        threading.Thread(target=pump, daemon=True).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
        return

    ips = all_lan_ips()
    name = bonjour_name()
    line = "  http://%s:%d  " % (ips[0], port)
    bar = "=" * (max(len(line), 44) + 2)
    print("\n" + bar)
    print("   PROPORTION GRAND PRIX — race server running")
    print(bar)
    if name:
        nline = "  http://%s:%d  " % (name, port)
        print("\n   THE LINK TO GIVE YOUR STUDENTS (same every lesson):\n")
        print("  " + "-" * len(nline))
        print(" " + nline)
        print("  " + "-" * len(nline))
        print("\n   If a device cannot open that name, use this instead")
        print("   (this one CHANGES every time the Mac rejoins wi-fi):\n")
    else:
        print("\n   TYPE THIS INTO THE BROWSER ON EACH PHONE / IPAD:\n")
    print("  " + "-" * len(line))
    print(" " + line)
    print("  " + "-" * len(line))
    if len(ips) > 1:
        print("\n   This computer also answers on:")
        for extra in ips[1:]:
            print("       http://%s:%d" % (extra, port))
    print("\n   If a phone says it cannot connect, check in this order:")
    print("     1. Is the phone on the SAME wi-fi as this Mac? (not mobile data)")
    print("     2. Did you type http:// and the :%d on the end?" % port)
    print("     3. Is this window still open? Closing it stops the race.")
    print("     4. School wi-fi sometimes stops devices talking to each other.")
    print("        Test it with a phone on your home wi-fi to tell the two apart.")
    print("\n   Everyone races through that address, INCLUDING YOU.")
    print("   Do not double-click the game file - that is a solo-only copy.")
    print("   Up to %d racers per room. One person taps 'New room' and reads" % MAX_RACERS)
    print("   out the 4-letter code; everyone else types it and taps 'Join room'.")
    print("\n   Watch the line below: it counts every device that reaches this Mac.")
    print("   If it stays at 0, the phone is not getting here at all.\n")
    print("   Press Ctrl+C here to stop the server.\n")
    # open the teacher's own browser on the right page, so they never have to
    # double-click the game file (pointless inside a hosting container)
    if not CLOUD:
        def _open():
            time.sleep(0.7)
            try:
                webbrowser.open("http://127.0.0.1:%d/" % port)
            except Exception:
                pass
        threading.Thread(target=_open, daemon=True).start()

    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n   Server stopped. See you next lesson.\n")
    except Exception as e:
        print("\n   The server stopped with an error: %s\n" % e)
        pause()


if __name__ == "__main__":
    main()
