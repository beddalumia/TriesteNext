from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

class myGUI:
    def __init__(self, win, ims):
        x0, xt0, y0, yt0 = 100, 100, 250, 300
        #---- First label and entry -------
        self.lbl0 = Label(win, text='Numero di chicchi')
        self.lbl0.config(font=('Arial', 22))
        self.lbl0.place(x=x0, y=y0)
        self.Nriso = Entry()
        self.Nriso.place(x=xt0, y=yt0)
        self.Nriso.insert(END, str(0))
        self.t_0 = float(self.Nriso.get())
        self.ims = ims
        self.pi = 0.0
        self.pistr = "π ="+str(self.pi)
        self.pilabel = Label(win, text="π =")
        self.pilabel.config(font=('LatinModern', 22))
        self.pilabel.place(x=x0, y=y0+200)

        #---- Compute button -------
        self.btn = Button(win, text='Calcola')
        self.btn.bind('<Button-1>', self.update)
        self.btn.place(x=xt0, y=y0 + 100)

        self.figure, self.ax = plt.subplots(figsize=(10, 10), dpi=100)

        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_aspect('equal')
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="lightskyblue") )
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=0.5 ,color="tab:blue") )

        #---- Show the plot-------
        self.plots = FigureCanvasTkAgg(self.figure, win)
        self.plots.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=0)

      #   self.result, self.box = plt.subplots(figsize=(3, 1), dpi=100)
      #   self.result.patch.set_alpha(0)
      #   self.box.patch.set_alpha(0)
      #   self.rplots = FigureCanvasTkAgg(self.result, win)
      #   self.rplots.get_tk_widget().pack(side=LEFT, expand=0)

    def update(self, event):
        self.ax.cla()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_aspect('equal')
        Nriso = int(self.Nriso.get())
        x = np.random.random(Nriso)
        y = np.random.random(Nriso)
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="lightskyblue") )
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=0.5 ,color="tab:blue") )
        self.ax.scatter(x,y,marker="")
        N=len(x)
        for xi, yi in zip(x,y):
           i =  np.random.randint(0,7)
           image=self.ims[i]
           im = OffsetImage(image, zoom=10/self.ax.figure.dpi)
           im.image.axes = self.ax
           ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
           self.ax.add_artist(ab)

        self.plots.draw()

        self.pi=0
        for i in range(len(x)):
          if ( np.sqrt( (x[i]-0.5)**2+(y[i]-0.5)**2 )<0.5 ): self.pi+=1.0
        self.pi = self.pi/Nriso * 4
        self.pilabel.config(text="π = "+str(self.pi))





paths=[]
ims=[]
for i in range(1,9):
    path='riso'+f"{i}"+'.png'
    paths.append(path)
    #ims.append(image.imread(path))
    #image = plt.imread(path)[116:116+30, 236:236+30]
    ims.append(plt.imread(path)) #[6:6+30, 126:126+30])

window = Tk()
window.attributes("-fullscreen",True)
myGUI(window,ims)
window.title('Riso Monte Carlos')
window.geometry("600x800+10+10")
window.mainloop()