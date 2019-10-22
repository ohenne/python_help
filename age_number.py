import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import operator
import datetime
import os #to use environment eg path from profile
from classes import CPlife,COL 
from six.moves import cPickle
from collections import OrderedDict
EXPID =  'lindp2K_500tr'#
odir = os.environ.get('results')
ngp = 1024

# read grid point distribution info
f = open(odir+'/coldpool/'+EXPID+'/output/cp/CPlife.save', 'rb')
a = cPickle.load(f)
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


for k in a.keys(): # loop trough all CPS
  j = (a[k].start-47)-(a[k].start-47)%dt  + 47
  for kk in a[k].age.keys(): # loop trough all ages fpr this CP
   if a[k].age[kk] < 29:
    if not a[k].age[kk] in xxm[j].keys():  # if key for age nit exists
      xxm[j][a[k].age[kk]] = 0
    xxm[j][a[k].age[kk]] +=1

fig, ax = plt.subplots(1,figsize=(10,10))
colors = plt.cm.jet(np.linspace(0.2,1,len(trange[:-1])))
simstart =  datetime.datetime(2018,1,1,8,5)
time_list = [simstart + datetime.timedelta(minutes=5*x) for x in trange]
i = 0
for t in trange[:-1]:
 i += 1
 lists = sorted(xxm[t].items()) # sorted by key, return a list of tuples
 x, y = zip(*lists)
 ax.plot(np.multiply(x,5),y,label=time_list[i-1].strftime('%H:%M') +'-'+ time_list[i].strftime('%H:%M'),color=colors[i-1],linewidth=2)

ax.set_ylabel('# cold pools')
ax.set_xlabel('CP age / min')
ax.legend()
fig.savefig('plots/age_number.pdf')
plt.show()

