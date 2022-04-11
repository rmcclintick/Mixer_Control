# Based on examples at
# https://wiki.python.org/moin/UdpCommunication and https://docs.python.org/2/library/socketserver.html
import socket
import socketserver
import threading
from typing import Type

from ui import MixerControl

JAVA_CLIENT_HOST = "0.0.0.0"
JAVA_CLIENT_PORT = 4445
PYTHON_SERVER_PORT = 4446
LOCAL_IP = "0.0.0.0"  # "192.168.1.198"

ui: Type = MixerControl
my_socket: Type = socket


def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((JAVA_CLIENT_HOST, JAVA_CLIENT_PORT))
    try:
        sock.sendall(message.encode())
        print("sending: " + message)
    finally:
        sock.close()


def dispose():
    global server
    server.shutdown()
    server.server_close()


# Put the code you want to do something based on when you get data here.
def on_data(data, sock):
    global ui
    message = data.decode("utf-8")
    # print(message);
    if message == "refresh":
        namelist = ui.refreshSessions(ui)
        string_list = "refresh"
        for name in namelist:
            string_list += " " + name
        send_message(string_list)
        print("sent namelist")
    else: # probably needs to change later
        tuple = message.split()
        id = tuple[0]
        value = tuple[1]
        ui.update_mixer(ui, int(value), int(id))


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    print("thread")

    def handle(self):
        global my_socket
        global JAVA_CLIENT_HOST
        # print(str(self.request))
        # print("ADDRESS" + str(self.client_address))
        JAVA_CLIENT_HOST = self.client_address[0]
        data = self.request[0].strip()
        my_socket = self.request[1]
        # print(my_socket)
        on_data(data, my_socket)


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
