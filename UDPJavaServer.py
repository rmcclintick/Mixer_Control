# Based on examples at
# https://wiki.python.org/moin/UdpCommunication and https://docs.python.org/2/library/socketserver.html
import socket
import socketserver
import threading
from typing import Type

from ui import MixerControl

JAVA_SERVER_HOST = "192.168.1.245"
JAVA_SERVER_PORT = 4445
PYTHON_SERVER_PORT = 4446
LOCAL_IP = "192.168.1.198"

ui: Type[MixerControl] = MixerControl


def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((JAVA_SERVER_HOST, JAVA_SERVER_PORT))
    try:
        sock.sendall(message.encode())
    finally:
        sock.close()


def dispose():
    global server
    server.shutdown()
    server.server_close()


# Put the code you want to do something based on when you get data here.
def on_data(data):
    global ui
    message = data.decode("utf-8")
    if message == "refresh":
        ui.refreshSessions(ui)
        print("refresh")
    else:
        ui.update_mixer(ui, int(message), 0)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    print("thread")

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        on_data(data)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


server = ThreadedUDPServer


def main():
    global ui
    global server

    server = ThreadedUDPServer((LOCAL_IP, PYTHON_SERVER_PORT), ThreadedUDPRequestHandler, ui)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    ui = MixerControl()
    print(server_thread)


if __name__ == "__main__":
    main()
