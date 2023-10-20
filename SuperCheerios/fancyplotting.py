import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def draw_bowl_cartoon(ax,x,y,mask):
   ax.cla()
   ax.set_facecolor('lightskyblue')
   ax.scatter(x[mask==1],y[mask==1],c="None",s=350,marker="o",edgecolor="xkcd:maize",linewidth=9)
   ax.set_xlim([-0.5,20.0])
   ax.set_ylim([-0.5,17.0])
   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])

def draw_bowl_cheerios(ax,x,y,mask,cheerios):
   ax.cla()
   ax.set_facecolor('lightskyblue')
   ax.scatter(x[mask==1],y[mask==1],marker="")
   for xi, yi in zip(x[mask==1],y[mask==1]):
      i =  np.random.randint(0,6)
      image=cheerios[i]
      im = OffsetImage(image, zoom=27/ax.figure.dpi)
      im.image.axes = ax
      ab = AnnotationBbox(im, (xi,yi), frameon=False, pad=0.0,)
      ax.add_artist(ab)
   ax.set_xlim([-0.5,20.0])
   ax.set_ylim([-0.5,17.0])
   ax.set_aspect('equal')
   ax.set_xticks([])
   ax.set_yticks([])