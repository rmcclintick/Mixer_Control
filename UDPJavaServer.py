# Based on examples at https://wiki.python.org/moin/UdpCommunication and https://docs.python.org/2/library/socketserver.html
import socket
import threading
import socketserver
import time

JAVA_SERVER_HOST = "192.168.1.245"
JAVA_SERVER_PORT = 4445
PYTHON_SERVER_PORT = 4446

def sendMessage(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((JAVA_SERVER_HOST, JAVA_SERVER_PORT))
    try:
        sock.sendall(message.encode())
    finally:
        sock.close()

# Put the code you want to do something based on when you get data here.
def onData(data):
    print("Python got data: " + data.decode("utf-8"), end = "\n")
    
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        onData(data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass

# This starts up the server, sends a few messages and then shuts the server down.
server = ThreadedUDPServer(("192.168.1.198", PYTHON_SERVER_PORT), ThreadedUDPRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread: ", server_thread.name)
time.sleep(3)
#sendMessage("Hello Java 1")
time.sleep(3)
#sendMessage("Hello Java 2")
time.sleep(3)
#sendMessage("Hello Java 3")
time.sleep(5)

print("\nShutting down Python server")
server.shutdown()
server.server_close()
