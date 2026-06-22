import http.server
import socketserver
import os
import sys

# Default port (matches previous instructions)
DEFAULT_PORT = 8787

# Directories we never want to serve
BLOCKED_DIRS = {".git", ".github", ".svn", "node_modules", "__pycache__"}

class SafeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        """Override to block sensitive paths."""
        path = super().translate_path(path)

        # Check if any blocked directory appears in the path
        parts = path.split(os.sep)
        if any(part in BLOCKED_DIRS for part in parts):
            self.send_error(404, "File not found")
            return ""

        return path

    def log_message(self, format, *args):
        """Cleaner logging - only show main requests."""
        if not args or not args[0].startswith("GET"):
            return
        # Only log interesting requests (ignore favicon, etc.)
        if "/favicon" not in args[0]:
            print(f"{self.address_string()} - {args[0]}")

def main():
    # Determine directory to serve (always the folder containing this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)

    # Allow custom port from command line
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port '{sys.argv[1]}', using default {DEFAULT_PORT}")

    handler = SafeHTTPRequestHandler

    # Bind to all interfaces so it works in Codespaces / containers
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}"
        print("🌿 CalmTap Safe Server")
        print(f"   Serving from: {os.getcwd()}")
        print(f"   URL:          {url}")
        print("   Press Ctrl+C to stop.\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()
