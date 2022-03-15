
from tkinter import *
from audio_controller import *
from pycaw.pycaw import AudioUtilities
  
root = Tk()  
root.geometry("400x300") 
v2 = DoubleVar()
ac = AudioController('msedge.exe')

sessions = AudioUtilities.GetAllSessions()
names = []
for i in sessions:
    if hasattr(i.Process, 'name'):
        names.append(i.Process.name())
names = list(dict.fromkeys(names))
#print(names)
faders = []
audioControllers = []                          
    

def show2(val):
    for i in range(len(faders)):
        audioControllers[i].set_volume(faders[i].get())
##    vol = v2.get() / 100
##    sel = "Vertical Scale Value = " + str(v2.get()) 
##    l2.config(text = sel, font =("Courier", 14))
##    ac.set_volume(float(value) / 100)

for i in range(len(names)):
    ac = AudioController(names[i])
    audioControllers.append(ac)
    faders.append(Scale(root, 
                        from_ = 0, to = 1,
                        resolution = 0.01,
                        orient = HORIZONTAL,
                        command = show2,
                        label = names[i],
                        length = 200,
                        ))
    faders[i].set(ac.process_volume())
    

  
##s2 = Scale( root, variable = v2,
##           from_ = 100, to = 0,
##           orient = VERTICAL,
##            command = show2)

#s2.set(float(ac.process_volume() * 100))
  
  
b2 = Button(root, text ="Set Volume",
            command = show2,
            bg = "purple", 
            fg = "white")
  
l2 = Label(root)
  
#s2.pack()
for fader in faders:
    fader.pack()

b2.pack()
l2.pack()
  
root.mainloop()
