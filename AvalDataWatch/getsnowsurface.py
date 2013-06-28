# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
'''
Doc...

:Author: kmu
:Created: 28. june 2013
'''
from base import urlquery
from base import timeseries

"""
Tested on Python 2.6.6 and Python 2.7.2

Module 'timeseries' requires the additional Python packages 'numpy' and 'matplotlib'.
Though they are not required to run this specific example and can be commented out in timeseries.py.
"""


def getSnowSurfaceType():
    """
    Returns all observations of surface hoar on the snow surface.
    """
    uq = urlquery.SnowSurfaceQuery()
    
    uq.add_filter("DtObsTime ge datetime'2012-09-01T00:00:00'")
    uq.add_filter("LangKey eq 1")
    
    res = uq.get_json_data()
    
    print uq.UQ # can be copied to the browser's address field to view the full result of the query
    
    shTS = timeseries.SnowSurfaceTS()

    for item in res:
        """
        Just exchange "SH Overflaterim/hulromsrim" by:
        "IF Is og skare"
        "MFcr Gjenfroset smeltelag"
        "MF Smelteomdannede korn"
        to retrieve infroamtion about crusts.
        """
        if item['SnowSurfaceName'] == "SH Overflaterim/hulromsrim":  
            shTS.values.append(item['SnowSurfaceName'])
            shTS.dates.append(item['DtObsTime'])
            shTS.snowdepth.append(item['SnowDepth'])
            shTS.lwq.append(item['SurfaceWaterContentName'])
            shTS.UTMZone.append(item['UTMZone'])
            shTS.UTMEast.append(item['UTMEast'])
            shTS.UTMNorth.append(item['UTMNorth'])
    
    shTS.json_date_as_datetime()
    print shTS


def getSnowSurfaceWetness():
    """
    Returns all observations of a wet snow surface.
    """
    uq = urlquery.SnowSurfaceQuery()
    
    uq.add_filter("DtObsTime ge datetime'2012-09-01T00:00:00'")
    uq.add_filter("LangKey eq 1")
    
    res = uq.get_json_data()
    
    print uq.UQ # can be copied to the browser's address field to view the full result of the query
    
    shTS = timeseries.SnowSurfaceTS()

    for item in res:
        """
        Just exchange "SH Overflaterim/hulromsrim" by:
        "IF Is og skare"
        "MFcr Gjenfroset smeltelag"
        "MF Smelteomdannede korn"
        to retrieve infroamtion about crusts.
        """
        wetness_l= [u'Fuktig',
                    u'Våt',
                    u'Meget våt',
                    u'Sørpe']
        
        if item['SurfaceWaterContentName'] in wetness_l:  
            shTS.values.append(item['SnowSurfaceName'])
            shTS.dates.append(item['DtObsTime'])
            shTS.snowdepth.append(item['SnowDepth'])
            shTS.lwq.append(item['SurfaceWaterContentName'])
            shTS.UTMZone.append(item['UTMZone'])
            shTS.UTMEast.append(item['UTMEast'])
            shTS.UTMNorth.append(item['UTMNorth'])
    
    shTS.json_date_as_datetime()
    print shTS
    
    
if __name__ == '__main__':
    getSnowSurfaceType()
    print "####################################################################"
    getSnowSurfaceWetness()