# -*- coding:iso-8859-10 -*-
__author__ = 'kmu'

from AvalDataWatch.base import urlquery
from AvalDataWatch.base import timeseries

def generate_url():
    uq = urlquery.RegistrationQuery()

    uq.add_filter("DtObsTime ge datetime'2012-12-15T00:00:00'")
    uq.add_filter("DtObsTime le datetime'2013-01-01T00:00:00'")
    uq.add_filter("LangKey eq 1")
    uq.add_filter("ForecastRegionTID eq 119")

    #uq.update()
    #print uq.UQ

    res = uq.get_json_data()

    print uq.UQ # can be copied to the browser's address field to view the full result of the query

    TS = timeseries.RegObsTS()

    for item in res:
        TS.values.append(item['RegID'])
        TS.set_regid(item['RegID'])


    TS.json_date_as_datetime()
    print TS


if __name__ == '__main__':
    generate_url()