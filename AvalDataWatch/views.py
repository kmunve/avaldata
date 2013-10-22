# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
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
    from AvalDataWatch.getprecipdata import get_precip_data
#     from AvalDataWatch.getwinddata import get_wind_data
    
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

def region(request):
    ti = datetime.timedelta(days=1)
    dt = datetime.datetime.now()-ti

    burl = r'ftp://ftp.met.no/users/dagrunvs/snow/'
    bstation = '53530_MIDTSTOVA'
    start_date= '20130901'
    curr_date = '{0}{1}{2}'.format(dt.year, dt.month, dt.day)
    fext = '.png'

    cro_vert_profile = '{0}{1}/{2}-VERTICAL-PROFILE-{3}-{4}-{5}-14.jpg'.format(burl,
                                                                              curr_date,
                                                                              bstation,
                                                                         dt.year,
                                                                         dt.month,
                                                                         dt.day-1)

    mep_aval_type = '{0}{1}/{2}-20130901-avalancheType{3}'.format(burl, curr_date, bstation, fext)
    mep_nat_risk = '{0}{1}/{2}-20130901-naturalRisk{3}'.format(burl, curr_date, bstation, fext)
    mep_acc_risk = '{0}{1}/{2}-20130901-accidentalRisk{3}'.format(burl, curr_date, bstation, fext)

    htmlresp = render(request, 'region.html',
        {'CRO_vert_profile': cro_vert_profile,
         'CRO_rho-profile': '',
         'CRO_lwc_profile': '',
         'CRO_gtype_profile': '',
         'MEP_aval_type': mep_aval_type,
         'MEP_nat_risk': mep_nat_risk,
         'MEP_acc_risk': mep_acc_risk
        })
    return htmlresp