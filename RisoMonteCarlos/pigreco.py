from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

errorfont = {'family': 'Arial',
            'color':  'white',
            'weight': 'bold',
            'size': 32
            }

class myGUI:
    def __init__(self, win, ims):
        self.window=win
        x0, xt0, y0, yt0 = 100, 100, 250, 300
        #---- Grains label and entry -------
        self.lbl0 = Label(win, text='Numero di chicchi')
        self.lbl0.config(font=('Arial', 22))
        self.lbl0.place(x=x0, y=y0)
        self.Nriso = Entry()
        self.Nriso.place(x=xt0, y=yt0)
        self.Nriso.insert(END, str(0))
        self.t_0 = float(self.Nriso.get())
        self.ims = ims
        # PI label and accuracy label
        self.pi = 0.0
        self.pilabel = Label(win, text="π =")
        self.pilabel.config(font=('LatinModern', 32))
        self.pilabel.place(x=x0, y=y0+200)
        #
        self.piacclabel = Label(win,text="Precisione: ")
        self.piacclabel.config(font=('Arial',22))
        self.piacclabel.place(x=x0,y=y0+250)
        
        # Computational Effort Label
        self.effortlabel = Label(win,text="👀")
        self.effortlabel.config(font=("Arial",60))
        self.effortlabel.place(x=x0, y=y0+300)
        
        #---- Compute button -------
        self.btn1 = Button(win, text='Calcola')
        self.btn1.bind('<Button-1>', self.update)
        self.btn1.place(x=xt0, y=y0 + 100)

        self.figure, self.ax = plt.subplots(figsize=(10, 10), dpi=100)

        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_aspect('equal')
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="lightskyblue") )
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=0.5 ,color="tab:blue") )

        #---- Show the plot-------
        self.plots = FigureCanvasTkAgg(self.figure, win)
        self.plots.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=0)

        #---- Switch for rice or scatterplot

        self.switch_frame = Frame(win)
        self.switch_frame.place(x=100,y=120)
        
        self.switch_variable = StringVar(value="Riso")
        self.riso_button = Radiobutton(self.switch_frame, text="Riso", variable=self.switch_variable,
                                       indicatoron=False, value="Riso", width=8)
        self.punti_button = Radiobutton(self.switch_frame, text="Punti", variable=self.switch_variable,
                                        indicatoron=False, value="Punti", width=8)
        self.riso_button.pack(side="left")
        self.punti_button.pack(side="right")

        
    def update(self, event):

        Nriso = int(self.Nriso.get())

        #ERROR IF TOO MANY/FEW GRAINS
        if(Nriso>10**6):
            self.ax.cla()
            self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="red") )
            self.ax.text(0.2,0.5,"TROPPO DIFFICILE",fontdict=errorfont)
            self.pilabel.config(text="π = ?")
            self.piacclabel.config(text="Precisione: ?")
            self.effortlabel.config(text="💀")
            self.plots.draw()
        elif(Nriso<=0):
            self.pilabel.config(text="π = ?")
            self.piacclabel.config(text="Precisione: ?")
            self.effortlabel.config(text="Maddai! 🤡")
        else:
            
            if(Nriso<100):
                self.effortlabel.config(text="Facile! 🙃")
            elif(Nriso<1000):
                self.ax.cla()
                self.effortlabel.config(text="⏳...")
                self.window.update()
                self.effortlabel.config(text="Oook! 🥲")
            else:
                self.ax.cla()
                self.effortlabel.config(text="Siediti… 🙈")
                self.window.update()
                self.effortlabel.config(text="Fatica! 🫠")
            self.draw()

        return

            

    def draw(self):
    
        # Compute PI
        Nriso = int(self.Nriso.get())
        x = np.random.random(Nriso)
        y = np.random.random(Nriso)
        self.pi=0
        for i in range(len(x)):
          if ( np.sqrt( (x[i]-0.5)**2+(y[i]-0.5)**2 )<0.5 ): self.pi+=1.0
        self.pi = self.pi/Nriso * 4
        self.pilabel.config(text="π = "+str(self.pi))
        self.piacclabel.config(text="Precisione: "+f"{100*(1-abs(self.pi-np.pi)/np.pi) :.5f}"+"%")

        # Reset Plot
        self.ax.cla()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_aspect('equal')
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="lightskyblue") )
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=0.5 ,color="tab:blue") )

        # Redraw plot (if feasible)
        if(Nriso>=50000):
            self.ax.text(0.1,0.5,"Troppi chicchi, immaginali!",fontdict=errorfont)
            self.plots.draw()
            return
        if(self.switch_variable.get()=="Riso" and Nriso<5000):
            self.ax.scatter(x,y,marker="")
            for xi, yi in zip(x,y):
                i =  np.random.randint(0,7)
                image=self.ims[i]
                im = OffsetImage(image, zoom=10/self.ax.figure.dpi)
                im.image.axes = self.ax
                ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
                self.ax.add_artist(ab)
        else:
            self.ax.scatter(x,y,marker=".",color="white")       
                        
        self.plots.draw()

        return


# Main
paths=[]
ims=[]
for i in range(1,8):
    path='riso'+f"{i}"+'.png'
    paths.append(path)
    ims.append(plt.imread(path))
window = Tk()
window.attributes("-fullscreen",True)
myGUI(window,ims)

def close_app():
   window.destroy()
   quit()
button_close = Button(window, text = "Exit", command = close_app)
button_close.place(x=100, y=50)
window.title('Calcoliamo PI-GRECO')
window.geometry("600x800+10+10")
window.mainloop()
