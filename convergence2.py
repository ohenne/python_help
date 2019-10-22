import numpy as np
import numpy.ma as ma
import os   # for environment 
import copy
import math
import matplotlib
import random
import operator
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
EXPID ='lindp2K_13' #'test1plus4K' #'lind_p2K' #'test1plus4K'# 'lindp2K'#
DIR = '$modelo/UCLA_lind/lind_p2K/lind_p2K_budget.nc'
dir = '/nbi/ac/conv1/henneb/results/coldpool/'
data_in    = Dataset('/nbi/ac/cond3/rawdata/UCLA_lind/lind_p2K/lind_p2K_budget.nc', 'r')

bins = np.linspace(-0.03, 0.03, 100)
bins2 = np.linspace(-0.03, 0.03, 50)
fig, ax = plt.subplots(2,2)
fig2,ax2 = plt.subplots(2,2,figsize=(20,10))
fig3,ax3=plt.subplots()
colors = plt.cm.winter(np.linspace(0,1,12))
timestart = datetime.datetime(2018,01,01,12)
#firsttime = timestart+datetime.timedelta(minutes=5)
print timestart
con_in = np.array(data_in.variables["conv_h_sfc"][17:23,:,:])
n,x,_ = ax[0,0].hist(con_in.ravel(), bins, histtype='step',alpha=0.5,normed=1,color=colors[0])
bin_centers = 0.5*(x[1:]+x[:-1])
ax2[0,0].plot(bin_centers,n,label=datetime.time(9).strftime("%H:%M"),color=colors[0])


for it in range(47,107,6):
  con_in = np.array(data_in.variables["conv_h_sfc"][it-1:it-1+6,:,:])
  tr_mask =np.ones(con_in.shape,dtype=bool)
  dummy_mask = np.ones(con_in.shape)
  tr_mask2 =np.ones(con_in.shape,dtype=bool)
  tr_mask3 =np.ones(con_in.shape,dtype=bool)

  for i in range(0,6):
    inn=int(it+1+i)
    tracer_data_in = Dataset(dir+EXPID+'/output/cp/tracermask'+str(inn)+'.nc','r')
    CPoutl_data_in = Dataset(dir+EXPID+'/output/cp/tracer'+str(inn)+'.nc','r')
    tr_mask[i,:,:] = np.array(tracer_data_in.variables["data"])
    tr_mask3[i,:,:] =np.array(CPoutl_data_in.variables["data"])
    tr_mask_inv = np.subtract(1,tr_mask[i,:,:]) 
    # include neigbouring gridpoints
    tr_mask2[i,:,:] =np.subtract(1,np.multiply(np.multiply( np.multiply(np.multiply(np.multiply(np.multiply( np.multiply(np.multiply(
                      tr_mask_inv, 
                      np.roll(tr_mask_inv,-1,0)),np.roll(tr_mask_inv,-1,1)),np.roll(tr_mask_inv,1,0)),np.roll(tr_mask_inv,1,1)),
                      np.roll(np.roll(tr_mask_inv,-1,1),-1,0)),np.roll(np.roll(tr_mask_inv,-1,1),1,0)),
                      np.roll(np.roll(tr_mask_inv, 1,1),-1,0)),np.roll(np.roll(tr_mask_inv, 1,1),1,0)))
#     tr_mask3[i,:,:] =np.subtract(1,np.multiply(np.multiply(np.multiply(np.multiply
#                                  (np.multiply(np.multiply(np.multiply(np.multiply
#                                  (np.multiply(np.multiply(np.multiply(np.multiply
#                                  (np.multiply(np.multiply(np.multiply(np.multiply
#                                  (np.multiply(np.multiply(np.multiply(np.multiply
#                                  (np.multiply(np.multiply(np.multiply(np.multiply
#                    (tr_mask_inv, np.roll(tr_mask_inv,-1,0)),np.roll(tr_mask_inv,-1,1)),np.roll(tr_mask_inv, 1,0)),np.roll(tr_mask_inv, 1,1)),
#                                  np.roll(tr_mask_inv, 2,1)),np.roll(tr_mask_inv, 2,0)),np.roll(tr_mask_inv,-2,1)),np.roll(tr_mask_inv,-2,0)),
#                                  np.roll(np.roll(tr_mask_inv,-1,1),-1,0)),np.roll(np.roll(tr_mask_inv,-1,1),1,0)),
#                                  np.roll(np.roll(tr_mask_inv, 1,1),-1,0)),np.roll(np.roll(tr_mask_inv, 1,1),1,0)),
#                                  np.roll(np.roll(tr_mask_inv,-1,1),-2,0)),np.roll(np.roll(tr_mask_inv,-1,1),2,0)),
#                                  np.roll(np.roll(tr_mask_inv, 1,1),-2,0)),np.roll(np.roll(tr_mask_inv, 1,1),2,0)),
#                                  np.roll(np.roll(tr_mask_inv,-2,1),-1,0)),np.roll(np.roll(tr_mask_inv,-2,1),1,0)),
#                                  np.roll(np.roll(tr_mask_inv, 2,1),-1,0)),np.roll(np.roll(tr_mask_inv, 2,1),1,0)),
#                                  np.roll(np.roll(tr_mask_inv,-2,1),-2,0)),np.roll(np.roll(tr_mask_inv,-2,1),2,0)),
#                                  np.roll(np.roll(tr_mask_inv, 2,1),-2,0)),np.roll(np.roll(tr_mask_inv, 2,1),2,0)))


    #tr_mask2[i,:,:] = np.subtract(1,np.array(tracer_data_in.variables["data"]))

  con_in_mask = con_in.ravel()[tr_mask.ravel()]
  con_in_mask2 = con_in.ravel()[tr_mask2.ravel()]
  con_in_mask3 = con_in.ravel()[tr_mask3.ravel()]

  n,x,_ = ax[0,0].hist(con_in.ravel(), bins, histtype='step',alpha=0.5,normed=1,label=timestart.strftime("%H:%M"), color=colors[((it-47)/6)+1])
  m,y,_ = ax[0,0].hist(con_in_mask, bins, histtype='step',alpha=0.5,normed=1, label=timestart.strftime("%H:%M"),linewidth=2.2,color=colors[((it-47)/6)+1])
  l,z,_ = ax[0,0].hist(con_in_mask2.ravel(), bins, histtype='step',alpha=0.5,normed=1, label=str(it),linewidth=2.2)
  k,s,_ = ax[0,0].hist(con_in_mask3.ravel(), bins, histtype='step',alpha=0.5,normed=1, label=str(it),linewidth=2.2)

  nn,xx,_ = ax[1,0].hist(con_in.ravel(), bins2, histtype='step',label=timestart.strftime("%H:%M"), color=colors[((it-47)/6)+1])
  mm,yy,_ = ax[1,0].hist(con_in_mask, bins2, histtype='step', label=timestart.strftime("%H:%M"),linewidth=2.2,color=colors[((it-47)/6)+1])
  
  bin_centers2 = 0.5*(xx[1:]+xx[:-1])
  print np.max(np.divide(np.multiply(100.,mm),nn))
  ax3.plot(bin_centers2,np.divide(np.multiply(100.,mm),nn),color=colors[((it-47)/6)+1])
  bin_centers = 0.5*(x[1:]+x[:-1])

  ax2[0,0].plot(bin_centers,n,label=timestart.strftime("%H:%M"),color=colors[((it-47)/5)+1])
  ax2[1,0].plot(bin_centers,m,label=timestart.strftime("%H:%M"),color=colors[((it-47)/5)+1])
  ax2[1,1].plot(bin_centers,l,label=timestart.strftime("%H:%M"),color=colors[((it-47)/5)+1])
  ax2[0,1].plot(bin_centers,k,label=timestart.strftime("%H:%M"),color=colors[((it-47)/5)+1])

  mean00 = np.mean(con_in.ravel()[:])
  ax2[0,0].plot([mean00,mean00], [0, 10], 'k-', lw=2,color=colors[((it-47)/5)+1])
  mean00 = np.mean(con_in_mask)
  ax2[1,0].plot([mean00,mean00], [0, 10], 'k-', lw=2,color=colors[((it-47)/5)+1])
  mean00 = np.mean(con_in_mask2)
  ax2[1,1].plot([mean00,mean00], [0, 10], 'k-', lw=2,color=colors[((it-47)/5)+1])
  mean00 = np.mean(con_in_mask3)
  ax2[0,1].plot([mean00,mean00], [0, 10], 'k-', lw=2,color=colors[((it-47)/5)+1])

  median00 = np.median(con_in.ravel()[:])
  ax2[0,0].plot([median00,median00], [240, 250], 'k-', lw=2,color=colors[((it-47)/5)+1])
  median00 = np.median(con_in_mask)
  ax2[1,0].plot([median00,median00], [130, 140], 'k-', lw=2,color=colors[((it-47)/5)+1])
  median00 = np.median(con_in_mask2)
  ax2[1,1].plot([median00,median00], [110, 120], 'k-', lw=2,color=colors[((it-47)/5)+1])
  median00 = np.median(con_in_mask3)
  ax2[0,1].plot([median00,median00], [110, 120], 'k-', lw=2,color=colors[((it-47)/5)+1])

  timestart=timestart+timedelta(minutes=30)

left = 0.02 #, width = .05, .5
bottom = 0.02 #, height = .45, .0
right = 0.98 #left + width
top = 0.98 # bottom + height


ax2[0,0].text(left, top, 'a) all grid points',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax2[0,0].transAxes)

ax2[0,0].text(0.45, top, 'median',
        horizontalalignment='left',
        verticalalignment='center',
        transform=ax2[0,0].transAxes)
ax2[0,0].text(0.45, bottom, 'mean',
        horizontalalignment='left',
        verticalalignment='center',
        transform=ax2[0,0].transAxes)


ax2[1,0].text(left, top, 'b) grid points with tracer',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax2[1,0].transAxes)
ax2[1,1].text(left, top, 'd) grid points with tracer '+'\n' +'and neighbours ',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax2[1,1].transAxes)

#ax2[1,1].text(left, top, 'd)  grid points with tracer '+'\n' +'and 2 neighbours ',
ax2[0,1].text(left, top, 'c) gridpoints at CP boundaries ',
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax2[0,1].transAxes)

ax[0,0].set_xlim(-0.015,0.02)
ax[0,0].legend()
ax[0,0].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')

ax[1,0].set_xlim(-0.015,0.02)
ax[1,0].legend()
ax[1,0].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')

ax[0,1].set_xlim(-0.015,0.02)
ax[0,1].legend()
ax[0,1].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')

ax3.set_xlim(-0.025,0.025)
ax3.set_ylim(0.,100)
ax3.legend()

ax2[0,0].set_xlim(-0.015,0.02)
ax2[0,0].legend()
ax2[0,0].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')
ax2[0,0].set_ylabel('normalized frequency / kg$\mathregular{^{-1}}$ m$\mathregular{^{2}}$ s')

#ax2[0,0].legend(loc='upper left')

ax2[1,0].set_xlim(-0.015,0.02)
#ax2[1,0].legend()
#ax2[1,0].legend(loc='upper left')
ax2[1,0].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')
ax2[1,0].set_ylabel('normalized frequency / kg$\mathregular{^{-1}}$ m$\mathregular{^{2}}$ s')

ax2[0,1].set_xlim(-0.015,0.02)
#ax2[0,1].legend()
#ax2[0,1].legend(loc='upper left')
ax2[0,1].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')
ax2[0,1].set_ylabel('normalized frequency / kg$\mathregular{^{-1}}$ m$\mathregular{^{2}}$ s')

ax2[1,1].set_xlim(-0.015,0.02)
#ax2[1,1].legend()
#ax2[1,1].legend(loc='upper left')
ax2[1,1].set_xlabel('convergence / kg m$\mathregular{^{-2}}$ s$\mathregular{^{-1}}$')
ax2[1,1].set_ylabel('normalized frequency / kg$\mathregular{^{-1}}$ m$\mathregular{^{2}}$ s')

plt.show()

