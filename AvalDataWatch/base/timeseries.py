# -*- coding:iso-8859-10 -*-
__doc_format__ = "reStructuredText"
'''
Created on 14. mai 2013

@author: kmu
'''

''' Imports '''
# Built-in
import datetime
# Additional
import numpy as np
#import pylab as plt
# Own

class TimeSeries(object):
    
    def __init__(self):
        self.dates = []
        self.values = []
        self.legend = ""
        self.unit = ""
        self.name = "" # defines the name of the entity 
        
    
    def __str__(self):
        if len(self.values) == 0:
            return "Empty time series"
        else:
            for d, v in zip(self.dates, self.values):
                return "{0} : {1}".format(d, v)
            
            
    def json_date_as_datetime(self):
        """
        From http://stackoverflow.com/questions/5786448/date-conversion-net-json-to-iso/5787129#5787129
        """
        for index,jd in enumerate(self.dates):
            sign = jd[-7]
            if sign not in '-+' or len(jd) == 13:
                millisecs = int(jd[6:-2])
            else:
                millisecs = int(jd[6:-7])
                hh = int(jd[-7:-4])
                mm = int(jd[-4:-2])
                if sign == '-': mm = -mm
                millisecs += (hh * 60 + mm) * 60000
            self.dates[index] = datetime.datetime(1970, 1, 1) \
                + datetime.timedelta(microseconds=millisecs * 1000)
    
    
    def datetime_as_iso(self, dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ") # truncates
    
    
    def datetime_as_iso_ms(self, dt): # with millisecs as fraction
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%%03dZ") \
            % (dt.microsecond // 1000) # truncate  
       
        
class PrecipitationTS(TimeSeries):
    
    def __init__(self):
        super(PrecipitationTS, self).__init__()
        self.unit = "mm"
        self.name = "Precipitation"
        
    def calc_three_days_sum(self):
        if len(self.values) >= 3:
            self.three_days_sum = self.values[-3]+self.values[-2]+self.values[-1]
        else:
            self.three_days_sum = None
        
        
class WindTS(TimeSeries):
    """ Move to appropiate module """
    def __init__(self):
        pass
    
    def plot_windrose(self):
        """
        try:
            import matplotlib
            plot windrose
        except ImportError:
            print "Install matlpotlib to use this function / or a django error msg"
        """
        pass
    
    
class DangerLevelTS(TimeSeries):    

    def __init__(self):
        super(DangerLevelTS, self).__init__()
        self.unit = ""
        self.name = "Avalanche Danger Level"
        
    # Remove duplicate dates from validT list
    def clean_dates(self):
        DL_clean = []
        validT_clean = []
        
        for index in range(len(self.dates)):
            if self.dates[index] not in self.dates[:index]:
                DL_clean.append(self.values[index])
                validT_clean.append(self.dates[index])
            
        DL_array = np.asarray(DL_clean, int)
        self.distr = np.bincount(DL_array)
#         DL_percent = np.asarray(DL_distr, float)/np.size(DL_array, axis=0) * 100.0
    
        self.values = DL_array
        self.dates = validT_clean
        
    
    def bar_plot(self, title=""):
    
        DL_labels = ['0 - no rating', '1 - low', '2 - moderate', '3 - considerable', '4 - high', '5 - very high']
        DL_colors = ['0.5', '#ccff66', '#ffff00', '#ff9900', '#ff0000', 'k']
        
        fsize = (16, 10)
        fig = plt.figure(figsize=fsize)
        
        colors = []
        for n in self.values:
            if n == 1:
                colors.append(DL_colors[1])
            elif n == 2:
                colors.append(DL_colors[2])
            elif n == 3:
                colors.append(DL_colors[3])
            elif n == 4:
                colors.append(DL_colors[4])
            elif n == 5:
                colors.append(DL_colors[5])
            else:
                colors.append(DL_colors[0])
        
        ax = plt.axes([.15, .05, .8, .9])        
        ax.bar(self.dates, self.values, color=colors)
    #    plt.ylim([0, 5])
        plt.yticks(range(len(DL_labels)), DL_labels, size='small')
    #    ymajorLocator = MultipleLocator(1)
    #    ax.yaxis.set_major_locator( ymajorLocator )
        plt.xlabel('Date')
        plt.ylabel(self.name)
        plt.title(title)
        
        
        # this is an inset axes over the main axes
        afrac = 0.2
        bfrac = (float(fsize[0])/float(fsize[1])) * afrac
        apos = 0.95-afrac
        bpos = 0.95-bfrac
        a = plt.axes([apos, bpos, afrac, bfrac])
        
        a.pie(self.distr, colors=DL_colors, autopct='%1.0f%%', shadow=False)
    #    n, bins, patches = hist(s, 400, normed=1)
    #    plt.title('Frequency')
        plt.setp(a, xticks=[], yticks=[])
        
    #     plt.savefig(title+".png", dpi=300)
    #     plt.savefig(title+".pdf", dpi=600)
        plt.show()  
        

