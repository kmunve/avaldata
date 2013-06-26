# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
'''
Doc...

:Author: kmu
:Created: 15. mai 2013
'''

''' Imports '''
# Built-in

# Additional

# Own
from base.urlquery import AvalancheWarningQuery
from base.timeseries import DangerLevelTS

RegionIDs = {"Alta": 106,
             "Kåfjord": 107,
             "": 108,
             "": 109,
             "": 110,
             "": 111,
             "": 112,
             "": 113,
             "": 114,
             "": 115,
             "": 116,
             "": 117,
             "": 118,
             "": 119,
             "": 120,
             "": 121,
             "Sogn": 122,
             "": 123,
             "": 124,
             "": 125,
             "": 126,
             "": 127,
             "": 128,
             "Tamokdalen": 129,}


def get_danger_level(region_id):
    uq = AvalancheWarningQuery()
    
    uq.add_filter("ForecastRegionTID eq {0}".format(region_id))
    uq.add_filter("LangKey eq 1")
    
    data = uq.get_json_data()
    
    dl = DangerLevelTS()
    
    for item in data:
        dl.values.append(item['AvalancheDangerTID'])
        dl.dates.append(item['DtValidFromTime'])
    
    dl.json_date_as_datetime()
    dl.clean_dates()

    dl.bar_plot(title=unicode.encode(data[0]['ForecastRegionName'], 'utf-8'))
    
    
def make_report():
    
    for i in range(106,130):
        print "Processing region %i..." % i
        get_danger_level(i)
    
if __name__ == '__main__':
    # get_danger_level(107)
    make_report()