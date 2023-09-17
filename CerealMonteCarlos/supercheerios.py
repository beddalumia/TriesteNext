from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from mc_simulation import *
from fancyplotting import *

plot_font = {'family': 'Arial',
            'color':  'white',
            'weight': 'bold',
            'size': 32
            }

class myGUI:
    def __init__(self, win, ims):
        self.window=win
        x0, y0 = 80, 250
        #---- Input labels and entries -------
        self.lbl0 = Label(win, text='Numero di cereali')
        self.lbl0.config(font=('Arial', 22))
        self.lbl0.place(x=x0, y=y0)
        self.Nflakes = Entry()
        self.Nflakes.place(x=x0, y=y0+50)
        self.Nflakes.insert(END, str(0))
        self.t_0 = float(self.Nflakes.get())
        self.ims = ims
        # Count labels
        self.inlabel  = Label(win, text="Dentro: ")
        self.outlabel = Label(win, text="Fuori: ")
        self.inlabel.config(font=('Arial',22))
        self.outlabel.config(font=('Arial',22))
        self.inlabel.place(x=x0, y=y0+200)
        self.outlabel.place(x=x0, y=y0+250)
        # PI label
        self.pi = 0.0
        self.pilabel = Label(win, text="π =")
        self.pilabel.config(font=('LatinModern', 32))
        self.pilabel.place(x=x0, y=y0+350)
        # Accuracy label
        self.piacclabel = Label(win,text="Precisione: ")
        self.piacclabel.config(font=('Arial',22))
        self.piacclabel.place(x=x0,y=y0+400)
        # Computational Effort Label
        self.effortlabel = Label(win,text="👀")
        self.effortlabel.config(font=("Arial",60))
        self.effortlabel.place(x=x0, y=y0+500)
        
        # Compute button
        self.btn1 = Button(win, text='Calcola')
        self.btn1.bind('<Button-1>', self.update)
        self.btn1.place(x=x0, y=y0 + 100)

        # Matplotlib window
        self.figure, self.ax = plt.subplots(figsize=(10, 10), dpi=100)

        # Configure axes
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('lightskyblue')

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
        Nflakes = int(self.Nflakes.get())
        #ERROR IF TOO MANY/FEW GRAINS
        if(Nflakes>10**6):
            self.ax.cla()
            self.ax.add_patch( matplotlib.patches.Circle((0.5,0.5),radius=2   ,color="xkcd:red") )
            self.ax.text(0.2,0.5,"TROPPO DIFFICILE",fontdict=plot_font)
            self.inlabel.config(text="Dentro: ?")
            self.outlabel.config(text="Fuori: ?")
            self.pilabel.config(text="π = ?")
            self.piacclabel.config(text="Precisione: ?")
            self.effortlabel.config(text="💀")
            self.plots.draw()
        elif(Nflakes<=0):
            self.inlabel.config(text="Dentro: ?")
            self.outlabel.config(text="Fuori: ?")
            self.pilabel.config(text="π = ?")
            self.piacclabel.config(text="Precisione: ?")
            self.effortlabel.config(text="Maddai! 🤡")
        else:
            if(Nflakes<100):
                self.effortlabel.config(text="Facile! 🙃")
            elif(Nflakes<1000):
                self.ax.cla()
                self.effortlabel.config(text="⏳...")
                self.window.update()
                self.effortlabel.config(text="Oook! 🥲")
            else:
                self.ax.cla()
                self.effortlabel.config(text="Siediti… 🙈")
                self.window.update()
                self.effortlabel.config(text="Fatica! 🫠")
            self.run()
        return

            
    # Draw the dice & draw the figure 
    def run(self):
        # Run the Metropolis simulation
        BowlSize=20 # Hard coded for now (ever?)
        X, Y, iNN, jNN = build_lattice(BowlSize)
        Nflakes = int(self.Nflakes.get())
        occupancies, indices = init_simulation(Nflakes,BowlSize)
        E_tot = total_energy(occupancies,indices,iNN,jNN)
        Nsteps=100  # Hard coded for now (ever?)
        T=0.1       # Hard coded for now (ever?)
        occupancies, indices, e_gain = metropolis(Nsteps,T,occupancies,indices,iNN,jNN)
        E_tot += e_gain
        # Redraw plot (if feasible)
        if(Nflakes>=50000):
            self.ax.text(0.1,0.5,"Troppi chicchi, immaginali!",fontdict=plot_font)
            self.plots.draw()
            return
        if(self.switch_variable.get()=="Riso" and Nflakes<2500):
            draw_bowl_cheerios(self.ax,X,Y,occupancies,self.ims)
        else:
            draw_bowl_cartoon(self.ax,X,Y,occupancies)      
        # Refresh matplotlib window          
        self.plots.draw()
        return


# Read the pictures
paths=[]
ims=[]
for i in range(1,7):
    path='C'+f"{i}"+'.png'
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
window.title('SuperCheerios')
window.geometry("600x800+10+10")
window.mainloop()
