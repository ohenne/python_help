import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import operator
import datetime
import os #to use environment eg path from profile
from classes import CPlife,COL 
from six.moves import cPickle
from collections import OrderedDict
import matplotlib.pylab as pylab
params = {'legend.fontsize': '10',
          'figure.figsize': (5.5, 4.5),
         'axes.labelsize': '14',
         'axes.titlesize':'12',
         'xtick.labelsize':'14',
         'ytick.labelsize':'14'}
pylab.rcParams.update(params)
EXPID =  'lindp2K_500tr'#
odir = os.environ.get('results')
ngp = 1024

# read grid point distribution info
f = open(odir+'/coldpool/'+EXPID+'/output/cp/CPlife.save', 'rb')
a = cPickle.load(f)
f.close()

# read tracer info (eg size)
f = open(odir+'/coldpool/'+EXPID+'/output/cp/Size.save', 'rb')
CPsize = cPickle.load(f)
f.close()
dt = 12
trange=range(47,162,dt)
xxm = {} # tracer on gp
xxo = {} # individual tracer

avg_xxm={}
var_xxm={}
avg_xxo={}
var_xxo={}
p05_xxm={}
p95_xxm={}
p05_xxo={}
p95_xxo={}

for t in trange:
 xxm[t] ={}
 xxo[t] ={}
 avg_xxm[t]={}
 var_xxm[t]={}
 avg_xxo[t]={}
 var_xxo[t]={}
 p05_xxm[t]={}
 p95_xxm[t]={}
 p05_xxo[t]={}
 p95_xxo[t]={}


for k in CPsize.keys(): # loop trough all CPS
  j = (a[k].start-47)-(a[k].start-47)%dt  + 47
  for kk in a[k].age.keys(): # loop trough all ages fpr this CP
   if a[k].age[kk] in CPsize[k].keys():
    if not a[k].age[kk] in xxm[j].keys():  # if key for age nit exists
      xxm[j][a[k].age[kk]] = []
    xxm[j][a[k].age[kk]].append(CPsize[k][a[k].age[kk]])

fig, ax = plt.subplots(1)
colors = plt.cm.winter(np.linspace(0,1,len(trange[:-2])))
simstart =  datetime.datetime(2018,1,1,8,5)
time_list = [simstart + datetime.timedelta(minutes=5*x) for x in trange]
i = 0
for t in trange[:-2]:
 i += 1
 for k in sorted(xxm[t].keys()):  #loop trough every age
  if len(xxm[t][k]) > 5:
   print k 
   avg_xxm[t][k] = np.mean(xxm[t][k])
   var_xxm[t][k] = np.var (xxm[t][k])
   p05_xxm[t][k] = np.percentile(xxm[t][k],25)
   p95_xxm[t][k] = np.percentile(xxm[t][k],75)
 lists = sorted(avg_xxm[t].items()) # sorted by key, return a list of tuples
 x, y = zip(*lists)
 list05 = sorted(p05_xxm[t].items())
 x,y05 = zip(*list05)
 list95 = sorted(p95_xxm[t].items())
 x,y95 = zip(*list95)
 
# ax[0].errorbar(avg_xxm[t].keys(),avg_xxm[t].values(),yerr=np.vstack([p05_xxm[t].values(),p95_xxm[t].values()]), 
#  label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'),color=colors[i-1], marker=' ',linewidth=1.5)
# ax[1].errorbar(avg_xxo[t].keys(),avg_xxo[t].values(),yerr=np.vstack([p05_xxo[t].values(),p95_xxo[t].values()]), label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'),color=colors[i-1], marker=' ',linewidth=1.5)
 #print avg_xxm[t].keys(), avg_xxm[t].values()
 #ax[0].plot(sorted(avg_xxm[t].keys()),for k in sorted(avg_xxm[t].keys()) avg_xxm[t].values(),
 ax.plot(np.multiply(x,5),np.multiply(y,0.2),label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'),color=colors[i-1],linewidth=1.5)

# ax[1].errorbar(x,y,yerr=np.vstack([y05,y95]),label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'),color=colors[i-1],linewidth=1.5)

#ax[1].xaxis.set_ticks(xxm.keys())

#volume / '+'$\mathregular{10^3}$'+'$\mathregular{m^{-3}}$')
#for k in sorted(a.keys()):
#  xx = list(a[k].age.values())
#  yy = list(a[k].noIT.values())
#  ax[1].plot(xx,yy)
ax.set_ylabel('CP radius / km',fontsize=12)
#ax[1].set_ylabel('CP radius / km')
ax.set_xlabel('CP age / min',fontsize=12)
#ax[1].set_xlabel('CP age / min')
ax.set_xlim(0,180)
ax.legend(loc='upper left')
fig.savefig('plots/age_size.pdf')

plt.show()
