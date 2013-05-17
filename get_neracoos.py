# -*- coding: utf-8 -*-
"""
Created on Thu May 02 08:27:24 2013

@author: Huanxin
"""
from matplotlib.dates import date2num, num2date
import datetime as dt

import sys
import matplotlib.pyplot as plt
import numpy as np
from pandas import *


pydir='../'

sys.path.append(pydir)

from neracoos_def import get_neracoos_ctl,depth_select,get_id_s_id_e_id_max_url,get_neracoos_data

'''
Dataset: A01.sbe37.historical.50m.nc
lat, 42.5180647466176
lon, -70.5652227043109
Dataset: B01.sbe37.historical.20m.nc
lat, 43.1806472713891
lon, -70.4276963702579
Dataset: D02.sbe37.historical.10m.nc
lat, 43.7617166666667
lon, -69.9878833333333
Dataset: E01.sbe37.historical.50m.nc
lat, 43.7151721464189
lon, -69.3557710445127
Dataset: E02.sbe37.historical.50m.nc
lat, 43.7065
lon, -69.32
Dataset: F01.sbe37.historical.50m.nc
lat, 44.0556001811715
lon, -68.9967173062176
Dataset: F02.sbe37.realtime.1m.nc
lat, 44.3878
lon, -68.8308
Dataset: I01.sbe37.historical.50m.nc
lat, 44.1059919278702
lon, -68.1084972935196
Dataset: M01.sbe37.historical.250m.nc
lat, 43.4897
lon, -67.8815
Dataset: N01.sbe37.historical.180m.nc
lat, 42.3314893622147
lon, -65.9064274838096
'''


 
inputfilename='./get_neracoos_ctl.txt'
mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites=get_neracoos_ctl(inputfilename) #get input from input file
sdtime_n=date2num(mindtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of start time
edtime_n=date2num(maxdtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of end time
depths,site_d=depth_select(sites,i_mindepth,i_maxdepth) #one site match one depth, 
for index_site in range(len(site_d)):
    period_str,temp_list,depth_list=[],[],[]
    '''
    if i_maxdepth<=10:
        url='http://neracoos.org:8080/opendap/'+index_site+'/'+index_site+'.'+model+'.historical.1m.nc?'
        id_s,id_e,id_max_url=get_id_s_id_e_id_max_url(,url,sdtime_n,edtime_n)
    if i_mindepth>35:
        url='http://neracoos.org:8080/opendap/'+index_site+'/'+index_site+'.'+model+'.historical.50m.nc?'
        id_s,id_e,id_max_url=get_id_s_id_e_id_max_url(,url,sdtime_n,edtime_n)
    '''
    url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.historical.'+depths[index_site]+'m.nc?'     
    id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
    if mintime=='':   
        judgement='1' #"judgement" can help us judge if this  site has historical data.
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.'+depths[index_site]+'m.nc?'     
        id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
    else:
        judgement=''
    if id_e0<>'':  
      (period_str,depth_temp)=get_neracoos_data(url,id_s,id_e0,id_max_url) #get data from web neracoos 
  
      df = DataFrame(np.array(depth_temp),index=period_str,columns=['                depth','      temp','        lat   ','      lon   ' ])
    else:
        print "According to your input, there is no data here"
    
    '''
    if judgement<>'1':
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.'+depths[index_site]+'m.nc?'     
        id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
        if id_e<>'':     
           (period_str,depth_temp)=get_neracoos_data(url,id_s,id_e,id_max_url)  #get data from web neracoos
           #df = DataFrame(np.array(depth_temp),index=period_str,columns=['                depth','      temp']).append(df)
           if id_e0=='':
              df = DataFrame(np.array(depth_temp),index=period_str)
           else:              
              df = DataFrame(np.array(depth_temp),index=period_str).append(df)
    '''
    '''
    df.plot(title=index_site+'_'+model+'\ndepth='+str(depth[0])+'\nlat='+str(lat[0])+'\nlon='+str(lon[0]))
    plt.show()
    
    depth_temp=[]   #convert row to line
    for k in range(len(depth_list)):
        depth_temp.append([depth_list[k],temp_list[k]])
    '''
     #combine them in DataFrame    
    #df = DataFrame(depth_list,temp_list, index=period_str,columns=['depth', 'temp']) #combine them in DataFrame
    #df.plot()
    df.to_csv('temp_'+site_d[index_site]+'.csv') #save it to a csv file
#plt.show()




























'''
mindtime1,maxdtime1,i_mindepth,i_maxdepth,site2,mindtime,maxdtime
	  #According to the conditions to select data from "emolt_sensor"
url2="http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.TIME_LOCAL,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I&emolt_sensor.TIME_LOCAL>="+str(mindtime1)+"&emolt_sensor.TIME_LOCAL<="\
+str(maxdtime1)+"&emolt_sensor.DEPTH_I>="+str(i_mindepth)+"&emolt_sensor.DEPTH_I<="+str(i_maxdepth)+site2
try:   
    dataset1=open_url(url2)
except:
    print 'Sorry, '+url2+' not available' 
    sys.exit(0)
emolt_sensor=dataset1['emolt_sensor']
try:   
	          sites2=list(emolt_sensor['SITE'])
except:
	          print "'Sorry, According to your input, here are no value. please check it! ' "
	          sys.exit(0) 
	  #sites2=list(emolt_sensor['SITE'])
time=list(emolt_sensor['TIME_LOCAL'])
yrday0=list(emolt_sensor['YRDAY0_LOCAL'])
temp=list(emolt_sensor['TEMP'])
depth1=list(emolt_sensor['DEPTH_I'])
	

	  time1,temp1,yrday01,sites1,depth=[],[],[],[],[]
	  for m in range(len(time)):
	      #if mindtime<=dt.datetime.strptime(str(time[m]),'%Y-%m-%d')<=maxdtime:
	      if date2num(mindtime)<=yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))<=date2num(maxdtime):
	      #if str(time[m])=='2012-01-01':
	        temp1.append(temp[m])
	        yrday01.append(yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d')))
	        sites1.append(sites2[m])
	        time1.append(date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))) 
	        depth.append(depth1[m])
	  #print len(temp1)     
	  return time1,yrday01,temp1,sites1,depth,'''

