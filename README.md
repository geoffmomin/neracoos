neracoos
========

This program is used for extracting NERACOOS  data . The user can extract data based on time period, geographic range, depth range, and/or type, name of sites.

After running this program, you can obtain a file of data in same folder as this program. The file is named according to the date and time it was created.

How to use it:

1,Modify the control file 'getneracoos_ctl.txt' to what you want before you run it (see example control file below).

<pre>
[1 1 1 1]
[2012,1,1,0,0;2012,4,14,23,59]
[met]   #like met,sbe37,sbe16,aanderaa
[18,21]  
[A01]   # like  A01,F01


The first line represent index of the following 5 line,'1' means picking,'0' means not.
the 2nd line represent the period of date
the 3rd line represent the mooring type ,'met' for wind,'sbe' for temperature and salinity, 'aanderaa' for current
the 4th line represent the range depth of sensor,  frist min,seconed max. (Ignored in wind case.) 
the 5th line represent the mooring, use "," to split

</pre>

2, Run 'get_neracoos_main.py' in either ipython, spyder, or whatever is your favorite Python environment.
    4 options will be showed:<br>

        1= get temperture data  
        2= get wind data
        3= get current surface data 
        4= get current layers data

3, select an option(input index number). 


4, the output files should be like data files or graphs.
<pre>
	              depth  temp   salinity
2012-01-01-00-00	20	7.93	32.05
2012-01-01-00-30	20	7.95	32.06
2012-01-01-00-59	20	7.95	32.06
2012-01-01-01-30	20	7.92	32.06
2012-01-01-02-00	20	7.9	    32.05
2012-01-01-02-29	20	7.91	32.05
2012-01-01-03-00	20	7.96	32.06
2012-01-01-03-30	20	7.91	32.06
2012-01-01-03-59	20	7.9	    32.05
2012-01-01-04-30	20	7.89	32.05
2012-01-01-05-00	20	7.9	    32.05
2012-01-01-05-29	20	7.92	32.07

</pre>


