# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:27:11 2013

@author: hxu
"""
import datetime as dt
def get_neracoos_ctl_py():
  select=[0,1,1,1]
  dtime='[2002,9,1,0,0;2013,9,10,23,59]'
  model=['sbe37']   #like met,sbe37,sbe16,aanderaa
  idepth=[30,90]   #depth range
  sites=['B01']   # like  A01,F01


  select1=select[0]
  select2=select[1]
  select3=select[2]

   
  if select1 ==1:# get time period
   
       dtime=dtime[0:dtime.index(']')].strip('[').split(';')
       mindtime=dt.datetime.strptime(dtime[0],'%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime(dtime[1],'%Y,%m,%d,%H,%M') 
  else:
       
       mindtime=dt.datetime.strptime('2001,1,1,0,0','%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime('2014,1,1,0,0','%Y,%m,%d,%H,%M') #w
  #get mooring model
  model=model[0]
  if select2 ==1: #get depth_range
       i_mindepth=float(idepth[0])
       i_maxdepth=float(idepth[1])
  else:
       i_mindepth=0
       i_maxdepth=2000
     
       
  if select3 ==1: #get sites
       sites=sites
  else:
       sites=''
       
  return  mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites

#the 2nd line represent the period of date
#the 3rd line represent the range depth of sensor,  frist min,seconed max. (Ignored in wind case.) 
#the 4th line represent the mooring type ,'met' for wind,'sbe' for temperature and salinity, 'aanderaa' for current
#the 5th line represent the mooring, use "," to split
