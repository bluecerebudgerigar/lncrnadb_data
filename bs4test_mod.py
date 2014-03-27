#!/usr/bin/env python 

from bs4 import BeautifulSoup
import urllib2
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")
import re
import json, simplejson


##
##class URLFINDER:
##    ### convert list of pudmed id into 1. authour and year
##    ### and urls ###
##    def __init__(self):
##        self.aut_year = {}
##        self.urls = {}
##    
def convert_ref(text):
    aut_year = {}
    id_string = ",".join(text)
    url_pmd = "http://www.ncbi.nlm.nih.gov/pubmed/?term=%s&report=docsum&format=xml" % id_string
    url_response = urllib2.urlopen(url_pmd)
    url_response = url_response.read()
    url_response = BeautifulSoup(url_response)
    aut = url_response.find_all("p", {"class":"desc"})
    year = url_response.find_all("p",{"class":"details"})
    for x, y, z in zip(year, aut, text):
        dates = list(x.children)[1]
        dates = re.search("\d{4}",dates)
        first_aut = y.string
        first_aut =re.search("\w+",first_aut)
        entry = "<a href=\\\"http://www.ncbi.nlm.nih.gov/pubmed/%s\\\">(%s_%s)</a>" % (str(z), str(dates.group(0)), str(first_aut.group(0)))
        aut_year[z] = entry
    print "conversion completed"
    return aut_year
    
def convert_ref_literature(text):
    converted = [] ##list of list
    p = re.compile(r'(\[)|(\])|(<.*?>)')
    id_string = ",".join(text)
    url_pmd = "http://www.ncbi.nlm.nih.gov/pubmed/?term=%s&report=docsum&format=xml" % id_string
    url_response = urllib2.urlopen(url_pmd)
    url_response = url_response.read()
    url_response = BeautifulSoup(url_response)
    aut = url_response.find_all("p", {"class":"desc"})
    year = url_response.find_all("p",{"class":"details"})
    title = url_response.find_all("p",{"class":"title"})
    
    for w, x, y, z in zip(title, year, aut, text):
        entry =[]
        
        dates = list(x.children)[1]
        dates = re.search("\d{4}",dates)
        first_aut = y.string
        first_aut =re.search("\w+",first_aut)

        entry_title=p.sub('', str(w))
        pubmed_link =  "<a href=\\\"http://www.ncbi.nlm.nih.gov/pubmed/%s\\\">%s</a>" % (str(z), str(z))
        entry.append([pubmed_link, str(first_aut.group(0)),entry_title, str(dates.group(0))])
        converted.extend(entry)
    print "conversion completed"
    return converted

    
    
    

#
#url_response = urllib2.urlopen("http://www.ncbi.nlm.nih.gov/pubmed/?term=2156682,16274687,1628523,1205542,123687,2188975&report=docsum&format=xml")
#a = url_response.read()
#b = BeautifulSoup(a)
#authour = b.find_all("p", {"class":"desc"})
#year = b.find_all("p",{"class":"details"})
#for x, y in zip(year, authour):
#    dates = list(x.children)[1]
#    dates = re.search("\d{4}",dates)
#    first_authour = y.string
#    first_authour =re.search("\w+",first_authour)
#    print "(%s_%s)" % (dates.group(0), first_authour.group(0))
#        
#
#
#    #print re.search("(?<=</span>)", i)
#