
from tkinter import *
from audio_controller import *
from pycaw.pycaw import AudioUtilities
from UDPJavaServer import *


LOCAL_IP = "192.168.1.198"
PYTHON_SERVER_PORT = 4446


names = []
faders = []
audioControllers = []
root = None
server = None
server_thread = None

class MixerControl:
    
    def updateMixers(self, val):
        global audioControllers
        for i in range(len(faders)):
            audioControllers[i].set_volume(faders[i].get())

    def updateMixer(self, val, i):
        global audioControllers
        global faders
        print(i)
        print(len(faders))
        print(len(audioControllers))
        audioControllers[i].set_volume(val / 100)

            
    def createFaders(self):
        global names
        global faders
        global audioControllers
        global root
        sessions = AudioUtilities.GetAllSessions()
        for i in sessions:
            if hasattr(i.Process, 'name'):
                names.append(i.Process.name())
        names = list(dict.fromkeys(names))

        for i in range(len(names)):
            global audioController
            ac = AudioController(names[i])
            audioControllers.append(ac)
            faders.append(Scale(root, from_ = 0, to = 1, resolution = 0.01,
                                orient = HORIZONTAL, command = self.updateMixers,
                                label = names[i], length = 200))
            faders[i].set(ac.process_volume())
        for fader in faders:
            fader.pack()
        print("AC length :" + str(len(audioControllers)))

    #debug only
    def printMessage(message):
        print(message)
    def getLength():
        global audioControllers
        return len(audioControllers)

    def refreshSessions(self):
        global names
        global faders
        global audioControllers
        global root
        sessions = AudioUtilities.GetAllSessions()
        
        names.clear()
        for i in sessions:
            if hasattr(i.Process, 'name'):
                names.append(i.Process.name())
        names = list(dict.fromkeys(names))

        for fader in faders:
            fader.destroy()
        faders.clear()
        audioControllers.clear()
        for i in range(len(names)):
            ac = AudioController(names[i])
            audioControllers.append(ac)
            faders.append(Scale(root, from_ = 0, to = 1, resolution = 0.01,
                                orient = HORIZONTAL, command = self.updateMixers,
                                label = names[i], length = 200))
            faders[i].set(ac.process_volume())
        for fader in faders:
            fader.pack()

            
    def createRefreshBtn(self):
        global root
        b2 = Button(root, text ="Refresh",
                command = self.refreshSessions,
                padx = 10, pady = 10)
        b2.pack()


    def getProgNameList():
        global names
        return names

    def onClosing(self):
        global server
        server.shutdown()
        server.server_close()

    def __init__(self):
        global root
        global server
        global server_thread
        root = Tk()
        root.title('Mixer Control')
        root.geometry("250x300")
        self.createRefreshBtn()
        self.createFaders()
        #root.protocol("WM_DELETE_WINDOW", self.onClosing)
        root.mainloop()

        

def main():
    ui = MixerControl()
    server = ThreadedUDPServer((LOCAL_IP, PYTHON_SERVER_PORT), ThreadedUDPRequestHandler, ui)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    

if __name__ == "__main__":
    main()

