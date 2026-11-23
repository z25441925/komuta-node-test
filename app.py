import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

TCP_PORT = 9000
UDP_PORT = 9000
HTTP_PORT = 8080


def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", TCP_PORT))
    s.listen(50)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_tcp, args=(conn,), daemon=True).start()


def handle_tcp(conn):
    try:
        data = conn.recv(4096)
        conn.sendall(b"KOMUTA-TCP-OK " + data)
    except OSError:
        pass
    finally:
        conn.close()


def udp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", UDP_PORT))
    while True:
        data, addr = s.recvfrom(4096)
        s.sendto(b"KOMUTA-UDP-OK " + data, addr)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"KOMUTA-HTTP-OK"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()
    HTTPServer(("0.0.0.0", HTTP_PORT), Handler).serve_forever()
