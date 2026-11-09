
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PORT = int(os.getenv("PORT", "8003"))
MESSAGE = os.getenv("MESSAGE", "Tickets online")
MODE = os.getenv("MODE", "test")
APP_VERSION = os.getenv("APP_VERSION", "1.0")

DATA_DIR = "/data"
STATE_FILE = os.path.join(DATA_DIR, "state.json")

tickets = {
    "open": 5,
    "closed": 10
}


def load_state():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            return json.load(file)

    return {"requests": 0}


def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)


class TicketHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-App-Name", "Ticket Service")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        state = load_state()
        state["requests"] += 1
        save_state(state)

        if self.path == "/tickets":
            response = {
                "message": MESSAGE,
                "open": tickets["open"],
                "closed": tickets["closed"],
                "requests": state["requests"]
            }
            self.send_json(response)

        elif self.path == "/health":
            self.send_json({"status": "healthy"})

        elif self.path == "/config":
            response = {
                "PORT": PORT,
                "MODE": MODE,
                "MESSAGE": MESSAGE,
                "APP_VERSION": APP_VERSION
            }
            self.send_json(response)

        else:
            self.send_json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        print(format % args)


server = HTTPServer(("0.0.0.0", PORT), TicketHandler)

print(f"Server started on port {PORT}")

server.serve_forever()
