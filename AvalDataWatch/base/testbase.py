# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
'''
Doc...

:Author: kmu
:Created: 14. mai 2013
'''

''' Imports '''
# Built-in

# Additional

# Own
import urlquery
import timeseries


def test_urlquery():
    uq = urlquery.NVEChartServerQuery()
    uq.queryargument["time"] = "-3;0"
    uq.precipitation(13655)
    print uq.UQ

def test_regobsquery(region_id):
    uq = urlquery.AvalancheWarningQuery()
    
    uq.query_options["$orderby"] = "DtObsTime desc"
    
    uq.add_filter("ForecastRegionTID eq {0}".format(region_id))
    uq.add_filter("LangKey eq 1")
    
    res = uq.get_json_data()
    print uq.UQ
    print res
    
def __test_getSnowCover():
    uq = urlquery.RegistrationQuery()
    
    uq.add_filter("RegistrationTID eq 23")
    # uq.add_filter("RegistrationName eq 'SnowCoverObs'")
    uq.add_filter("DtObsTime ge datetime'2012-09-01T00:00:00'")
    uq.add_filter("LangKey eq 1")
    
    res = uq.get_json_data()
    print uq.UQ
    #    print res
    
    shTS = timeseries.TimeSeries()
    
    for item in res:
        if item['TypicalValue2'] == "Rimlag ":
            shTS.values.append(item['TypicalValue2'])
            shTS.dates.append(item['DtObsTime'])
    
    
    shTS.json_date_as_datetime()
    # for d, v in zip(shTS.dates, shTS.values):
    #     print d, v
    
def test_getSnowCover():
    uq = urlquery.SnowCoverQuery()
    
    uq.add_filter("DtObsTime ge datetime'2012-09-01T00:00:00'")
    uq.add_filter("LangKey eq 1")
    
    res = uq.get_json_data()
    print uq.UQ
    
    shTS = timeseries.RegObsTS()
    
    for item in res:
        if item['CriticalLayerName'] == "Rimlag ":
            shTS.values.append(item['CriticalLayerName'])
            shTS.dates.append(item['DtObsTime'])
            shTS.UTMZone.append(item['UTMZone'])
            shTS.UTMEast.append(item['UTMEast'])
            shTS.UTMNorth.append(item['UTMNorth'])
    
    
    shTS.json_date_as_datetime()
    print shTS
    
    
if __name__ == '__main__':
#     test_urlquery()
#    test_regobsquery(123)
    test_getSnowCover()