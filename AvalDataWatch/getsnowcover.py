# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
'''
Doc...

:Author: kmu
:Created: 23. june 2013
'''
from base import urlquery
from base import timeseries

"""
Tested on Python 2.6.6 and Python 2.7.2

Module 'timeseries' requires the additional Python packages 'numpy' and 'matplotlib'.
Though they are not required to run this specific example and can be commented out in timeseries.py.
"""


def getSnowCover():
    uq = urlquery.SnowCoverQuery()
    
    uq.add_filter("DtObsTime ge datetime'2012-09-01T00:00:00'")
    uq.add_filter("LangKey eq 1")
    
    res = uq.get_json_data()
    
    print uq.UQ # can be copied to the browser's address field to view the full result of the query
    
    shTS = timeseries.RegObsTS()
    
    for item in res:
        if item['CriticalLayerName'] == "Rimlag ":
            shTS.values.append(item['CriticalLayerName'])
            shTS.dates.append(item['DtObsTime'])
            shTS.UTMZone.append(item['UTMZone'])
            shTS.UTMEast.append(item['UTMEast'])
            shTS.UTMNorth.append(item['UTMNorth'])
            shTS.set_regid(item['RegID'])
    
    
    shTS.json_date_as_datetime()
    print shTS
    
    
if __name__ == '__main__':
    getSnowCover()