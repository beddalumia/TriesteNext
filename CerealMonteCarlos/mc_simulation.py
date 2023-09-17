import numpy as np

def init_simulation(N,L):
   occupancies = np.zeros((L,L),dtype=int)
   indices = np.zeros((N,2),dtype=int)
   if(N>L**2): raise ValueError("N > L×L")
   for i in range(N):
      ix=np.random.randint(0,L)
      iy=np.random.randint(0,L)
      while(occupancies[ix,iy]==1):
         ix=np.random.randint(0,L)
         iy=np.random.randint(0,L)   
      occupancies[ix,iy] = 1
      indices[i,:] = [ix,iy]
   return occupancies, indices

def metropolis(length,T,occupancies,indices,iNN,jNN):
   istep = 0
   Nstep = length
   Natom = np.sum(occupancies)
   Nsize = np.size(occupancies,0)
   beta  = 1/T
   for istep in range(Nstep):
      irand =np.random.randint(Natom)
      ixrand=np.random.randint(Nsize)
      iyrand=np.random.randint(Nsize)
      while(occupancies[ixrand,iyrand]==1):
         ixrand=np.random.randint(Nsize)
         iyrand=np.random.randint(Nsize)
      xy_vic=[ixrand,iyrand]
      e_old=0.0
      for j in range(6):
         xy_tmp = [iNN[indices[irand,0],indices[irand,1],j],jNN[indices[irand,0],indices[irand,1],j]]
         if(occupancies[xy_tmp[0],xy_tmp[1]]==1): e_old-=1.0
      e_new=0.0
      for j in range(6):
         xy_tmp = [iNN[xy_vic[0],xy_vic[1],j],jNN[xy_vic[0],xy_vic[1],j]]
         if(np.array(xy_tmp== indices[irand,:]).all ):continue #it would be empty
         if(occupancies[xy_tmp]==1): e_new-=1.0
      e_gain = e_old - e_new
      P = np.exp(e_gain*beta)
      R = np.random.rand()
      if(R<P):
         occupancies[xy_vic[0],xy_vic[1]]=1
         occupancies[indices[irand,0],indices[irand,1]]=0
         indices[irand,0] = xy_vic[0]
         indices[irand,1] = xy_vic[1]
   return occupancies, indices, e_gain
        
    
def total_energy(occupancies,indices,iNN,jNN):
   Ntot = np.sum(occupancies)
   Etot = 0.0
   for n in range(Ntot):
      ix=indices[n,0]; iy=indices[n,1]
      for ik in range(6):
         if(occupancies[iNN[ix,iy,ik],jNN[ix,iy,ik]]==1): Etot+=0.5
   return Etot

def build_lattice(L): 
   # init lattice coordinates
   Xij=np.zeros((L,L),dtype=np.float64)
   Yij=np.zeros((L,L),dtype=np.float64)
   # init neighbor indices
   iNN=np.zeros((L,L,6),dtype=int)
   jNN=np.zeros((L,L,6),dtype=int)
   # build everything
   for i in range(L):
      for j in range(L):
         # EVEN ROWS
         if( j%2==0):
               Xij[i,j] = i 
               Yij[i,j] = 0.5*j*np.sqrt(3.0)
               # neighbor #1
               if(i>0):
                  iNN[i,j,1]=i-1
                  jNN[i,j,1]=j
               else:
                  iNN[i,j,1]=L-1
                  jNN[i,j,1]=j
               # neighbor #2
               if(i<L-1):
                  iNN[i,j,2]=i+1
                  jNN[i,j,2]=j
               else:
                  iNN[i,j,2]=0
                  jNN[i,j,2]=j
               # neighbor #3
               if(i>0 and j<L-1):
                  iNN[i,j,3]=i-1
                  jNN[i,j,3]=j+1
               elif(i==0 and j<L-1):
                  iNN[i,j,3]=L-1
                  jNN[i,j,3]=j+1
               elif(i>0 and j==L-1):
                  iNN[i,j,3]=i-1
                  jNN[i,j,3]=0
               else:
                  iNN[i,j,3]=L-1
                  jNN[i,j,3]=0
               # neighbor #4
               if(j<L-1):
                  iNN[i,j,4]=i
                  jNN[i,j,4]=j+1
               else:
                  iNN[i,j,4]=i
                  jNN[i,j,4]=0
               # neighbor #5
               if(i>0 and j>0):
                  iNN[i,j,5]=i-1
                  jNN[i,j,5]=j-1
               elif(i==0 and j>0):
                  iNN[i,j,5]=L-1
                  jNN[i,j,5]=j-1
               elif(i>0 and j==0):
                  iNN[i,j,5]=i-1
                  jNN[i,j,5]=L-1
               else:
                  iNN[i,j,5]=L-1
                  jNN[i,j,5]=L-1
               # neighbor #6
               if(j>0):
                  iNN[i,j,0]=i
                  jNN[i,j,0]=j-1
               else:
                  iNN[i,j,0]=i
                  jNN[i,j,0]=L-1
         # ODD ROWS
         else:
               Xij[i,j] = i+0.5
               Yij[i,j] = 0.5*j*np.sqrt(3.0)
               # neighbor #1
               if(i>0):
                  iNN[i,j,1]=i-1
                  jNN[i,j,1]=j
               else:
                  iNN[i,j,1]=L-1
                  jNN[i,j,1]=j
               # neighbor #2
               if(i<L-1):
                  iNN[i,j,2]=i+1
                  jNN[i,j,2]=j
               else:
                  iNN[i,j,2]=0
                  jNN[i,j,2]=j
               # neighbor #3
               if(j<L-1):
                  iNN[i,j,3]=i
                  jNN[i,j,3]=j+1
               else:
                  iNN[i,j,3]=i
                  jNN[i,j,3]=0
               # neighbor #4
               if(i<L-1 and j<L-1):
                  iNN[i,j,4]=i+1
                  jNN[i,j,4]=j+1
               elif(i==L-1 and j<L-1):
                  iNN[i,j,4]=0
                  jNN[i,j,4]=j+1
               elif(i<L-1 and j==L-1):
                  iNN[i,j,4]=i+1
                  jNN[i,j,4]=0
               else:
                  iNN[i,j,4]=0
                  jNN[i,j,4]=0
               # neighbor #5
               if(j>0):
                  iNN[i,j,5]=i
                  jNN[i,j,5]=j-1
               else:
                  iNN[i,j,5]=i
                  jNN[i,j,5]=L-1
               # neighbor #6
               if(i<L-1 and j>0):
                  iNN[i,j,0]=i+1
                  jNN[i,j,0]=j-1
               elif(i==L-1 and j>0):
                  iNN[i,j,0]=0
                  jNN[i,j,0]=j-1
               elif(i<L-1 and j==0):
                  iNN[i,j,0]=i+1
                  jNN[i,j,0]=L-1
               else:
                  iNN[i,j,0]=0
                  jNN[i,j,0]=L-1  
   # return coordinates and neighbors 
   return Xij, Yij, iNN, jNN         