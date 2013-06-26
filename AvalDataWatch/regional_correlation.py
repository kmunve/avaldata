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
import numpy as np
import pylab as plt
# Own
from base.urlquery import AvalancheWarningQuery
from base.timeseries import DangerLevelTS

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


def get_correlation(region_1, region_2):
    uq = AvalancheWarningQuery()
    
    uq.add_filter("ForecastRegionTID eq {0}".format(region_1))
    uq.add_filter("LangKey eq 1")
    
    data = uq.get_json_data()
    
    dl_1 = DangerLevelTS()
    
    for item in data:
        dl_1.values.append(item['AvalancheDangerTID'])
        dl_1.dates.append(item['DtValidFromTime'])
    
    dl_1.json_date_as_datetime()
    dl_1.clean_dates()
    
    uq = AvalancheWarningQuery()
    
    uq.add_filter("ForecastRegionTID eq {0}".format(region_2))
    uq.add_filter("LangKey eq 1")
    
    data = uq.get_json_data()
    
    dl_2 = DangerLevelTS()
    
    for item in data:
        dl_2.values.append(item['AvalancheDangerTID'])
        dl_2.dates.append(item['DtValidFromTime'])
    
    dl_2.json_date_as_datetime()
    dl_2.clean_dates()
    
    cc = np.correlate(dl_1.values, dl_2.values, mode='valid')
    print cc
    coef = np.corrcoef(dl_1.values, dl_2.values)
    print coef
    
    dl_diff = dl_1.values - dl_2.values
    print np.float(np.size(np.where(dl_diff == 0))) / np.float(len(dl_diff))
    
    plt.plot(dl_diff)
#     plt.hold(True)
#     plt.plot(dl_1.values)
#     plt.plot(dl_2.values)
    plt.show()
    
    """
    Do an intercomparison btw all regions
    """
    
if __name__ == '__main__':
    get_correlation(119, 120)