# -*- coding: utf-8 -*-
"""
Created on Thu May 02 08:27:24 2013

@author: Huanxin
"""
from matplotlib.dates import date2num, num2date
import datetime as dt

import sys
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy as np
from pydap.client import open_url
from pandas import *
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
Dataset: F01.sbe37.historical.50m.nc
lat, 44.0556001811715
lon, -68.9967173062176
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
pydir='../'

sys.path.append(pydir)

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
def get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n): # get id of start time and end time
        id_max_url,maxtime,mintime=get_neracoos_ctl_id_max(url)
        if sdtime_n<mintime:
            id_s=0
            if edtime_n<mintime:
                id_e=''
            if mintime<=edtime_n<=maxtime:
                id_e=get_neracoos_ctl_id(url,edtime_n)
            else:
                id_e=id_max_url
        if mintime<=sdtime_n<=maxtime:
            id_s=get_neracoos_ctl_id(url,sdtime_n)
            if mintime<=edtime_n<=maxtime:
                id_e=get_neracoos_ctl_id(url,edtime_n)
            else:
                id_e=id_max_url
        else:
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
        if sites[k]=='A01' or 'B01' or 'E01' or 'E02' or 'F02' or 'I01':
            
            depth_box=[1,20,50]
            depth_index=[i for i,x in enumerate(depth_box) if i_maxdepth >= x >=i_mindepth]
            print depth_index
            for i in depth_index:
                depths.append(str(depth_box[i]))
                site_d.append(sites[k])
        if sites[k]=='D02':
            depth_box=[1,2,10]
            depth_index=get_depth_index(i_mindepth,i_maxdepth,depth_box)
            for i in depth_index:
                depths.append(str(depth_box[depth_index]))
                site_d.append(sites[k])
        if sites[k]=='F02':
            depth_box=[1]
            depth_index=get_depth_index(i_mindepth,i_maxdepth,depth_box)
            for i in depth_index:
                depths.append(str(depth_box[depth_index]))
                site_d.append(sites[k])
        if sites[k]=='M01':
            depth_box=[1,20,50,100,150,200,250,283]
            depth_index=get_depth_index(i_mindepth,i_maxdepth,depth_box)
            for i in depth_index:
                depths.append(str(depth_box[depth_index]))
                site_d.append(sites[k])
        if sites[k]=='N01':
            depth_box=[1,20,50,100,150,180]
            depth_index=get_depth_index(i_mindepth,i_maxdepth,depth_box)
            for i in depth_index:
                depths.append(str(depth_box[depth_index]))
                site_d.append(sites[k])
        '''
        else:
            print sites[k]+' is not here,please check  your input '
        '''
    return depths,site_d
def get_neracoos_data(url,id_s,id_e): #get data from neracoos.
          url=url+'temperature[0:1:'+id_max_url+'][0:1:0][0:1:0][0:1:0]'
          database=open_url(url)['temperature'][int(id_s):int(id_e)]
          #lat=database['lat']
          #lon=database['lon']
          depth=database['depth']
          period=database['time']
          temp=database['temperature']
          temp=temp[0:].tolist()
          period=num2date(period[0:]+date2num(dt.datetime(1858, 11, 17, 0, 0)))
          return depth[0],temp,period
 
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
    id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
    if mintime=='':   
        judgement='1' #"judgement" can help us judge if this  site has historical data.
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.'+depths[index_site]+'m.nc?'     
        id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
    else:
        judgement=''
    if id_e<>'':  
      (depth,temp,period)=get_neracoos_data(url,id_s,id_e) #get data from web neracoos 
       #convert array to 1d list
      for i in range(len(period)):
        period_str.append(dt.datetime.strftime(period[i],'%Y-%m-%d-%H-%M'))
        temp_list.append(temp[i][0][0][0])
        depth_list.append(depth)     
    else:
        print "According to your input, there is no data here"
    
    if judgement<>'1':
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.'+depths[index_site]+'m.nc?'     
        id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
        if id_e<>'':     
           (depth,temp,period)=get_neracoos_data(url,id_s,id_e)  #get data from web neracoos 
           #convert array to 1d list
           for i in range(len(period)): #convert format to list
             period_str.append(dt.datetime.strftime(period[i],'%Y-%m-%d-%H-%M'))
             temp_list.append(temp[i][0][0][0])
             depth_list.append(depth)     
    '''
    df.plot(title=index_site+'_'+model+'\ndepth='+str(depth[0])+'\nlat='+str(lat[0])+'\nlon='+str(lon[0]))
    plt.show()
    '''
    depth_temp=[]   #convert row to line
    for k in range(len(depth_list)):
        depth_temp.append([depth_list[k],temp_list[k]])
    df = DataFrame(np.array(depth_temp),index=period_str,columns=['                depth','      temp']) #combine them in DataFrame    
    #df = DataFrame(depth_list,temp_list, index=period_str,columns=['depth', 'temp']) #combine them in DataFrame
    df.plot()
    df.to_csv('temp_'+site_d[index_site]+'_'+str(depth)) #save it to a csv file
    print '1'
plt.show()




























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

