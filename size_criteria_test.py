import numpy as np
import matplotlib.pyplot as plt
import operator
import datetime
import os #to use environment eg path from profile
from classes import CPlife,COL
from six.moves import cPickle
from collections import OrderedDict
EXPID =  'lindp2K_100tr'#
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
   Arel.append(1-Achange)
   if Achange < 1:
    Arelshrink.append(1-Achange)
   if Achange < 0.6 :
    print k, kk, maxA, CPsize[k][kk] 
fig, ax = plt.subplots(1,figsize=(10,8))
fig2,ax0 = plt.subplots(1,figsize=(20,10))

bins = np.linspace(0,0.3, 20)
n,x,_ = ax0.hist(Arel, bins, histtype='step',alpha=0.5,normed=1)
bin_centers = 0.5*(x[1:]+x[:-1])
#ax.plot(bin_centers,n,label="")
n,x,_ = ax0.hist(Arelshrink, bins, histtype='step',alpha=0.5,normed=1, lw=2)
#ax.semilogy(bin_centers,n,label="")
ax.plot(bin_centers,n,label="")

ax.set_ylabel('normalized frequency')
ax.set_xlabel('cold pool area reduction')

fig.savefig('plots/size_criteria_test.pdf')

plt.show()

     

