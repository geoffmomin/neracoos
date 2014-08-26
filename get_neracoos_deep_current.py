# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 12:53:09 2013

@author: hxu
"""

####################################################
#get layer current data from neracoos OpenDap,generate a dataframe which includes time,lat,lon,u,v and depth.
#then ,plots a graph
#Functions uses: get_neracoos_ctl,get_id_s_id_e_id_max_url,get_neracoos_deep_current_data,depth_select_ADCP
#input values: datetime period,the mooring type, the name of mooring site,layer depth
#output values: a data frame 
####################################################
from matplotlib.dates import date2num, num2date
import datetime as dt

import sys
import matplotlib.pyplot as plt
import numpy as np
from pandas import *
pydir='../'
sys.path.append(pydir)
from neracoos_def import get_neracoos_ctl,get_id_s_id_e_id_max_url,get_neracoos_deep_current_data,depth_select_ADCP
from get_neracoos_ctl import get_neracoos_ctl_py

inputfilename='./get_neracoos_ctl.txt'
if inputfilename[-2:]=='py':
    mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites=get_neracoos_ctl_py()
else:
    
    mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites=get_neracoos_ctl(inputfilename) #get input from input file
model='doppler'   
sdtime_n=date2num(mindtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of start time
edtime_n=date2num(maxdtime)-date2num(dt.datetime(1858, 11,  17, 0, 0)) #get number type of end time
depths,site_d,depth_index=depth_select_ADCP(sites,i_mindepth,i_maxdepth)
for index_site in range(len(site_d)):
    url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.historical.nc?'     
    id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
    if mintime=='':   
        histvsreal='1' #"histvsreal" can help us judge if this  site has historical data.
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.nc?'     
        id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
        print 'realtime from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))
    else:
        histvsreal=''
        print 'historical from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))
    if id_e0<>'':  
      (period_str,current_all)=get_neracoos_deep_current_data(url,id_s,id_e0,id_max_url,depth_index[index_site]) #get data from web neracoos      
      df = DataFrame(np.array(current_all),index=period_str,columns=['u','v','depth'])
    else:
        print "According to your input, there is no data here"    
    if histvsreal<>'1':
      if   maxtime<edtime_n: #make sure if we need a realtime data
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.nc?'     
        id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
        if id_e<>'':     
           (period_str,current_all)=get_neracoos_deep_current_data(url,id_s,id_e,id_max_url,depth_index[index_site])  #get data from web neracoos
           print 'realtime from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))
           #df = DataFrame(np.array(depth_temp),index=period_str,columns=['                depth','      temp']).append(df)
           if id_e0=='':
              df = DataFrame(np.array(current_all),index=period_str,columns=['u','v' ,'depth'])
           else:              
              df = df.append(DataFrame(np.array(current_all),index=period_str,columns=['u','v','depth' ])) #combine them in DataFrame 
    
    df_uv=df.ix[:,[0,1]]  #get u,v from df    
    df_uv.plot(title=site_d[index_site]+'_'+depths[index_site]+'m')
    plt.gcf().autofmt_xdate()
    df.to_csv('current_d_'+site_d[index_site]+'.csv') #save it to a csv file
plt.show()
