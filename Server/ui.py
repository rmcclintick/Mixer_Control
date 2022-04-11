from tkinter import *

from audio_controller import *

LOCAL_IP = "192.168.1.198"
PYTHON_SERVER_PORT = 4446

names = []
faders = []
audioControllers = []
root = None


def update_mixers(val):
    global audioControllers
    for i in range(len(faders)):
        audioControllers[i].set_volume(faders[i].get())


class MixerControl:

    def update_mixer(self, val, i):
        global audioControllers
        global faders
        audioControllers[i].set_volume(val / 100)
        faders[i].set(val / 100)

    def create_faders(self):
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
            ac = AudioController(names[i])
            audioControllers.append(ac)
            faders.append(Scale(root, from_=0, to=1, resolution=0.01,
                                orient=HORIZONTAL, command=update_mixers,
                                label=names[i], length=200))
            faders[i].set(ac.process_volume())
        for fader in faders:
            fader.pack()
        print("AC length :" + str(len(audioControllers)))

    # debug only
    def printMessage(message):
        print(message)

    def getLength(self):
        global audioControllers
        return len(audioControllers)

    def refreshSessions(self) -> list:
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
            faders.append(Scale(root, from_=0, to=1, resolution=0.01,
                                orient=HORIZONTAL, command=update_mixers,
                                label=names[i], length=200))
            faders[i].set(ac.process_volume())
        for fader in faders:
            fader.pack()
        return names

    def createRefreshBtn(self):
        global root
        b2 = Button(root, text="Refresh",
                    command=self.refreshSessions,
                    padx=10, pady=10)
        b2.pack()

    def getProgNameList(self):
        global names
        return names

    def onClosing(self):
        pass
        # server.shutdown()
        # server.server_close()

    def __init__(self):
        global root
        root = Tk()
        root.title('Mixer Control')
        root.geometry("250x300")
        self.createRefreshBtn()
        self.create_faders()
        # root.protocol("WM_DELETE_WINDOW", self.onClosing)
        root.mainloop()
