#!/usr/bin/env python3
"""
Local preview server with live reload.

    python3 dev.py            # http://localhost:8000
    python3 dev.py 3000       # a different port

Save any file in this folder and the browser refreshes itself. This is a
development tool only -- it is never deployed, and the files it serves are
untouched on disk. GitHub Pages serves the real thing.
"""

import os
import sys
import time
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
WATCH_EXT = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".vscode"}
POLL_TIMEOUT = 25      # seconds a held request waits before answering
POLL_INTERVAL = 0.3

RELOAD_SNIPPET = b"""
<script>
/* injected by dev.py -- not present in the deployed site */
(function () {
  var current = null;
  function poll() {
    fetch('/__reload')
      .then(function (r) { return r.text(); })
      .then(function (stamp) {
        if (current !== null && stamp !== current) { location.reload(); return; }
        current = stamp;
        poll();
      })
      .catch(function () { setTimeout(poll, 1000); });
  }
  poll();
})();
</script>
"""


def stamp():
    """A fingerprint of the tree: newest mtime plus the file count."""
    newest, count = 0.0, 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1].lower() not in WATCH_EXT:
                continue
            try:
                newest = max(newest, os.stat(os.path.join(dirpath, name)).st_mtime)
                count += 1
            except OSError:
                pass
    return "%.3f-%d" % (newest, count)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        if self.path.split("?")[0] == "/__reload":
            self.hold_until_changed()
            return
        if self.serve_html():
            return
        super().do_GET()

    def hold_until_changed(self):
        """Answer only once something changes, or after a timeout."""
        start = initial = stamp()
        deadline = time.time() + POLL_TIMEOUT
        while start == initial and time.time() < deadline:
            time.sleep(POLL_INTERVAL)
            start = stamp()
        body = start.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def serve_html(self):
        """Serve .html with the reload snippet injected. Returns True if handled."""
        rel = posixpath.normpath(self.path.split("?")[0].lstrip("/"))
        if rel in (".", ""):
            rel = "index.html"
        full = os.path.join(ROOT, rel)
        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        if not full.endswith(".html") or not os.path.isfile(full):
            return False

        with open(full, "rb") as fh:
            body = fh.read()
        if b"</body>" in body:
            body = body.replace(b"</body>", RELOAD_SNIPPET + b"</body>", 1)
        else:
            body += RELOAD_SNIPPET

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        return True

    def end_headers(self):
        # Never cache during development, or edits to css/js would not show up.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "__reload" in (args[0] if args else ""):
            return                       # the poll would flood the terminal
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError as exc:
        print("Could not bind port %d: %s" % (port, exc))
        print("Something else is using it. Try:  python3 dev.py %d" % (port + 1))
        sys.exit(1)

    print("\n  Live preview:  http://localhost:%d" % port)
    print("  Watching %s" % ROOT)
    print("  Save a file and the browser refreshes.  Ctrl-C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.\n")


if __name__ == "__main__":
    main()
