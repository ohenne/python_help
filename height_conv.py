import numpy as np
import numpy.ma as ma
import os   # for environment 
import copy
import math
import matplotlib
import random
import operator
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime
from datetime import timedelta
from classes import RAINCLOUD, CP_map
#from classes import TRACER,CP_map,  CPstart, RAINCLOUD, CPlife
import scipy.stats as stats
from operator import itemgetter
from netCDF4 import Dataset
from six.moves import cPickle   # to save class files
dir = '/nbi/ac/conv1/henneb/results/coldpool/'
data_in    = Dataset(os.environ.get('modelo2')+'/UCLA_lind/p2K_large/lind_p2K_convergence.nc', 'r')


avg_con ={} #convergence con>0 average over whole odmain
avg_con_tr={} # convergence averaged over gridcell with tracers including divergence
colors = plt.cm.winter(np.linspace(0,1,12))
fig, ax = plt.subplots(1,3,figsize=(10,5),sharey=True)
timestart = datetime.datetime(2018,01,01,12)

# loop trough time
zt_in = np.array(data_in.variables['zt'])
print zt_in
for it in range(47,96,6):
  avg_con[it]={}
  avg_con_tr[it] = {}
  for li in range(1,6):

    con_in = np.array(data_in.variables["qconv_h_sfc"][it-1:it-1+6,:,:,li])

    avg_con[it][li] = np.ma.masked_where(con_in < 0.,con_in).mean() *1000.
    tr_mask =np.ones(con_in.shape,dtype=bool)
    if li == 1:
     EXPID ='lindp2K_500tr'
    else:
      EXPID ='lindp2K_500tr_lvl'+str(li)
    for i in range(0,6):
      inn=int(it+1+i)
      tracer_data_in = Dataset(dir+EXPID+'/output/cp/tracermask'+str(inn)+'.nc','r')
      tr_mask[i,:,:] = np.array(tracer_data_in.variables["data"])
    con_in_mask = con_in.ravel()[tr_mask.ravel()]
    avg_con_tr[it][li] = np.mean(con_in_mask)*1000.
#  ax[0].plot(avg_con_tr[it].values(),zt_in[0:9],color=colors[((it-47)/6)+1],label=timestart.strftime("%H:%M"))
#  ax[1].plot(avg_con[it].values(),zt_in[0:9],color=colors[((it-47)/6)+1])
  ax[1].plot(avg_con_tr[it].values(),avg_con_tr[it].keys(),color=colors[((it-47)/6)+1],label=timestart.strftime("%H:%M"))
  ax[0].plot(avg_con[it].values(),avg_con[it].keys(),color=colors[((it-47)/6)+1],label=timestart.strftime("%H:%M"))
  timestart=timestart+timedelta(minutes=30)
ax[0].set_xlabel('convergence / g kg$\mathregular{^{-1}}$ s$\mathregular{^{-1}}$')
ax[1].set_xlabel('convergence / g kg$\mathregular{^{-1}}$ s$\mathregular{^{-1}}$')
ax[0].set_ylabel('model level') #height / m$')
ax[0].text(0.02, 0.98, 'a)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[0].transAxes)
ax[1].text(0.02, 0.98, 'b)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[1].transAxes)

ax[0].legend()

# SIZE
EXPID ='lindp2K_500tr' #'lindp2K_500tr'


f = open(dir+EXPID+'/output/cp/Size.save', 'rb')
refsize = cPickle.load(f)
f.close()

size_lvl = {}
for i in range(2,6):
  print 'lindp2K_500tr_lvl'+str(i)
  EXPID ='lindp2K_500tr_lvl'+str(i)
  f = open(dir+EXPID+'/output/cp/Size.save', 'rb')
  cur_size = cPickle.load(f)
  f.close()
  size_list = []
  for x in cur_size.keys():
   if x in refsize.keys():
    for y in cur_size[x].keys():
     if y in refsize[x].keys():
      size_list.append(cur_size[x][y]/refsize[x][y])

   size_lvl[i] = np.average(size_list) 
size_lvl[1] = 1
#ax[2].plot(size_lvl.values(),zt_in[0:9])
ax[2].plot(size_lvl.values(),size_lvl.keys())
ax[2].set_xlabel('normalized CP size')
ax[2].text(0.02, 0.98, 'c)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[2].transAxes)


fig.savefig('convergence_height.pdf')
plt.show()

