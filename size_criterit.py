import numpy as np
import matplotlib.pyplot as plt
import operator
import datetime
import os #to use environment eg path from profile
from classes import CPlife,COL
from six.moves import cPickle
from collections import OrderedDict
import matplotlib.pylab as pylab
params = {'legend.fontsize': '12',
          'figure.figsize': (5, 6),
         'axes.labelsize': '12',
         'axes.titlesize':'12',
         'xtick.labelsize':'12',
         'ytick.labelsize':'12'}
pylab.rcParams.update(params)

EXPID =  'lindp2K_500tr'#
odir = os.environ.get('results')


f = open(odir+'/coldpool/'+EXPID+'/output/cp/Size.save', 'rb')
CPsize = cPickle.load(f)
Arel = []
Arelshrink=[]
for k in CPsize.keys(): # loop trough all CPS
  maxA = 0
  for kk in CPsize[k].keys(): # loop trough all ages fpr this CP
   maxA = max(maxA,CPsize[k][kk])
   Achange = CPsize[k][kk]/maxA
   if Achange < 1: #only reduction in size
     Arel.append(Achange)

#fig, ax = plt.subplots([1,2])
fig, ax = plt.subplots(2)
fig2,ax0 = plt.subplots(1)

bins = np.linspace(0.6,1, 20)
n,x,_ = ax0.hist(Arel, bins, histtype='step',lw=3)
bin_centers = 0.5*(x[1:]+x[:-1])
nc=np.zeros(19)

print n
nc[0] = n[0]
for i in range(1,19):
   nc[i] = nc[i-1] +n[i]
print nc

nc=np.divide(nc,nc[18])
print nc
ax[0].plot(bin_centers,nc,label="",lw=2.5)

ax[0].set_ylabel('cumulative frequency')
#ax[0].set_xlabel('area fraction f')
ax[0].set_xticks([0.6,0.7,0.8,0.9])
f = open('/nbi/ac/conv1/henneb/results/coldpool/lindp2K_500tr_neu3/output/cp/termination.txt', 'r')
lines = f.readlines()
frac=[]
for line in lines:
  columns = line.split()
  frac.append((float(columns[2])))
bins = np.linspace(0.0,0.6, 20)
n,x,_ = ax0.hist(frac, bins, histtype='step',alpha=0.5,normed=1)
bin_centers = 0.5*(x[1:]+x[:-1])
ax[1].plot(bin_centers,n,label="",lw=2.5)
ax[1].set_ylabel('normalized frequency')
ax[1].set_xlabel('area fraction f')
ax[1].set_yticks([0,1,2,3,4])

ax[0].text(0.02, 0.98, 'a)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[0].transAxes)

ax[1].text(0.02, 0.98, 'b)',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[1].transAxes)


fig.savefig('plots/size_criteria.pdf')

plt.show()

     

