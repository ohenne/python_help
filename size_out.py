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

odir = '/nbi/ac/conv1/henneb/results/coldpool/'
EXPID ='lindp2K_500tr_lvl10' #'lindp2K_500tr'

f = open('/nbi/ac/conv1/henneb/results/coldpool/'+EXPID+'/output/cp/coldpool_tracer_out_all.txt', 'r')
lines = f.readlines()

CPsize={}
CPdist={}
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

    if not (cCP,age) in CPdist.keys():
      CPdist[(cCP,age)] = []
      if not cCP in CPsize.keys():
        CPsize[cCP] = {}
    CPdist[(cCP,age)].append(dist) 

for (kc,ka) in  CPdist.keys():
  CPsize[kc][ka] = np.mean(CPdist[(kc,ka)])


f = open(odir+EXPID+'/output/cp/Size.save', 'wb')
cPickle.dump(CPsize, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
   
    

