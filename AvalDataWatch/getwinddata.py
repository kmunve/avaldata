# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
'''
Created on 8. mai 2013

@author: kmu
'''

import urllib2
import json
import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



"""
Chart showing wind speed from Mannen

http://h-web01.nve.no/chartserver/
ShowChart.aspx?req=getchart&ver=1.0&
time=-31;0&
chd=ds=htsre,id=61410.16,rt=1:0,mth=inst

- id = stationID.timeseriesID

- time can either be -"day sbefore today";"days after today" or between two dates "date as yyyymmddThhmm";"date as yyyymmddThhmm" 

Wind speed data from Mannen

http://h-web01.nve.no/chartserver/ # defines server
ShowData.aspx? # defines function(?)
req=getchart& # defines request
ver=1.0& # defines version number
vfmt=json& # defines output format
time=20130422T0000;20130521T0000& # defines time interval
chs=10x10& # defines chart size
lang=no& # defines language
chlf=desc& # defines chart legend format
chsl=0;+0& # marks an area dependent on start and end dates/times 
chd=ds=htsre,da=29,id=61410.16,rt=1:00,cht=line,mth=inst| # ???
    ds=htsry,id=metx[61410;16].6038,mth=inst,rt=1:00,cht=line&nocache=0.33931976436234856 # ???
    
    
    

"""
met_no_stations={'Filefjell':54710,
                 'Sk�bu':13655}

def __windrose():
    """ http://sourceforge.net/projects/windrose/ """
    pass

def json_date_as_datetime(jd):
    """
    From http://stackoverflow.com/questions/5786448/date-conversion-net-json-to-iso/5787129#5787129
    """
    sign = jd[-7]
    if sign not in '-+' or len(jd) == 13:
        millisecs = int(jd[6:-2])
    else:
        millisecs = int(jd[6:-7])
        hh = int(jd[-7:-4])
        mm = int(jd[-4:-2])
        if sign == '-': mm = -mm
        millisecs += (hh * 60 + mm) * 60000
    return datetime.datetime(1970, 1, 1) \
        + datetime.timedelta(microseconds=millisecs * 1000)
        
        
def get_wind_data(verbose=False):
    url = """http://h-web01.nve.no/chartserver/ShowData.aspx?req=getchart&ver=1.0&vfmt=json&time=20130506T0000;20130509T0000&chs=1056x512&lang=no&chlf=desc&chsl=0;+0&chd=ds=htsre,da=29,id=25110.16,rt=1:00,cht=line,mth=inst|ds=htsry,id=metx[25110;16].6038,mth=inst,rt=1:00,cht=line&nocache=0.9582291734404862"""
    

    usock = urllib2.urlopen(url)#.encode("iso-8859-10"))    
    data = usock.read()
    usock.close()
    
    jdata = json.loads(data)
    res_list = jdata[0]['SeriesPoints']
    
    try:
        res_keys = res_list[0].keys()
        
        legend_text = jdata[0]['LegendText']
        
        dt = []
        windspeed = []
        for item in res_list:
            dt.append( json_date_as_datetime(item['Key']) )
            windspeed.append(item['Value'])
        
        img_src = './windspeed.png'
        #plt.plot(dt, windspeed)
        plt.savefig(img_src)
        
        
    except IndexError:
        print "#####################"
        print "# No data returned. #"
        print "#####################"
    
    if verbose:
        print url
        print usock.headers
        print res_keys
        print "#items:", len(res_list)
        print jdata[0]['LegendText']
        print windspeed
        plt.show()
        
    return legend_text, dt, windspeed, img_src    
        

if __name__ == '__main__':
    get_wind_data(verbose=True)