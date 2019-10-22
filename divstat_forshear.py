import numpy as np
import numpy.ma as ma
import os   # for environment 
import math
import matplotlib
import operator
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter
from netCDF4 import Dataset
from six.moves import cPickle   # to save class files

atime = datetime.datetime.now()
###############################################################
# SETTINGS
# ###############################################################
#DIR = '/nbi/ac/conv1/henneb/results/'
DIR = '/nbi/ac/conv1/henneb/results/coldpool/'

#sim ='lindp2KdivUCP'
sim = 'lind_adv_500tr'

f = open(DIR+sim+'/output/raincell/headerfile.txt', 'r')
lines = f.readlines()
IDs={}
for line in lines:
  columns = line.split()
  ID = (int(columns[0]))
  starting = (int(columns[3]))
  if starting == 0:
   IDs[ID] =1
  
f = open(DIR+sim+'/output/raincell/irt_tracks_output_pure.txt', 'r')
lines = f.readlines()
IDlast = 0
con={} # list of converging cells at age(key)
div={} # list of diverging cells at age(key)
divage={} 
uv={}
for  i in range(1,8):
  con[i] = []
  div[i] = []
  uv[i] = []

for line in lines:
  columns = line.split()
  IDist = (int(columns[0]))    # timestep
  conin = (float(columns[6]))
  u = abs((float(columns[7])))
  v = abs((float(columns[8])))
  uvist = u+v
  if IDist == 257:
    print conin , 'conin for 257'
  if IDist in IDs.keys():
    if IDist > IDlast:
      age=1
      IDlast = IDist
    if age < 8:
     if conin > 0:
       con[age].append(conin) 
     elif conin< 0:
       div[age].append(conin)  
     uv[age].append(uvist)
     if conin<  -0.0025: #-0.001:
      if not IDist in divage.keys():
        divage[IDist] = age
    age= age+1


print  IDist 
fig, ax = plt.subplots(2)  # make some smart devision accoridng to number of varaibles

#ax[0].plot(con.keys(),len(con.values()), linewidth=3.0)

conl = {}
divl={}
conm= {}
divm={}
uvm={}
tot={} # total number of cells with age(key)

for k in range(1,8) : 
  conl[k] = len(con[k])
  conm[k] = np.mean(con[k])
  divl[k] = len(div[k])
  tot[k] = conl[k]+divl[k]
  divm[k] = np.mean(div[k]) *(-1)
  uvm[k] = np.mean(uv[k])

  conl[k] = np.divide(float(conl[k]),float(tot[k]))
  divl[k] = np.divide(float(divl[k]),float(tot[k]))

agediv = {}  
for k in range(min(divage.values()),max(divage.values())+1):
  agediv[k] = 0

for k in IDs.keys(): #divage.keys() : #range(min(divage.values()),max(divage.values())+1):
  if k in divage.keys() :
     agediv[divage[k]] = agediv[divage[k]]+ 1
  else:
     print k , 'not in '
print max(divage.values())
agedivcum={}
totcum = {}
agedivcum[min(divage.values())] = agediv[min(divage.values())]
totcum[min(divage.values())] =tot[min(divage.values())]
print 'min',min(divage.values())
for k in range(min(divage.values())+1,max(divage.values())+1):
  print 'k', k
  agedivcum[k] = agedivcum[k-1]+agediv[k]
#  totcum[k] = tot[k-1]+tot[k]

print 'totcum', totcum, tot 
for k in agedivcum.keys():
  print k
  print agedivcum[k]
  agedivcum[k] = float(agedivcum[k])/float(tot[1])
  print 'final', agedivcum[k]
ax[0].plot(con.keys(),conl.values(), linewidth=3.0,label='D < 0',color='darkorange')
ax[0].plot(con.keys(),divl.values(), linewidth=3.0,label='D > 0',color='royalblue')

ax[0].plot(agedivcum.keys(),agedivcum.values(), linewidth=3.0,label='D > 2.5 g $\mathregular{m^{-2}}$ $\mathregular{s^{-1}}$',color='seagreen')

ax[1].plot(con.keys(),np.multiply(conm.values(),1000), linewidth=3.0,label='D < 0',color='darkorange')
ax[1].plot(con.keys(),np.multiply(divm.values(),1000), linewidth=3.0,label='D > 0',color='royalblue')
#ax[1].plot(con.keys(),uvm.values(), linewidth=3.0,label='uv')

#print len(IDs.keys())
#print max(divage.keys()), max(agedivcum.values())
#print divage[257] 
#print uvm.values()
#ax[0].set_xlabel('duration of precipitation track in time steps')
ax[1].set_xlabel('duration of precipitation track in time steps')
ax[1].set_ylabel('|D| / g $\mathregular{m^{-2}}$ $\mathregular{s^{-1}}$')
ax[0].set_ylabel('fraction of cells')
ax[0].legend()
ax[1].legend()
ax[0].set_xticks([])
# make labeling
left = 0.02 #, width = .05, .5
bottom = 0.02 #, height = .45, .0
right = 0.98 #left + width
top = 0.98 # bottom + height

ax[0].text(left, top, 'c',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[0].transAxes,
        fontsize=20)
ax[1].text(left, top, 'd',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[1].transAxes,
        fontsize=20)
for i in [0,1]:
 for item in ([ax[i].title, ax[i].xaxis.label, ax[i].yaxis.label] +
             ax[i].get_xticklabels() + ax[i].get_yticklabels()):
    item.set_fontsize(15)

#fig.savefig('plots/conv_div_lindp2K.pdf')
fig.savefig('plots/conv_div_adv.pdf')

plt.show() 


