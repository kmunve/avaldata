'''
Created on 8. mai 2013

@author: kmu
'''
from django.http import HttpResponse
from django.shortcuts import render

import datetime

def pgtitle(request):
    return HttpResponse("Avalanche Weather Watch")


def precip(request):
    from AvalWeatherWatch.getprecipdata import get_precip_data
#     from AvalWeatherWatch.getwinddata import get_wind_data
    
    precip = get_precip_data()

    htmlresp = render(request, 'aws_data.html',
                      {'TSname': precip.name,
                       'TSunit': precip.unit,
                       'TSlegend': precip.legend,
                       'TSzipdata': zip(precip.dates, precip.values),
                       'three_days_sum': precip.three_days_sum,
                       'update_date': datetime.datetime.now()}
                      )
    return htmlresp
    

def mscharts(request):
    htmlresp = render(request,'base.html', {'coverimg': 'http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&lang=no&time=-3;0&chd=ds=htsre,id=23550.17,rt=1:0,mth=inst,clr=black,drwd=2|ds=htsre,id=23550.0,rt=1:00,mth=sum,cht=col,clr=blue|ds=htsre,id=54710.0,rt=1:00,mth=sum,cht=col,clr=red|ds=htsre,id=13655.0,rt=1:00,mth=sum,cht=col'})
    return htmlresp