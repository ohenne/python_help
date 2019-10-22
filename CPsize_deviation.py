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
makedataCP=False
makedataPR=True
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
# GET PRECIP DATA
########################################################
if makedataPR:

  f = open(idir+'/raincell/irt_objects_output.txt', 'r')
  lines = f.readlines()
  PREC = {}
  AREA = {}
  for line in lines:
    columns = line.split()
    objID = (int(columns[1]))
    if objID > 0:
      tist    = (int(columns[0])) 
      prec_ob = (float(columns[4]))
      area = (float(columns[3]))
      if not tist in PREC.keys():
        PREC[tist] = 0
        AREA[tist] = 0
      PREC[tist] += prec_ob*area
      AREA[tist] += area

  #mean_PREC = np.divide(PREC[],AREA)
  #min_PREC = {}
  #max_PREC={}
  mean_PREC={}
  #std_PREC={}
  for i in PREC.keys():
   if AREA > 0:
    #min_PREC[i]  = np.percentile(PREC[i],10)
    #max_PREC[i]  = np.percentile(PREC[i],90)
    mean_PREC[i] = PREC[i]/AREA[i]
    #std_PREC[i] = np.std(PREC[i])

  # SAVE DATA
  f = open('tempstore/PRECmean.save', 'wb')
  cPickle.dump(mean_PREC, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

  #f = open('tempstore/PRECmin.save', 'wb')
  #cPickle.dump(min_PREC, f, protocol=cPickle.HIGHEST_PROTOCOL)
  #f.close()

  #f = open('tempstore/PRECmax.save', 'wb')
  #cPickle.dump(max_PREC, f, protocol=cPickle.HIGHEST_PROTOCOL)
  #f.close()

  #f = open('tempstore/PRECstd.save', 'wb')
  #cPickle.dump(std_PREC, f, protocol=cPickle.HIGHEST_PROTOCOL)
  #f.close()

else:

  f = open('tempstore/PRECmean.save', 'rb')
  mean_PREC = cPickle.load(f)
  f.close()

  #f = open('tempstore/PRECmin.save', 'rb')
  #min_PREC = cPickle.load(f)
  #f.close()

  #f = open('tempstore/PRECmax.save', 'rb')
  #max_PREC = cPickle.load(f)
  #f.close()

  #f = open('tempstore/PRECstd.save', 'rb')
  #std_PREC = cPickle.load(f)
  #f.close()

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
  yerrgp = np.divide(std_size_gp.values(),avg_size_gp.values())
  ax.errorbar(time_list,avg_size_gp.values(),yerrgp, label='grid points', marker=' ', color = 'royalblue',linewidth=1.5)
  ax.plot(time_list,min_size_gp.values(), color = 'cornflowerblue',linewidth=1.5,label='grid points ,10 and 90 percentile')
  ax.plot(time_list,max_size_gp.values(), color = 'cornflowerblue',linewidth=1.5)

  yerrtr = np.divide(std_size_tr.values(),avg_size_tr.values())
  ax.errorbar(time_list,avg_size_tr.values(),yerrtr, label='tracer'     , marker=' ', color='darkorange',linewidth=1.5)
  ax.plot(time_list,min_size_tr.values(), color = 'navajowhite',linewidth=1.5,label='tracer ,10 and 90 percentile')
  ax.plot(time_list,max_size_tr.values(), color = 'navajowhite',linewidth=1.5)

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
  ax.xaxis.set_major_formatter(myFmt)
  ax.legend()
  ax.legend(loc='upper left')

  # PRECI PLOT
  ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis  
  ax2.set_ylabel('precipitation intensity / mm h$\mathregular{^{-1}}$ ', color='seagreen')  # we already handled the x-label with ax1
  time_list2 = [simstart + datetime.timedelta(minutes=5*z) for z in mean_PREC.keys()]

  ax2.plot(time_list2, mean_PREC.values(),label='precipitation',marker=' ', color='seagreen',linewidth=1.5)

  ax2.tick_params(axis='y', labelcolor='seagreen')


  plt.show()
  fig.savefig('plots/CPsize.pdf')


