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
params = {'legend.fontsize': '12',
          'figure.figsize': (5, 6),
         'axes.labelsize': '12',
         'axes.titlesize':'12',
         'xtick.labelsize':'12',
         'ytick.labelsize':'12'}
pylab.rcParams.update(params)

EXPID ='lindp2K_13' #'test1plus4K' #'lind_p2K' #'test1plus4K'# 'lindp2K'#
dir = '/nbi/ac/conv1/henneb/results/coldpool/'
data_in    = Dataset('/nbi/ac/cond3/rawdata/UCLA_lind/lind_p2K/lind_p2K_budget.nc', 'r')
nt = 12
simstart =  datetime.datetime(2018,1,1,8,05)
ztime = datetime.datetime.now()
f = open(dir+EXPID+'/output/cp/TracerMap.save', 'rb')
CPmap = cPickle.load(f)
f.close()

fig, ax = plt.subplots(2,2)
timestart = datetime.datetime(2018,01,01,8)
atime = datetime.datetime.now()
print 'took ',(atime-ztime), 'to read data MAP'

con_in = np.array(data_in.variables["conv_h_sfc"][46,:,:])
btime = datetime.datetime.now()
print 'took ',(btime-atime), 'to read data'

outdat = {}
plotdata = {}
outdat2 = {}
plotdata2 = {}
outdat3 = {}
plotdata3 = {}
trange =range(47,162,nt)
colors = plt.cm.winter(np.linspace(0,1,len(trange)+2))

data = CPmap.keys()
data2 = sorted(data,key=itemgetter(0))
ctime = datetime.datetime.now()
print 'took ',(ctime-btime), 'for stuff'

for ti in trange:
  outdat[ti] = {}
  outdat2[ti] = {}
  plotdata[ti] = {}
  for i in [1,2,3,4,5]:
    outdat[ti][i] = []
    outdat2[ti][i] = 0
arange = range(0,31,1)
for i in [1,2,3,4]:
  outdat3[i] = {}
  plotdata3[i] = {}
  for a in arange:
    outdat3[i][a] = []
dtime = datetime.datetime.now()
print 'took ',(dtime-ctime), 'for initial loop'
 
tist = 47
for (t,x,y) in sorted(CPmap.keys(),key=itemgetter(0)): # data2[0:10]: #CPmap.keys()[0:10]:
  ti = t - (t-47)%nt  # binned to traneg
  outdat[ti][min(CPmap[(t,x,y)].nCPs,5)].append(CPmap[(t,x,y)].nTrtot)
  outdat2[ti][min(CPmap[(t,x,y)].nCPs,5)] += 1
  for CPID in CPmap[(t,x,y)].age.keys():
    age = CPmap[(t,x,y)].age[CPID]
    a = age #%age - (age%5)
    outdat3[min(CPmap[(t,x,y)].nCPs,4)][a].append(CPmap[(t,x,y)].nTrCP[CPID])
etime = datetime.datetime.now()
print 'took ',(etime-dtime), 'for main loop'
  
# outdat binned by timerange, keys for every time range: no CP
# outdat3 binned by no CP, keys for every class: age

#labels, data = outdat[47].keys(), outdat[47].values()
#
#plt.boxplot(data)
#plt.xticks(range(1, len(labels) + 1), labels)

#labels, data = [*zip(*outdat.items())]
i = 0
pb={}
time_list = [simstart + datetime.timedelta(minutes=5*x) for x in range(47,174,nt)]

for ti in trange:
   
   i += 1
   print ti,i
   sumdat = float(np.sum(outdat2[ti].values()) )
   for k in outdat[ti].keys():
     plotdata[ti][k] = np.mean(outdat[ti][k])
     #print float(np.sum(outdat2[ti].values()))
     if not sum(outdat2[ti].values()) == 0:
       outdat2[ti][k] = float(outdat2[ti][k])/sumdat
   timelab = (i-1)*5  
   ax[1,1].plot(outdat[ti].keys(),plotdata[ti].values(),color=colors[i],label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'))
   ax[0,0].plot(outdat[ti].keys(),outdat2[ti].values(),color=colors[i],label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'))
   ax[1,0].plot(outdat[ti].keys(),np.divide(plotdata[ti].values(),outdat[ti].keys()),color=colors[i],label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'))

colors = plt.cm.winter(np.linspace(0,1,6)) #len(arange)+2))
for k in outdat3.keys(): 
   for a in arange: #outdat3[a].keys():
     plotdata3[k][a] = np.mean(outdat3[k][a])
     print a, plotdata3[k][a]
   ax[0,1].plot(plotdata3[k].keys(),plotdata3[k].values(),color=colors[k],label = '# CP edge in grid cell')

ax[0,0].set_xlim(1,5)
ax[1,1].set_xlim(1,5)
#ax[0,1].set_xlim(1,5)
ax[1,0].set_xlim(1,5)

ax[0,0].set_xticks(np.arange(1,5,1))
ax[1,0].set_xticks(np.arange(1,5,1))
#ax[0,1].set_xticks(np.arange(1,5,1))
ax[1,1].set_xticks(np.arange(1,5,1))

ax[0,0].set_xlabel('# CP edge in grid cell')
ax[1,0].set_xlabel('# CP edge in grid cell')
ax[1,1].set_xlabel('# CP edge in grid cell')
ax[0,1].set_xlabel('CP age')

ax[0,0].legend()
ax[1,0].legend()
ax[1,1].legend()
labels = ('1 CP edge in grid cell', '2 CP edges in grid cell', '3 CP edges in grid cell', '$\geq$ 4 CP edges in grid cell'  )
ax[0,1].legend(labels)


ax[1,1].set_xlim(1,5)
#ax[0,1].set_xlim(1,5)
ax[1,0].set_xlim(1,5)



left = 0.02 #, width = .05, .5
bottom = 0.02 #, height = .45, .0
right = 0.98 #left + width
top = 0.98 # bottom + height

ax[0,0].text(left, top, 'a) grid points with CP edge ',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[0,0].transAxes)

ax[0,1].text(left, top, 'b) number of tracer per gridbox',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[0,1].transAxes)
ax[1,0].text(left, top, 'c) as d divided by # CP',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[1,0].transAxes)

#ax2[1,1].text(left, top, 'd)  grid points with tracer '+'\n' +'and 2 neighbours ',
ax[1,1].text(left, top, 'd) as b sorted by time range',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax[1,1].transAxes)


plt.show()




 
