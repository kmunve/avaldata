'''
Created on 8. mai 2013

@author: kmu
'''
import urllib2
import json
import datetime

from base.urlquery import UrlQuery
from base.timeseries import PrecipitationTS 


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
        
        
def get_precip_data(verbose=False):
#     url = """http://h-web01.nve.no/chartserver/ShowData.aspx?req=getchart&ver=1.0&vfmt=json&time=20130504T0000;20130506T0000&chs=10x10&lang=no&chlf=none&chsl=0;+0&chd=ds=htsre,da=29,id=25100.0,rt=1,cht=col,mth=sum,timeo=6:0|ds=htsry,id=metx[25100;0].6001,mth=sum,rt=1,cht=col&nocache=0.20784913911484182"""
    
    url = UrlQuery()

    usock = urllib2.urlopen(url.UQ)#.encode("iso-8859-10"))    
    data = usock.read()
    usock.close()
    
    jdata = json.loads(data)
    res_list = jdata[0]['SeriesPoints']
    
    try:
        res_keys = res_list[0].keys()
        
        
        precip = PrecipitationTS()
        precip.legend = jdata[0]['LegendText']
        for item in res_list:
            precip.dates.append( json_date_as_datetime(item['Key']) )
            precip.values.append(item['Value'])
            
        precip.calc_three_days_sum()
            
        
    except IndexError:
        print "#####################"
        print "# No data returned. #"
        print "#####################"
    
    if verbose:
        print url
        print usock.headers
        print res_keys
        print "#items:", len(res_list)
        
    return precip   
        

if __name__ == '__main__':
    get_precip_data(verbose=True)