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
from AvalDataWatch.base.urlquery import AvalancheWarningQuery
from AvalDataWatch.base.timeseries import DangerLevelTS

RegionIDs = {"": 107,
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
             "": 129,}


def get_danger_level(region_id):
    uq = AvalancheWarningQuery()
    
    uq.add_filter("ForecastRegionTID eq {0}".format(region_id))
    uq.add_filter("LangKey eq 1")
    
    data = uq.get_json_data()
    
    dl = DangerLevelTS()
    
#     region_name = data[0]['ForecastRegionName']
#     region_id = data[0]['ForecastRegionTID']
#     period_start = json_date_as_datetime(data[0]['DtValidFromTime'])
#     period_end = json_date_as_datetime(data[-1]['DtValidFromTime'])
#     
#     plot_title = "%i %s - %s to %s" % (region_id, region_name,
#                                        period_start.date(), period_end.date())
    
    for item in data:
        dl.values.append(item['AvalancheDangerTID'])
        dl.dates.append(item['DtValidFromTime'])
    
    dl.json_date_as_datetime()
    dl.clean_dates()

    dl.bar_plot(title=data[0]['ForecastRegionName'])
    

    
if __name__ == '__main__':
    get_danger_level(122)