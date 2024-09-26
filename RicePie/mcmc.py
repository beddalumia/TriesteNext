from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

plot_font = {'family': 'Arial',
            'color':  'white',
            'weight': 'bold',
            'size': 32
            }

class myGUI:
    def __init__(self, win, ims):
        self.window=win
        x0, y0 = 80, 250
        #---- Grains label and entry -------
        self.lbl0 = Label(win, text='Numero di chicchi')
        self.lbl0.config(font=('Arial', 22))
        self.lbl0.place(x=x0, y=y0)
        self.Nriso = Entry()
        self.Nriso.place(x=x0, y=y0+50)
        self.Nriso.insert(END, str(0))
        self.t_0 = float(self.Nriso.get())
        self.ims = ims
        self.lbl0 = Label(win, text='Parametro di salto d')
        self.lbl0.config(font=('Arial', 22))
        self.lbl0.place(x=x0, y=y0+100)
        self.delta = Entry()
        self.delta.place(x=x0, y=y0+150)
        self.Nriso.insert(END, str(0))
        # Count labels
        self.inlabel  = Label(win, text="Dentro: ")
        self.outlabel = Label(win, text="Fuori: ")
        self.inlabel.config(font=('Arial',22))
        self.outlabel.config(font=('Arial',22))
        self.inlabel.place(x=x0, y=y0+250)
        self.outlabel.place(x=x0, y=y0+300)
        # PI label
        self.pi = 0.0
        self.pilabel = Label(win, text="p =")
        self.pilabel.config(font=('LatinModern', 32))
        self.pilabel.place(x=x0, y=y0+400)
        # Accuracy label
        self.piacclabel = Label(win,text="Precisione: ")
        self.piacclabel.config(font=('Arial',22))
        self.piacclabel.place(x=x0,y=y0+450)
        ## Acceptance label
        self.accept_ratiolabel = Label(win,text="Accettazione: ")
        self.accept_ratiolabel.config(font=('Arial',22))
        self.accept_ratiolabel.place(x=x0,y=y0+500)
        # Computational Effort Label
        self.effortlabel = Label(win,text="??")
        self.effortlabel.config(font=("Arial",60))
        self.effortlabel.place(x=x0, y=y0+600)
        # add a label here for acceptance ratio
        # add an input for the delta jump
        
        # Compute button
        self.btn1 = Button(win, text='Calcola')
        self.btn1.bind('<Button-1>', self.update)
        self.btn1.place(x=x0, y=y0 + 200)

        # Matplotlib window
        self.figure, self.ax = plt.subplots(figsize=(10, 10), dpi=100)

        # Configure axes
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_aspect('equal')
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="lightskyblue") )
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=0.5 ,color="tab:blue") )

        # Show the matplotlib stuff 
        self.plots = FigureCanvasTkAgg(self.figure, win)
        self.plots.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=0)

        # Switch for rice or scatterplot (also lentils?)
        self.switch_frame = Frame(win)
        self.switch_frame.place(x=x0,y=120)
        self.switch_variable = StringVar(value="Riso")
        self.riso_button = Radiobutton(self.switch_frame, text="Riso", variable=self.switch_variable,
                                       indicatoron=False, value="Riso", width=8)
        self.punti_button = Radiobutton(self.switch_frame, text="Punti", variable=self.switch_variable,
                                        indicatoron=False, value="Punti", width=8)
        self.riso_button.pack(side="left")
        self.punti_button.pack(side="right")

    # Button behavior
    def update(self,event):
        Nriso = int(self.Nriso.get())
        #ERROR IF TOO MANY/FEW GRAINS
        if(Nriso>10**6):
            self.ax.cla()
            self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="xkcd:red") )
            self.ax.text(0.2,0.5,"TROPPO DIFFICILE",fontdict=plot_font)
            self.inlabel.config(text="Dentro: ?")
            self.outlabel.config(text="Fuori: ?")
            self.pilabel.config(text="π = ?")
            self.piacclabel.config(text="Precisione: ?")
            self.effortlabel.config(text="💀")
            self.plots.draw()
        elif(Nriso<=0):
            self.inlabel.config(text="Dentro: ?")
            self.outlabel.config(text="Fuori: ?")
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

            
    # Draw the dice & draw the figure 
    def draw(self):
        # Compute PI
        Nriso = int(self.Nriso.get())
        delta = float(self.delta.get()) # add input

        x = []
        y = []
        x0 = np.random.random()
        y0 = np.random.random()
        x.append(x0)
        y.append(y0)
        count = 0
        accept = 0
        for i in range(Nriso):
            del_x, del_y = np.random.uniform(-delta, delta), np.random.uniform(-delta, delta)
            if x0 + del_x < 1.0 and x0 + del_x > 0.0 and y0 + del_y < 1.0 and y0 + del_y > 0.0:
                x0, y0 = x0 + del_x, y0 + del_y
                accept+=1.0
            if x0**2 + y0**2 < 1.0:
                count+=1.0
            x.append(x0)
            y.append(y0)

        self.pi = count/Nriso * 4
        self.accept_ratio =  accept/Nriso # add definition for output
        self.inlabel.config(text="Dentro: "+str(int(count)))
        self.outlabel.config(text="Fuori: "+str(int(Nriso-count)))
        self.pilabel.config(text="p = "+f"{self.pi:.5f}")
        self.piacclabel.config(text="Precisione: "+f"{100*(1-abs(self.pi-np.pi)/np.pi):.2f}"+"%")
        self.accept_ratiolabel.config(text="Accettazione: "+f"{self.accept_ratio:.5f}")
        # Reset Plot
        self.ax.cla()
        self.ax.set_xlim(0,1)
        self.ax.set_ylim(0,1)
        self.ax.set_aspect('equal')
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="lightskyblue") )
        self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=0.5 ,color="tab:blue") )
        # Redraw plot (if feasible)
        if(Nriso>=50000):
            self.ax.text(0.1,0.5,"Troppi chicchi, immaginali!",fontdict=plot_font)
            self.plots.draw()
            return
        if(self.switch_variable.get()=="Riso" and Nriso<2500):
            self.ax.plot(x,y,'-',color="#b2182b",alpha=0.5)
            self.ax.scatter(x,y,marker="")
            for xi, yi in zip(x,y):
                i =  np.random.randint(0,7)
                image=self.ims[i]
                im = OffsetImage(image, zoom=10/self.ax.figure.dpi)
                im.image.axes = self.ax
                ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
                self.ax.add_artist(ab)
        else:
            self.ax.plot(x,y,'-',color="#b2182b",alpha=0.5)
            self.ax.scatter(x,y,marker=".",color="white")       
        # Refresh matplotlib window          
        self.plots.draw()
        return


# Read the pictures
paths=[]
ims=[]
for i in range(1,8):
    path='riso'+f"{i}"+'.png'
    paths.append(path)
    ims.append(plt.imread(path))

# Init the Tkinter window
window = Tk()
window.attributes("-fullscreen",True)
myGUI(window,ims)

# Exit the GUI and the python shell
def close_app():
   window.destroy()
   quit()
button_close = Button(window, text = "Exit", command = close_app)
button_close.place(x=80, y=50)

# Configure the global window
window.title('Calcoliamo PI-GRECO')
window.geometry("600x800+10+10")
window.mainloop()
