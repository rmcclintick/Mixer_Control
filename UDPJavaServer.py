# Based on examples at https://wiki.python.org/moin/UdpCommunication and https://docs.python.org/2/library/socketserver.html
import socket
import threading
import socketserver
import time
from ui import MixerControl

JAVA_SERVER_HOST = "192.168.1.245"
JAVA_SERVER_PORT = 4445
PYTHON_SERVER_PORT = 4446
mixer = None

def sendMessage(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((JAVA_SERVER_HOST, JAVA_SERVER_PORT))
    try:
        sock.sendall(message.encode())
    finally:
        sock.close()

def dispose():
    server.shutdown()
    server.server_close()

# Put the code you want to do something based on when you get data here.
def onData(data):
    message = data.decode("utf-8")
    if message == "refresh":
        mixer.refreshSessions(mixer)
    else:
        mixer.updateMixer(mixer, int(message), 0)
    
    
class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    print("thread")
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        onData(data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    global mixer
    mixer = 
    print(mixer.getLength())
    #pass

# This starts up the server, sends a few messages and then shuts the server down.
##server = ThreadedUDPServer(("192.168.1.198", PYTHON_SERVER_PORT), ThreadedUDPRequestHandler)
##server_thread = threading.Thread(target=server.serve_forever)
##server_thread.daemon = True
##server_thread.start()
##print("Server loop running in thread: ", server_thread.name)
#time.sleep(3)
#sendMessage("Hello Java 1")
#time.sleep(3)
#sendMessage("Hello Java 2")
#time.sleep(3)
#sendMessage("Hello Java 3")
#time.sleep(5)

#time.sleep(60)
##print("\nShutting down Python server")

