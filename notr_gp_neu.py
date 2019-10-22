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
end = 640 #last bin of how many tarcers end up in one grid cell
left,bottom, width, height= [0.05,0.05,0.39,0.36] # left bottom with height
dtick=100 
ni = 13

#EXPID ='lindp2K_13' #'test1plus4K' #'lind_p2K' #'test1plus4K'# 'lindp2K'#
#end = 640

dn =1 # bins

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
tr_range =range(0,end+dn,dn)

###############################################
# INIT DATA
#############################################
data = {}
data2={}
data_rand2={}
data_rand = {}

datapdf = {}
data2pdf={}
data_rand2pdf={}
data_randpdf = {}

for nn in tr_range:
  data[nn] = 0
  data2[nn] =  0
  data_rand[nn] = 0
  data_rand2[nn] = 0
# if subbinning is required
#for nn in range(1,dn,1):
#  data[nn] = 0
#  data2[nn] =  0
#  data_rand[nn] = 0
#  data_rand2[nn] = 0

tist = 0
tot = 0
tot2 = 0
fig0, ax0 = plt.subplots(1)
ax0.set_xlim(0,1024)
ax0.set_ylim(0,1024)
colorsmap = plt.cm.winter(np.linspace(0,1,104)) #  0.2,1,len(range(200,end+dn,dn))))

#################################
# READ and SORT DATA
###############################
nTrtot1 = 0 
nTrtot2 = 0
nt = 0
nt2 = 0
tist2 =0
plotmap=np.empty((1024,1024))
for (t,x,y) in sorted(CPmap.keys(),key=itemgetter(0)): # data2[0:10]: #CPmap.keys()[0:10]:
  if t > tist:
   nt += 1
   tist =t
 #if not CPmap[(t,x,y)].nTrtot == 1:
  nn  =(CPmap[(t,x,y)].nTrtot-1)- (CPmap[(t,x,y)].nTrtot-1)%dn
  if nn > 200:  
    i = (min(nn,end)-200)/dn
    #print 'plot at ', t-46
    #ax0.plot(x,y,'s', markersize=2,markerfacecolor=colorsmap[min(t-46,70)],markeredgecolor="None",zorder=1)
    plotmap[x-1,y-1] = t
  if CPmap[(t,x,y)].nTrtot == 0:
    print 'ohoh'
  else:
    nTrtot1 += CPmap[(t,x,y)].nTrtot 

  if nn > end:
    #;print 'more than '+str(end)
   data[end] += 1  
#  elif nn == 0:
#    data[CPmap[(t,x,y)].nTrtot-1] +=1 
  else:
    data[nn] += 1
  tot  +=1
  # for a selected time range
  if t > 70 and t< 77:
    if t > tist2:
      nt2 += 1
      tist2 =t
    nTrtot2 += CPmap[(t,x,y)].nTrtot
    if nn > end:
      print 'more than '+str(end)
      data2[end] += 1
#    elif nn == 0:
#      data2[CPmap[(t,x,y)].nTrtot-1] += 1
    else:
      data2[nn] += 1
    tot2 += 1
    if nn > 300 :
      print(t,x,y), nn 
btime = datetime.datetime.now()
print 'took ',(btime-atime), 'to sort the tracer'
ax0.contour(plotmap, origin='lower')

#####################################
# MAKE RANDOM DATA FOR COMPARISON
#####################################
rand_set=list(np.random.randint(tot, size=nTrtot1))
rand_set2=list(np.random.randint(tot2, size=nTrtot2))

ctime = datetime.datetime.now()
print 'took ',(ctime-btime), 'to create random data'
print 'timeintervall',tot2, nTrtot2
print 'all',tot, nTrtot1
#[[x,count(rand_set2,x)] for x in set(rand_set2)]

# loop trough every tracer to get 'grid point' and count how many tracer ar at one gp: 
rand_map2 = list(np.zeros(tot2))

for i in range(0,len(rand_set2)):
  rand_map2[rand_set2[i]] += 1
etime = datetime.datetime.now()
print 'took ',(etime-ctime), 'to count number of tracer on gridpoints in small random data'

rand_map1 = list(np.zeros(tot))
for i in range(0,len(rand_set)):
  rand_map1[rand_set[i]] += 1
ftime = datetime.datetime.now()
print 'took ',(ftime-etime), 'to count number of tracer on gridpoints in all random data'

for i in rand_map2:
 nn  =  (i-1)- (i-1)%dn
 if not nn <0:
  if nn > end:
    data_rand2[end] += 1
#  elif nn == 0:
#    data_rand2[i-1] += 1
  else:
    data_rand2[nn] += 1
gtime = datetime.datetime.now()
print 'took ',(gtime-ftime), 'to count no of gridpoints with certain numbert of tracer'

for i in rand_map1:
 nn  =  (i-1)- (i-1)%dn
 if not nn < 0:
  if nn > end:
    data_rand[end] += 1
#  elif nn==0:
#    data_rand[i-1] += 1
  else:
    data_rand[nn] += 1
htime = datetime.datetime.now()
print 'took ',(htime-gtime), 'to count no of gridpoints with certain numbert of tracer'

#################################
# MAKE CUMULATIVE DISTRIBUTION OUT OF PDF
#################################
keys = sorted(data.keys())[::-1]
for nn in sorted(data.keys())[0:ni]: #tr_range:
 datapdf[nn] = float(data[nn]) /float(tot)
 data2pdf[nn] = float(data2[nn]) /float(tot2)
 data_randpdf[nn] = float(data_rand[nn]) /float(tot) #(nxnx*nt)#float(tot)
 data_rand2pdf[nn] = float(data_rand2[nn]) /float(tot2)#(nxnx*nt2) #float(tot2)

for ii in range(0,len(data.keys())-1,1): #0,-1): sorted(data.keys())[-2:0]: #range(end-dn,0-dn,-dn):
  mn = keys[ii]
  mm = keys[ii+1]
  data[mm] = data[mm] + data[mn]
  data2[mm]=data2[mm] + data2[mn]
  data_rand[mm]=data_rand[mm] + data_rand[mn]
  data_rand2[mm]=data_rand2[mm] + data_rand2[mn]
for nn in data.keys(): #tr_range:
 data[nn] = float(data[nn]) /float(tot)
 data2[nn] = float(data2[nn]) /float(tot2)
 data_rand[nn] = float(data_rand[nn]) /float(tot) #(nxnx*nt)#float(tot)
 data_rand2[nn] = float(data_rand2[nn]) /float(tot2)#(nxnx*nt2) #float(tot2)

#print 'took ',(ftime-etime), 'to cumulate the data'

########################################
# MAKE PLOT
#######################################
# DATA FOR TRACER PLPT ALL
lists = sorted(data.items()) # sorted by key, return a list of tuples
listsr = sorted(data_rand.items()) # sorted by key, return a list of tuples
lists2 = sorted(data2.items()) # sorted by key, return a list of tuples
listsr2 = sorted(data_rand2.items()) # sorted by key, return a list of tuples

# for small plot
listspdf = sorted(datapdf.items()) # sorted by key, return a list of tuples
listsrpdf = sorted(data_randpdf.items()) # sorted by key, return a list of tuples
lists2pdf = sorted(data2pdf.items()) # sorted by key, return a list of tuples
listsr2pdf = sorted(data_rand2pdf.items()) # sorted by key, return a list of tuples

x, y = zip(*lists)
xr,yr = zip(*listsr)
x2, y2 = zip(*lists2)
xr2,yr2 = zip(*listsr2)

xpdf, ypdf = zip(*listspdf)
xrpdf,yrpdf = zip(*listsrpdf)
x2pdf, y2pdf = zip(*lists2pdf)
xr2pdf,yr2pdf = zip(*listsr2pdf)

# MAKE FIRST PLOT 
fig, ax = plt.subplots(1)
ax.semilogy(x,y,'darkorange',linewidth=2,label=str(nTrtot1)+ 'tracer, '+str(tot) +' gc')
ax.semilogy(xr,yr,'navajowhite',linewidth=2,label=str(nTrtot1)+' random seeds, '+str(tot) +' gc')
ax.semilogy(x2,y2,'royalblue',linewidth=2, label=str(nTrtot2)+ 'tracer, '+str(tot2)+ 'gc')
ax.semilogy(xr2,yr2,'cornflowerblue',linewidth=2, label=str(nTrtot2)+ 'random seeds, '+str(tot2)+' gc')

# insert small figure
ax2 = plt.axes([0,0,1,1]) #fig.add_axes([left, bottom, width, height])
ip = InsetPosition(ax, [left,bottom, width, height]) # left bottom with height
ax2.set_axes_locator(ip)


#ax2.plot(x[0:ni],y[0:ni],'darkorange',linewidth=2)
#ax2.plot(xr[0:ni],yr[0:ni],'navajowhite',linewidth=2)
#ax2.plot(x2[0:ni],y2[0:ni],'royalblue',linewidth=2)
#ax2.plot(xr2[0:ni],yr2[0:ni],'cornflowerblue',linewidth=2)

ax2.plot(xpdf,ypdf,'darkorange',linewidth=2)
ax2.plot(xrpdf,yrpdf,'navajowhite',linewidth=2)
ax2.plot(x2pdf,y2pdf,'royalblue',linewidth=2)
ax2.plot(xr2pdf,yr2pdf,'cornflowerblue',linewidth=2)


xstr = [">"+str(x[ii]) for ii in range(len(x))]
ax.set_xticks(x[::dtick])
ax.set_xticklabels(xstr[::dtick])
ax.set_xlabel('tracers per grid cell')
ax.set_ylabel('fraction of total grid cells with tracer' )

ax2.set_xticks(x[0:ni:ni-2])
ax2.set_xticklabels(x[1:ni+1:ni-1])
ax2.set_xticks(x[0:ni], minor=True)

#ax2.minorticks_on()
#ax2.yaxis.set_major_locator(plt.NullLocator())
#ax2.xaxis.set_minor_locator(x[0:10])
ax2.yaxis.tick_right()
yti = ax2.get_yticks()[::2]
ax2.set_yticks(yti)
ax2.set_yticklabels(["."+ "{:.0f}".format(yti[ii]*10) for ii in range(len(yti))])
#ax2.set_yticklabels('')
ax.legend()
fig.savefig('pdf_log_random_'+EXPID+'.pdf')
fig0.savefig('morethan200.pdf')

#plt.show()




 
