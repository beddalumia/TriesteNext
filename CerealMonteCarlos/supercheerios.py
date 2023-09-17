from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
# local modules
from mc_simulation import *
from fancyplotting import *

BowlSize=20 # Hard coded for ever (we don't want to scale the cereal size!)

class myGUI:
    def __init__(self, win, cheerios):
        self.window=win
        x0, y0 = 80, 250
        #---- Input labels, entries and data -------
        self.numpops = Label(win, text='Numero di cereali')
        self.numpops.config(font=('Arial', 22))
        self.numpops.place(x=x0, y=y0)
        self.Nflakes = Entry()
        self.Nflakes.place(x=x0, y=y0+50)
        self.Nflakes.insert(END, str(0))
        self.kinlabl = Label(win, text='Quanto agitiamo?')
        self.kinlabl.config(font=('Arial', 22))
        self.kinlabl.place(x=x0, y=y0+100)
        self.kinesis = Scale(win,from_=1,to=100,orient=HORIZONTAL)
        self.kinesis.place(x=x0,y=y0+130)
        self.cheerios = cheerios # png images
        #---- Parameter independent initialization -------
        self.occupancies = np.array([])
        self.indices = np.array([])
        self.x,self.y,self.i,self.j = build_lattice(BowlSize)
        self.Nflakes_old = 0
        self.initialized = False
        # Compute button
        self.btn1 = Button(win, text='Calcola')
        self.btn1.bind('<Button-1>', self.run)
        self.btn1.place(x=x0, y=y0 + 200)

        # Matplotlib window
        self.figure, self.ax = plt.subplots(figsize=(10, 10), dpi=100)

        # Configure axes
        self.ax.set_facecolor('lightskyblue')
        self.ax.scatter(self.x,self.y,marker=".",color="lightskyblue")
        # > auto-defines xlim and ylim
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_aspect('equal')

        # Show the matplotlib stuff 
        self.plots = FigureCanvasTkAgg(self.figure, win)
        self.plots.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=0)

        # Switch for rice or scatterplot (also lentils?)
        self.switch_frame = Frame(win)
        self.switch_frame.place(x=x0,y=120)
        self.switch_variable = StringVar(value="heavy")
        self.riso_button = Radiobutton(self.switch_frame, text="Super GPU", variable=self.switch_variable,
                                       indicatoron=False, value="heavy", width=8)
        self.punti_button = Radiobutton(self.switch_frame, text="Potato PC", variable=self.switch_variable,
                                        indicatoron=False, value="easy", width=8)
        self.riso_button.pack(side="left")
        self.punti_button.pack(side="right")

            
    # Draw the dice & draw the figure 
    def run(self,event):
         # Get all the input parameters
         Nflakes = int(self.Nflakes.get())
         Nsteps=1  # Hard coded for now (ever?)
         T=self.kinesis.get(); T = 0.1*T # Actual working scale
         print("T = "+str(T))
         # Retrieve the (pre-built) lattice coordinates and NN-list
         X, Y, iNN, jNN = self.x, self.y, self.i, self.j
         if self.Nflakes_old != Nflakes:
             # Discard initialization
             self.initialized = False
         if not(self.initialized):
            # Draw an initial configuration of cereals in the lattice
            occupancies, indices = init_simulation(Nflakes,BowlSize)
            # Thermalize the Markov chain (100 steps)
            occupancies, indices, e_gain = metropolis(100,T,occupancies,indices,iNN,jNN)
         else:
            # Or retrieve the stored state of the system, if any
            occupancies = self.occupancies
            indices = self.indices
         # Compute the total energy (no need for visualization)
         # > E_tot = total_energy(occupancies,indices,iNN,jNN)
         # Run the Markov chain for N steps
         while True:
            occupancies, indices, e_gain = metropolis(Nsteps,T,occupancies,indices,iNN,jNN)
            # Update the total energy (no need for visualization)
            # > E_tot += e_gain
            # Store the state of the system (for smart restart)
            self.occupancies = occupancies
            self.indices = indices
            self.Nflakes_old = Nflakes
            self.initialized = True
            # Draw latest Metropolis configuration 
            if(self.switch_variable.get()=="heavy"):
                  draw_bowl_cheerios(self.ax,X,Y,occupancies,self.cheerios)
            else:
                  draw_bowl_cartoon(self.ax,X,Y,occupancies)      
            # Refresh matplotlib window          
            self.plots.draw()
            self.window.update()


# Read the pictures
paths=[]
cheerios=[]
for i in range(1,7):
    path='C'+f"{i}"+'.png'
    paths.append(path)
    cheerios.append(plt.imread(path))

# Init the Tkinter window
window = Tk()
window.attributes("-fullscreen",True)
myGUI(window,cheerios)

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
