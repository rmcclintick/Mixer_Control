
from tkinter import *
from audio_controller import *
from pycaw.pycaw import AudioUtilities
  


names = []
faders = []
audioControllers = []

def createFaders():
    global names
    global faders
    global audioControllers
    sessions = AudioUtilities.GetAllSessions()
    for i in sessions:
        if hasattr(i.Process, 'name'):
            names.append(i.Process.name())
    names = list(dict.fromkeys(names))

    for i in range(len(names)):
        ac = AudioController(names[i])
        audioControllers.append(ac)
        faders.append(Scale(root, from_ = 0, to = 1, resolution = 0.01,
                            orient = HORIZONTAL, command = updateMixer,
                            label = names[i], length = 200))
        faders[i].set(ac.process_volume())
    for fader in faders:
        fader.pack()

def createRefreshBtn():
    b2 = Button(root, text ="Refresh",
            command = refreshSessions,
            padx = 10, pady = 10)
    b2.pack()


def refreshSessions():
    global names
    global faders
    global audioControllers
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
                            orient = HORIZONTAL, command = updateMixer,
                            label = names[i], length = 200))
        faders[i].set(ac.process_volume())
    for fader in faders:
        fader.pack()

def updateMixer(val):
    for i in range(len(faders)):
        audioControllers[i].set_volume(faders[i].get())

def getProgNameList():
    global names
    return names


root = Tk()
root.title('Mixer Control')
root.geometry("250x300") 
createRefreshBtn()
createFaders()

#l2 = Label(root)

#l2.pack()
root.mainloop()
