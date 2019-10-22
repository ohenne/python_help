import numpy as np
import numpy.ma as ma
import os   # for environment 
import math
import matplotlib
import operator
import matplotlib.pyplot as plt
import datetime
from classes import TRACER,CP_map,  CPstart, CPlife
from operator import itemgetter
from netCDF4 import Dataset
from six.moves import cPickle   # to save class files
import matplotlib.dates as mdates
import matplotlib.pylab as pylab
params = {'legend.fontsize': '12',
          'figure.figsize': (4.5, 4.5),
         'axes.labelsize': '12',
         'axes.titlesize':'12',
         'xtick.labelsize':'12',
         'ytick.labelsize':'12'}
pylab.rcParams.update(params)
makedataCP=False
makedataPR=False
plotdata=True
EXPID = 'lindp2K_500tr'
idir = '/nbi/ac/conv1/henneb/results/coldpool/'+EXPID+'/output/'
###################################################################
# GET  CP DATA
###################################################################

atime = datetime.datetime.now()
if makedataCP:
  size_gp={}
  size_tr={}
  size_tr_CP={}
  cgp = {}
  ctrCP = {}
  for i in range(47,150): #(137,249):
    size_gp[i] ={} 
    ctrCP[i] = {}
    size_tr_CP[i] = {}
  f = open(idir+'/cp/coldpool_tracer_out_all.txt', 'r')
  lines = f.readlines()
  for line in lines:
  #for i in range(1,20000,10):
  #    line = f.readline()
      time1 = datetime.datetime.now()
      columns = line.split()
      tist = (int(columns[0]))     # timestep
  #  if tist < 90: # just for testing and not running trough all data
      age  = (int(columns[1]))     # age
      cCP  = (int(columns[3]))     # belonging to CP ID
      dist = (float(columns[8]))     # distance to cog
      mm   = (int(columns[16]))    # merger = 1
      pID  = (int(columns[17]))  
      size = (float(columns[18]))
      if dist !=0 and dist < 300 and age != 0 and size < 105200 and size != 0:
        if not cCP in size_tr_CP[tist].keys():
          size_tr_CP[tist][cCP] = dist
          ctrCP[tist][cCP] = 1
          size_gp[tist][cCP] = size
        else:
          size_tr_CP[tist][cCP] += dist
          ctrCP[tist][cCP] += 1
  
  print 'read  lines'
  avg_size_tr = {}
  std_size_tr = {}
  min_size_tr = {}
  max_size_tr = {}
  
  avg_size_gp = {}
  std_size_gp = {}
  min_size_gp = {}
  max_size_gp = {}
  
  
  for i in range(48,150): # ize_tr.keys(): #range(1,178):
    for j in size_tr_CP[i].keys():
      size_tr_CP[i][j] = size_tr_CP[i][j]/ctrCP[i][j]
    
    min_size_tr[i] = np.percentile(np.multiply(size_tr_CP[i].values(),float(0.2)),10)
    max_size_tr[i] = np.percentile(np.multiply(size_tr_CP[i].values(),float(0.2)),90)
    avg_size_tr[i] = np.mean(np.multiply(size_tr_CP[i].values(),float(0.2)))
    std_size_tr[i] = np.std (np.multiply(size_tr_CP[i].values(),float(0.2)))
  
    min_size_gp[i] = np.percentile(((np.asarray(size_gp[i].values())/3.14)**0.5)*0.2,10)
    max_size_gp[i] = np.percentile(((np.asarray(size_gp[i].values())/3.14)**0.5)*0.2,90)
    avg_size_gp[i] = np.mean(((np.asarray(size_gp[i].values())/3.14)**0.5)*0.2)
    std_size_gp[i] = np.std( ((np.asarray(size_gp[i].values())/3.14)**0.5)*0.2)
  
  
  # SAVE DATA
  f = open('tempstore/SizeGP.save', 'wb')
  cPickle.dump(avg_size_gp, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  f = open('tempstore/minSizeGP.save', 'wb')
  cPickle.dump(min_size_gp, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  f = open('tempstore/maxSizeGP.save', 'wb')
  cPickle.dump(max_size_gp, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  f = open('tempstore/stdSizeGP.save', 'wb')
  cPickle.dump(std_size_gp, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()


  f = open('tempstore/SizeTR.save', 'wb')
  cPickle.dump(avg_size_tr, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()
  
  f = open('tempstore/minSizeTR.save', 'wb')
  cPickle.dump(min_size_tr, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  f = open('tempstore/maxSizeTR.save', 'wb')
  cPickle.dump(max_size_tr, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  f = open('tempstore/stdSizeTR.save', 'wb')
  cPickle.dump(std_size_tr, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

else:
  f = open('tempstore/SizeGP.save', 'rb')
  avg_size_gp = cPickle.load(f)
  f.close()

  f = open('tempstore/minSizeGP.save', 'rb')
  min_size_gp = cPickle.load(f)
  f.close()

  f = open('tempstore/maxSizeGP.save', 'rb')
  max_size_gp = cPickle.load(f)
  f.close()

  f = open('tempstore/stdSizeGP.save', 'rb')
  std_size_gp = cPickle.load(f)
  f.close()


  f = open('tempstore/SizeTR.save', 'rb')
  avg_size_tr = cPickle.load(f)
  f.close()

  f = open('tempstore/minSizeTR.save', 'rb')
  min_size_tr = cPickle.load(f)
  f.close()

  f = open('tempstore/maxSizeTR.save', 'rb')
  max_size_tr = cPickle.load(f)
  f.close()

  f = open('tempstore/stdSizeTR.save', 'rb')
  std_size_tr = cPickle.load(f)
  f.close()

###########################################################
# MAKE PLOT
########################################################
if plotdata:
  fig,ax = plt.subplots(1)
  #ax.plot(avg_size_gp.keys(),avg_size_gp.values(), linewidth=3.0, label='gp')
  #ax.plot(avg_size_tr.keys(),avg_size_tr.values(), linewidth=3.0,  label='tracer')
  #ax.errorbar(avg_size_gp.keys(),avg_size_gp.values(),std_size_gp.values(),  marker='^')
  #ax.errorbar(avg_size_tr.keys(),avg_size_tr.values(),std_size_tr.values(),  marker='^')
  simstart =  datetime.datetime(2018,1,1,8,5)
  time_list = [simstart + datetime.timedelta(minutes=5*z) for z in avg_size_gp.keys()]
  print time_list
  ax.plot(time_list,avg_size_gp.values(), label='grid points', color = 'royalblue',linewidth=2.5)
  ax.plot(time_list,min_size_gp.values(), color = 'cornflowerblue',linestyle='--',linewidth=1.5,label='grid points, 10 and 90 percentile')
  ax.plot(time_list,max_size_gp.values(), color = 'cornflowerblue',linestyle='--',linewidth=1.5)

  ax.plot(time_list,avg_size_tr.values(), label='tracer'    , color='darkorange',linewidth=2.5)
  ax.plot(time_list,min_size_tr.values(), color = 'navajowhite',linewidth=1.5,linestyle='--',label='tracer, 10 and 90 percentile')
  ax.plot(time_list,max_size_tr.values(), color = 'navajowhite',linewidth=1.5,linestyle='--')

  m,b = np.polyfit(np.divide(avg_size_tr.keys(),12),np.multiply(avg_size_tr.values(),2),1)
  print 'tracer avg',m,b
  m,b = np.polyfit(np.divide(max_size_tr.keys(),12),np.multiply(max_size_tr.values(),2),1)
  print 'tracer max',m,b
  m,b = np.polyfit(np.divide(min_size_tr.keys(),12),np.multiply(min_size_tr.values(),2),1)
  print 'tracer min',m,b
  m,b = np.polyfit(np.divide(avg_size_gp.keys(),12),np.multiply(avg_size_gp.values(),2),1)
  print 'object avg',m,b
  m,b = np.polyfit(np.divide(max_size_gp.keys(),12),np.multiply(max_size_gp.values(),2),1)
  print 'object max',m,b
  m,b = np.polyfit(np.divide(min_size_gp.keys(),12),np.multiply(min_size_gp.values(),2),1)
  print 'object min',m,b

  #ax.plot(min_size_tr.keys(),min_size_tr.values(), linewidth=2.5, color='darkorange')
  #ax.plot(max_size_tr.keys(),max_size_tr.values(), linewidth=2.5, color='darkorange')
  #ax.plot(min_size_gp.keys(),min_size_gp.values(), linewidth=2.5, color='royalblue')
  #ax.plot(max_size_gp.keys(),max_size_gp.values(), linewidth=2.5, color='royalblue')
  
  
  #ax.set_xlabel('model time')
  #ax.set_ylabel('CP-size / $\mathregular{km^{2}}$')
  ax.set_ylabel('CP radius / km')
  myFmt = mdates.DateFormatter('%H:%M')
  ax.set_xticks(time_list[11::24])

  ax.xaxis.set_major_formatter(myFmt)
  ax.legend()
  ax.legend(loc='upper left')

  plt.show()
  fig.savefig('plots/CPsize.pdf')


