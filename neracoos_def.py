# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:32:46 2013

@author: hxu
"""
from matplotlib.dates import date2num, num2date
import datetime as dt

import matplotlib.mlab as ml
import numpy as np
from pydap.client import open_url
from pandas import *

def get_neracoos_ctl(inputfilename):# get data input from a txt file
   f=open(inputfilename)  
   select=f.readline()
   select=select[0:select.index(']')].strip('[').split(' ')
   select1=select[0]
   select2=select[1]
   select3=select[2]
   
   if select1 =='1':# get time period
       dtime=f.readline()
       dtime=dtime[0:dtime.index(']')].strip('[').split(';')
       mindtime=dt.datetime.strptime(dtime[0],'%Y,%m,%d,%H,%M')
       maxdtime=dt.datetime.strptime(dtime[1],'%Y,%m,%d,%H,%M') 
   else:
       dtime=f.readline()
       
   if select2 =='1': #get depth_range
       idepth=f.readline()
       idepth=idepth[0:idepth.index(']')].strip('[').split(',')
       i_mindepth=float(idepth[0])
       i_maxdepth=float(idepth[1])
   else:
       i_mindepth=0
       i_maxdepth=2000
       dtime=f.readline()
       
   model=f.readline() #get mooring model
   model=model[0:model.index(']')].strip('[')    
       

       
   if select3 =='1': #get sites
       site=f.readline()
       sites=site[0:site.index(']')].strip('[').split(',') 
   else:
       site=f.readline()
       site=''
       
   return  mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites
def get_neracoos_ctl_id(url,datetime_wanted): #accroding time you input,get a index of that
    
        dtime=open_url(url+'?time')
        #dd=dtime['time']
        ddd=[]
        for i in list(dtime['time']):
            i=round(i,7)
            ddd.append(i)
        #print "This option has data from "+str(num2date(dd[0]+date2num(datetime.datetime(2001, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(datetime.datetime(2001, 1, 1, 0, 0)))) 
        #print 'This option has data from '+num2date(dd[0]).strftime("%B %d, %Y")+' to '+num2date(dd[-1]).strftime("%B %d, %Y")          
        f = lambda a,l:min(l,key=lambda x:abs(x-a)) #match datetime_wanted
        datetime_wanted=f(datetime_wanted, ddd)
        id=[i for i,x in enumerate(ddd) if x == datetime_wanted]       
        #id=ml.find(np.array(ddd)==round(datetime_wanted,7))
        #id_max=ml.find(np.array(ddd)==round(max(ddd),7))
        for i in id:
          id=str(i) 
        #print 'codar id is  '+id

        return id
def get_neracoos_ctl_id_max(url):  #get the max datetime , min datetime and index of max datetime
        try:
            dtime=open_url(url+'?time')
        except:
            print 'no data that you want in this '+url
            
            return '','',''
        ddd=[]
        for i in list(dtime['time']):
            i=round(i,7)
            ddd.append(i)
        #print "This option has data from "+str(num2date(dd[0]+date2num(datetime.datetime(2001, 1, 1, 0, 0))))+" to "+str(num2date(dd[-1]+date2num(datetime.datetime(2001, 1, 1, 0, 0)))) 
        #print 'This option has data from '+num2date(dd[0]).strftime("%B %d, %Y")+' to '+num2date(dd[-1]).strftime("%B %d, %Y")  
                
        #id_max=[m for m,x in enumerate(ddd) if x == 1]     
        id_max=ml.find(np.array(ddd)==round(max(ddd),7)) # match the lastest datetime
        for i in id_max:
          id_max=str(i) 
        #print 'codar id is  '+id

        return id_max,max(ddd),min(ddd)
def get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n): # get id of start time and end time, and get max datetime , min datetime and index of max datetime from get_neracoos_ctl_id
        id_max_url,maxtime,mintime=get_neracoos_ctl_id_max(url)
        if sdtime_n<mintime:
            id_s=0
            if edtime_n<mintime:
                id_e=''
            if mintime<=edtime_n<=maxtime:
                id_e=get_neracoos_ctl_id(url,edtime_n)
            if edtime_n>maxtime:
                id_e=id_max_url
        if mintime<=sdtime_n<=maxtime:
            id_s=get_neracoos_ctl_id(url,sdtime_n)
            if mintime<=edtime_n<=maxtime:
                id_e=get_neracoos_ctl_id(url,edtime_n)
            if edtime>maxtime:
                id_e=id_max_url
        if mintime>maxtime:
            id_s=''
            id_e=''
        
        return id_s,id_e,id_max_url,maxtime,mintime
def get_depth_index(i_mindepth,i_maxdepth,depth_box): #this function works for "depth_select",According depth range you input, get depth which we have
    depth_index1=ml.find(depth_box<=i_maxdepth)
    depth_index2=ml.find(depth_box>=i_mindepth)
    depth_index=list(set(depth_index2).intersection(set(depth_index1)))
    return depth_index
'''
def depth_add(depth_box):
   depth_index=ml.find(i_mindepth<=depth_box<=i_maxdepth)
   for i in depth_index:
       depths.append(depth_box[depth_index])
   return depths
'''
def depth_select(sites,i_mindepth,i_maxdepth): #select depth which we have in web . 
    depths=[]
    site_d=[]
    for k in range(len(sites)):
        if sites[k]=='A01' or 'B01' or 'E01' or 'E02' or 'F01' or 'I01':
            
            depth_box=[1,20,50]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth] #split sites in different depth
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='D02':
            depth_box=[1,2,10]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='F02':
            depth_box=[1]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='M01':
            depth_box=[1,20,50,100,150,200,250,283]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='N01':
            depth_box=[1,20,50,100,150,180]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        '''
        else:
            print sites[k]+' is not here,please check  your input '
        '''
    return depths,site_d
def get_neracoos_data(url,id_s,id_e,id_max_url): #get data from neracoos.
          url=url+'temperature[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0]'
          database=open_url(url)['temperature'][int(id_s):int(id_e)]
          lat=database['lat']
          lat=round(lat[0],2)
          lon=database['lon']
          lon=round(lon[0],2)
          depth=database['depth']
          period=database['time']
          temp=database['temperature']
          temp=temp[0:].tolist()
          period=num2date(period[0:]+date2num(dt.datetime(1858, 11, 17, 0, 0)))
          period_str,depth_temp=[],[]
    
          for i in range(len(period)): #convert format to list
             period_str.append(dt.datetime.strftime(period[i],'%Y-%m-%d-%H-%M'))
             #temp_list.append(temp[i][0][0][0])
             #depth_list.append(int(depth))  
             depth_temp.append([round(depth[0],1),round(temp[i][0][0][0],2),lat,lon])
          return period_str,depth_temp