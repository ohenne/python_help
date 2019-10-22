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
import matplotlib.pylab as pylab
params = {'legend.fontsize': '10',
          'figure.figsize': (5,5),
         'axes.labelsize': '12',
         'axes.titlesize':'12',
         'xtick.labelsize':'12',
         'ytick.labelsize':'12'}
pylab.rcParams.update(params)

dir = '/nbi/ac/conv1/henneb/results/coldpool/'
data_in    = Dataset(os.environ.get('modelo2')+'/UCLA_lind/p2K_large/lind_p2K_convergence.nc', 'r')
data_in_u  = Dataset(os.environ.get('modelo2')+'/UCLA_lind/p2K_large/lind_p2K.out.vol.u.nc', 'r')
data_in_v  = Dataset(os.environ.get('modelo2')+'/UCLA_lind/p2K_large/lind_p2K.out.vol.v.nc', 'r')


avg_FF_tr ={} #convergence con>0 average over whole odmain
avg_con_tr={} # convergence averaged over gridcell with tracers including divergence
colors = plt.cm.winter(np.linspace(0,1,12))
fig, ax = plt.subplots(1,3,sharey=True)
timestart = datetime.datetime(2018,01,01,12)
heights = [50,150,250,350,450]

# loop trough time
zt_in = np.array(data_in.variables['zt'])
print zt_in
for li in range(1,6):

    con_in = np.array(data_in.variables["qconv_h_sfc"][47:90,:,:,li])
    u_in = np.array(data_in_u.variables["u"][47:90,:,:,li])
    v_in = np.array(data_in_v.variables["v"][47:90,:,:,li])
    FF_in = np.sqrt(np.add(np.square(u_in),np.square(v_in)))
    tr_mask =np.ones(con_in.shape,dtype=bool)
    if li == 1:
     EXPID ='lindp2K_500tr'
    else:
      EXPID ='lindp2K_500tr_lvl'+str(li)
    for i in range(0,43):
      inn=int(47+1+i)
      print inn
      tracer_data_in = Dataset(dir+EXPID+'/output/cp/tracermask'+str(inn)+'.nc','r')
      tr_mask[i,:,:] = np.array(tracer_data_in.variables["data"])
    con_in_mask = con_in.ravel()[tr_mask.ravel()]
    FF_in_mask = FF_in.ravel()[tr_mask.ravel()]
    avg_con_tr[li] = np.mean(con_in_mask)*1000.
    avg_FF_tr[li] = np.mean(FF_in_mask)

#ax[1].plot(avg_con_tr.values(),avg_con_tr.keys(),marker="o")
ax[1].plot(avg_con_tr.values(),heights,marker="o")
#ax[2].plot( avg_FF_tr.values(), avg_FF_tr.keys(),marker="o")
ax[2].plot( avg_FF_tr.values(), heights,marker="o")

ax[2].set_xlabel('FF / m s$\mathregular{^{-1}}$')
ax[1].set_xlabel('conv. / g kg$\mathregular{^{-1}}$ s$\mathregular{^{-1}}$')
#ax[2].set_ylabel('model level') #height / m$')
#ax[2].set_ylabel('model level') #height / m$')

ax[1].set_xticks([0,1])
ax[2].set_xticks([0.5,1.5,2.5])


ax[2].text(0.02, 0.98, 'a)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[0].transAxes)
ax[1].text(0.02, 0.98, 'b)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[1].transAxes)

ax[2].legend()

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

#ax[0].plot(size_lvl.values(),size_lvl.keys(),marker="o")
ax[0].plot(size_lvl.values(),heights,marker="o")
ax[0].set_xlabel('norm. radius')
ax[2].text(0.02, 0.98, 'c)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[2].transAxes)
ax[0].set_ylabel('height / m')
ax[0].set_yticks(heights)
ax[0].set_xticks([0.5,1.0])


fig.savefig('plots/convergence_height_single.pdf')
#plt.show()

