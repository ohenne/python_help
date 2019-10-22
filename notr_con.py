import numpy as np
import numpy.ma as ma
import os   # for environment 
import copy
import math
import matplotlib
import random
import operator
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
#import seaborn as sns
import datetime
from datetime import timedelta
from classes import RAINCLOUD, CP_map
#from classes import TRACER,CP_map,  CPstart, RAINCLOUD, CPlife
import scipy.stats as stats
from operator import itemgetter
from netCDF4 import Dataset
from six.moves import cPickle   # to save class files
#################################
# SET UP
#################################
#import matplotlib.colors as mcolors
#EXPID ='lindp2K_100tr' #'test1plus4K' #'lind_p2K' #'test1plus4K'# 'lindp2K'#
#end = 150
#left,bottom, width, height= [0.6,0.3,0.36,0.39] # left bottom with height
#dtick =20
#ni = 10


EXPID ='lindp2K_500tr' #'test1plus4K' #'lind_p2K' #'test1plus4K'# 'lindp2K'#

data_in= Dataset('/nbi/ac/cond3/rawdata/UCLA_lind/lind_p2K/lind_p2K_budget.nc', 'r')

#EXPID ='lindp2K_13' #'test1plus4K' #'lind_p2K' #'test1plus4K'# 'lindp2K'#
#end = 640

dir = '/nbi/ac/conv1/henneb/results/coldpool/'
#colors = mcolors.tab20c
#colors = plt.cm.tab20c #(np.linspace(0,1,len(trange[:-2])))
ztime = datetime.datetime.now()
###############################################
# OPEN DATA
################################################
f = open(dir+EXPID+'/output/cp/TracerMap.save', 'rb')
CPmap = cPickle.load(f)
f.close()
atime = datetime.datetime.now()
print 'took ',(atime-ztime), 'to read data MAP'
data1 =[]
data2 = []
data6 = []
data11 = []
data51 = []
data101 = []
tist = 0
w_all=[]
for (t,x,y) in sorted(CPmap.keys(),key=itemgetter(0)): # data2[0:10]: #CPmap.keys()[0:10]:
  if t > tist:
    tist = t
    con_in = np.array(data_in.variables["conv_h_sfc"][t-1,:,:])
  w = con_in[y%1024,x%1024]
  if CPmap[(t,x,y)].nTrtot == 1:
    data1.append(w)
  elif CPmap[(t,x,y)].nTrtot > 1 and CPmap[(t,x,y)].nTrtot < 6:
    data2.append(w)
  elif CPmap[(t,x,y)].nTrtot > 5 and CPmap[(t,x,y)].nTrtot < 11:
    data6.append(w)
  elif CPmap[(t,x,y)].nTrtot > 10 and CPmap[(t,x,y)].nTrtot < 51:
    data11.append(w)
  elif CPmap[(t,x,y)].nTrtot > 51 and CPmap[(t,x,y)].nTrtot < 101:
    data51.append(w)
  elif CPmap[(t,x,y)].nTrtot > 100 :
    data101.append(w)

fig, ax = plt.subplots(1)
fig2,ax2 = plt.subplots(1,figsize=(8,4))

bins = np.linspace(-0.02, 0.02, 50)
n,x,_ = ax.hist(data1, bins, histtype='step',alpha=0.5,normed=1,label='1', color='orange')
bin_centers = 0.5*(x[1:]+x[:-1])
ax2.plot(bin_centers,n,label='1',color='darkorange',linewidth=2.2)

n,x,_ = ax.hist(data2, bins, histtype='step',alpha=0.5,normed=1,label='1', color='orange')
bin_centers = 0.5*(x[1:]+x[:-1])
ax2.plot(bin_centers,n,label='2-5',color='royalblue',linewidth=2.2)

n,x,_ = ax.hist(data6, bins, histtype='step',alpha=0.5,normed=1,label='1', color='orange')
bin_centers = 0.5*(x[1:]+x[:-1])
ax2.plot(bin_centers,n,label='6-10',color='seagreen',linewidth=2.2)

n,x,_ = ax.hist(data11, bins, histtype='step',alpha=0.5,normed=1,label='1', color='orange')
bin_centers = 0.5*(x[1:]+x[:-1])
ax2.plot(bin_centers,n,label='11-50',color='dimgrey',linewidth=2.2)

n,x,_ = ax.hist(data51, bins, histtype='step',alpha=0.5,normed=1)
bin_centers = 0.5*(x[1:]+x[:-1])
ax2.plot(bin_centers,n,label='51-100',color='mediumslateblue',linewidth=2.2)

n,x,_ = ax.hist(data101, bins, histtype='step',alpha=0.5,normed=1)
bin_centers = 0.5*(x[1:]+x[:-1])
ax2.plot(bin_centers,n,label='>100',color='red',linewidth=2.2)

#n,x,_ = ax.hist(w_all, bins, histtype='step',alpha=0.5,normed=1)
#bin_centers = 0.5*(x[1:]+x[:-1])
#ax2.plot(bin_centers,n,label='con',color='c',linewidth=2.2)

mean00 = np.mean(data1)
ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='darkorange')
mean00 = np.mean(data2)
ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='royalblue')
mean00 = np.mean(data6)
ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='seagreen')
mean00 = np.mean(data11)
ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='dimgrey')
mean00 = np.mean(data51)
ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='mediumslateblue')
mean00 = np.mean(data101)
ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='red')
#mean00 = np.mean(data)
#ax2.plot([mean00,mean00], [0, 0.05], 'k-', lw=2,color='c')


ax2.set_xlabel('horizontal convergence / m s$\mathregular{^{-1}}$')
ax2.set_ylabel('normalized frequency / m$\mathregular{^{-1}}$ s')

ax2.legend(title="# tracers in grid cell")

fig2.savefig('pdf_convergence_notracer_20level.pdf')
plt.show()




  



 
