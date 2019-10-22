import numpy as np
import numpy.ma as ma
import os   # for environment 
import math
import matplotlib
import operator
import matplotlib.pyplot as plt
import datetime
from classes import TRACER,CP_map   
from operator import itemgetter 
from netCDF4 import Dataset   
from six.moves import cPickle   # to save class files
##import matplotlib.pylab as pylab
##params = {'legend.fontsize': '8',
##          'figure.figsize': (5, 4),
##         'axes.labelsize': '10',
##         'axes.titlesize':'10',
##         'xtick.labelsize':'10',
##         'ytick.labelsize':'10'}
##pylab.rcParams.update(params)

EXPID ='lindp2K_13' #neworder' #''test1plus4K_is'
atime =datetime.datetime.now()
# SETTINGS
dir = '/nbi/ac/conv1/henneb/results/coldpool/'
simstart =  datetime.datetime(2018,1,1,8,5)
###############################################################
# SAVE DATA
############################################################

f = open(dir+EXPID+'/output/cp/Tracer.save', 'rb')
CoPo = cPickle.load(f)
f.close()
btime =datetime.datetime.now()
print 'took ',(btime-atime), 'to read data'

radvel={}
spreadvel={}
FFvel={}
FFvel2={}

avg_radvel={}
avg_spreadvel={}
avg_FFvel={}
avg_FFvel2={}

i = 0
print 'start loop'
for k in CoPo.keys():
 for t in sorted(CoPo[k].CP.keys()):

  if not CoPo[k].age[t] in radvel.keys():
    radvel[CoPo[k].age[t]] = []
    spreadvel[CoPo[k].age[t]] = []
    FFvel[CoPo[k].age[t]] = []
    FFvel2[CoPo[k].age[t]] = []

  radvel[CoPo[k].age[t]].append(CoPo[k].vr[t])
  FFvel[CoPo[k].age[t]].append(CoPo[k].FF[t])
  FFvel2[CoPo[k].age[t]].append(abs(CoPo[k].vt[t])) #**2.+CoPo[k].v[t]**2)**0.5)

  if t+1 in CoPo[k].d.keys():
   spreadvel[CoPo[k].age[t]].append((CoPo[k].d[t+1]-CoPo[k].d[t])*200. /(5.*60.))
fig, ax = plt.subplots(1)
for a in radvel.keys():
  if not a == 0:
    avg_radvel[a] = np.mean(radvel[a])
    avg_spreadvel[a] = np.mean(spreadvel[a])
    avg_FFvel[a] = np.mean(FFvel[a])
    avg_FFvel2[a] = np.mean(FFvel2[a])

ax.plot(np.divide(avg_radvel.keys(),5.),avg_radvel.values(),linewidth=2,label='v$\mathregular{_r}$')
ax.plot(np.divide(np.add(avg_radvel.keys(),0.5),5.),avg_spreadvel.values(),linewidth=2,label='v$\mathregular{_s}$')
ax.plot(np.divide(avg_FFvel.keys(),5.),avg_FFvel.values(),linewidth=2,label='FF')
ax.plot(np.divide(avg_FFvel2.keys(),5.),avg_FFvel2.values(),linewidth=2,label='v$\mathregular{_t}$')



#ax.set_ylabel('velocity / m s$\mathregular{^{-1}}$')
#
#ax.set_xlabel('tracer age / (5 min)')
#ax.legend()


#ax.set_ylim(-0.5,4.5)
#ax.set_xlim(0,4)
#ax.set_xticks(np.arange(0,4,1))
#ax.set_aspect(20.0)
#plt.legend()
ctime =datetime.datetime.now()
print 'took ',(ctime-atime), 'for all'
plt.show()

fig.savefig('plots/age_vr2.pdf') #'testplots/'+EXPID+'_age_vr_all_otherrange.pdf')

plt.show()
