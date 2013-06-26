'''
Created on 14. mai 2013

@author: kmu
'''

from urllib import urlencode
import urllib2
import json
import datetime

class UrlQuery(object):
    
    def __init__(self):
        self.server = ""
        
        self.servers = {"NVEChartServer": "http://h-web01.nve.no/chartserver/",
                        "RegObsAPI": "http://api.nve.no/hydrology/regobs/v0.8.7/Odata.svc/"}
        
        self.queryargument = {}
        
        self.filterargument = {}
        
        self.datestrformat = "%Y%m%dT%H%M"
        self.enddate = datetime.date.today()
        self.timeinterval = datetime.timedelta(days=1)
        self.startdate = self.enddate-self.timeinterval
        
        self.queryargument["time"]= "{0};{1}".format(self.startdate.strftime(self.datestrformat),
                                                     self.enddate.strftime(self.datestrformat))
        
        

    def set_startdate(self, sd):
        """
        Insert start date as string "yyyymmddThhmm"
        """
        pass



class NVEChartServerQuery(UrlQuery):
    
    def __init__(self):
        super(NVEChartServerQuery, self).__init__()
        self.server = self.servers['NVEChartServer']
        self.showdata = "ShowData.aspx?"
        self.showchart = "ShowChart.aspx?"
        
        self.queryargument = { "req": "getchart", "ver":1, "vfmt": "json" }
        """
        Changing the query argument:
        E.g. the output format from 'json' to 'XML'
        self.queryargument["vfmt"]="xml"
        """

    def _generate_queryargument(self, getChart=True):
        """
        Generates an url that requests data from NVE's chart server.
        Use getChart=False to receive data in json (default), xml or text. 
        """
        if getChart:
            self.UQ = self.server + self.showchart + urlencode(self.queryargument, True)
        else:
            self.UQ = self.server + self.showdata + urlencode(self.queryargument, True)
    
    
    def _generate_filterargument(self):
        da = ""
        for key, value in self.filterargument.iteritems():
            da += "{0}={1},".format(key, value)
        self.queryargument['chd'] = da[:-1]
            
            
    
    
    def precipitation(self,station_id, resolution_time="1:00"):
        """
        ds=htsre,id=23550.0,rt=1:00,mth=sum,cht=col,clr=blue
        self.queryargument[] =
        """
        self.filterargument['ds'] = 'htsre'
        self.filterargument['id'] = '{0}.0'.format(station_id)
        self.filterargument['rt'] = resolution_time
        self.filterargument['mth'] = 'sum'
        self.filterargument['cht'] = 'col'
        
        self._generate_filterargument()
        self._generate_queryargument()
        
        
        
class OdataQuery(object):
    """
    Should be the super class for RegobsQuery
    """
    pass
      
      
    
class RegobsQuery(UrlQuery):
    """
    http://api.nve.no/hydrology/regobs/v0.8.7/Odata.svc/
    AllRegistrationsV()?$filter=((
    (((cast(RegistrationTID,'Edm.Int32')) = 21) and 
    ((cast(GeoHazardTID,'Edm.Int32')) = 10)) and 
    ((cast(LangKey,'Edm.Int32')) = 1)) and
    (DtObsTime ge datetime'2013-05-12T10:04:38.0792551%2B02:00')) and 
    ((cast(ForecastRegionTID,'Edm.Int32')) = 129)
    
    
    """
    def __init__(self):
        super(RegobsQuery, self).__init__()
#         api_version = "v0.8.7"
        self.server_root = "http://api.nve.no/hydrology/regobs/v0.8.7/Odata.svc/"
        self.api_view = "" # used in child classes
        self.filter_str = "?$filter="
        
        self.query_options = {"$format":"json",}
        """
        Changing the query argument:
        E.g. the output format from 'json' to 'XML'
        self.query_options["$format"]="xml"
        """
        self.filter_options = []
        
        
    def _generate_queryargument(self):
        """
        Generates an url that requests data from NVE's chart server.
        Use getChart=False to receive data in json (default), xml or text. 
        """
        self.UQ = self.server_root + self.api_view + self.filter_str + "&"+ urlencode(self.query_options, True)
        self.UQ = self.UQ.replace(" ", "%20")
    
    
    def _generate_filterargument(self):
        for option in self.filter_options:
            self.filter_str += "{0} and ".format(option)
        self.filter_str = self.filter_str[:-5] # trim the last " and "
        
        
    def add_filter(self, fopt):
        self.filter_options.append(fopt)
        
            
    def update(self):
        self._generate_filterargument()
        self._generate_queryargument()
        
        
    def get_json_data(self):
        self.update()
        usock = urllib2.urlopen(self.UQ)#.encode("iso-8859-10"))    
        data = usock.read()
        usock.close()
        
        jdata = json.loads(data)
        return jdata['d']['results']


class RegistrationQuery(RegobsQuery):
    def __init__(self):
        super(RegistrationQuery, self).__init__()
        self.api_view = "AllRegistrationsV"
        
        
class SnowCoverQuery(RegobsQuery):
    def __init__(self):
        super(SnowCoverQuery, self).__init__()
        self.api_view = "SnowCoverObsV"
        
        
class AvalancheWarningQuery(RegobsQuery):
    def __init__(self):
        super(AvalancheWarningQuery, self).__init__()
        self.api_view = "AvalancheWarning2V"
        
        
        
        
        