#!/usr/bin/env python 

from bs4 import BeautifulSoup
import urllib2
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")
import re
import json, simplejson
#from HTMLParser import HTMLParser


##
##class URLFINDER:
##    ### convert list of pudmed id into 1. authour and year
##    ### and urls ###
##    def __init__(self):
##        self.aut_year = {}
##        self.urls = {}
##    


#
#class MLStripper(HTMLParser):                                               
#    def __init__(self):                                                     #Snippets from the web, should really write my own
#        self.reset()                                                        #
#        self.fed = []                                                       #
#    def handle_data(self, d):                                               #
#        self.fed.append(d)                                                  #
#    def get_data(self):                                                     #
#        return ''.join(self.fed)                                            #
#                                                                            #
#def strip_tags(html):                                                       #
#    s = MLStripper()                                                        #
#    s.feed(html)                                                            #

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

class sequence_converter(object):
    def __init__(self, json_data, seq_name):
        self.seq_name = seq_name
        self.data = json_data[1:]
        self.header = json_data.pop(0)
        
        print "this is the length of the header and see if there is %s" % len(self.header)

        self.detail_dict = {} 
        self.accession_uid_map = {}
        self.return_array = [self.header]
    
    
        
    def convert_data_to_dict(self):
        
        self.original_dict = { key : value for key, value in enumerate(self.data)}
        accession_list = [str(x[1]).lower() for x in self.data if x[1] ]
        self.data_dict = {key : value for key, value in enumerate(accession_list)}
        self.reverse_dict = { value : key for key, value in enumerate(accession_list) }
        
        
    def find_unmatched_queries(self):
        unmatch = dict([ (x,y) for x,y in self.data_dict.iteritems() if re.match("<[^>]*>", y ) is None if "," not in y])
        self.unmatch =  unmatch
        
        
    def unmatched_as_list(self):
        unmatch_keys = self.unmatch.keys()
        unmatch_keys = sorted(unmatch_keys)
        unmatch_list = []
        for keys in unmatch_keys:
            unmatch_list.append(self.data_dict[keys])
        
        unmatch_list = ",".join(unmatch_list)            
        self.unmatch_list = unmatch_list
         
        
    def read_get_beauty(self, url_terms):
        url_response = urllib2.urlopen(url_terms)                        
        url_response = url_response.read()                                    
        url_response = BeautifulSoup(url_response)                            
        self.url_response = url_response

        
        
    def find_multimapper(self):
        multi_mapper = []
        url_response =  self.url_response
        termset = url_response.find_all("termset")
        for x in termset:
            if  int(x.find("count").get_text())  > 1:
                multi_mapper.append(str(x.find("term").get_text()))


        multi_mapper = [ re.sub("\[.*\]|\"","",x) for x in multi_mapper]
        multi_mapper = [ x.lower() for x in multi_mapper ]       
        
        for x in multi_mapper:
            try:
                main_key = self.reverse_dict[x]
                del self.unmatch[main_key]
                self.original_dict[main_key] = ["Error Multi-mapper found ",x,"check id"]
            except ValueError:
                pass
            except KeyError:
                pass 
   
    
    def find_unfound(self):
        url_response = self.url_response
        unfound = url_response.find_all("phrasenotfound")
        if unfound is not None:
            unfound = [x.get_text() for x in unfound]
            unfound = [re.sub("\[.*\]","",x) for x in unfound]
            for x in unfound:
                try:
                    main_key = self.reverse_dict[x]
                    
                    del self.unmatch[main_key]
                    self.original_dict[main_key] = ["Error unfound terms ",x,"check id"]
                except ValueError:
                    pass
                except KeyError:
                    pass
                    
                    
    def accession_to_uid(self):
        url_response = self.url_response
        uid_list = [x.get_text() for x in url_response.find_all("id")]
        self.uid_list = ",".join(uid_list)


    def find_details(self, dbtype):
        url_response = self.url_response
        url_response = url_response.find_all("gbseq")
        
        for x in url_response:
            gbseq_primary = x.find("gbseq_primary")
            try :
                gbseq_organism = str(x.find("gbseq_organism").get_text())
            except AttributeError:
                gbseq_organims = "No Organism is found"
            try :
                gbseq_sequence = str(x.find("gbseq_sequence").get_text())
            except AttributeError:
                gbseq_sequence = "No Sequence Found"
                
            gbseq_ids =  x.find_all("gbseqid", text=re.compile('gi'))
            gbseq_id_text = gbseq_ids[0].get_text()
            gbseq_id_text = gbseq_id_text[3:]
            
            if gbseq_primary is None:
                gbseq_primary = x.find("gbseq_primary-accession")
                gbseq_primary = ",".join(gbseq_primary)
            else:
                gbseq_primary = str(gbseq_primary.get_text())
                result = re.findall('\s([A-Za-z0-9\.]+)\s',gbseq_primary)
                gbseq_primary = ",".join(result)
            
            
            self.accession_uid_map[str(gbseq_id_text)] = (str(gbseq_primary)).lower()
            gbseq_primary = ["<a href=https://www.ncbi.nlm.nih.gov/%s/%s>%s</a>" % (dbtype,x,x) for x in gbseq_primary.split(",")]
            gbseq_primary = ",".join(gbseq_primary)
            self.detail_dict[gbseq_id_text]= [str(gbseq_primary), str(gbseq_organism),  str(gbseq_sequence)]
        
        
        
        
    def reverse_match_details(self):
        detail_dict = self.detail_dict ## uid is key
        accession_uid_map = self.accession_uid_map ## uid is key, search term is value
        reverse_dict = self.reverse_dict ##search term is key, value is the entry no  
        for uid, details in detail_dict.iteritems():
            search_term  = accession_uid_map[uid]
            entry_no = reverse_dict[search_term] 
            
            sequence_name = "%s_%s_%s" % (self.seq_name, details[1], entry_no + 1)
            sequence_name = sequence_name.lower()
            sequence_name = re.sub("\s","",sequence_name)
            details.insert(0, sequence_name)
            old_entry = self.original_dict[entry_no]
            if len(old_entry) > 2:
                comments = str(old_entry.pop(2))
            if len(self.header) > 4 :
                details.insert(2,comments)
            self.original_dict[entry_no] = details
    
    def build_return_array(self):
        entry_list = self.original_dict.keys()
        entry_list = sorted(entry_list)
        for entry_no in entry_list:
             self.return_array.append(self.original_dict[entry_no])
    
  #  
  #  def fix_sequence_name(self):
  #      for entry_no, details in self.data_dict.iteritems():
  #           sequence_name = "%s_%s_%s" % (self.seq_name, details[1], entry_no)
  #           sequence_name.lower()
  #           print details 
  #           
  #           sequence_name = re.sub("\s","",sequence_name)
  #           print "this is equence name %s" % sequence_name
  #           self.return_array.append(details)

            
def convert_function_sequence(json_data, pagename):


    seq_convertor = sequence_converter(json_data, pagename)
    seq_convertor.convert_data_to_dict()
    seq_convertor.find_unmatched_queries()
    seq_convertor.unmatched_as_list()

    esearch_header = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term="
    esearch_url = "%s%s" % (esearch_header, seq_convertor.unmatch_list)

    try :
        seq_convertor.read_get_beauty(esearch_url)
    except urllib2.HTTPError:
        print "Error in HTTP"
        return seq_convertor.json_data

    seq_convertor.find_multimapper()
    seq_convertor.find_unfound()
    seq_convertor.unmatched_as_list()

    esearch_header = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucest&term="
    esearch_url = "%s%s" % (esearch_header, seq_convertor.unmatch_list)

    seq_convertor.find_multimapper()
    seq_convertor.find_unfound()
    seq_convertor.unmatched_as_list()

    if len(seq_convertor.unmatch_list) > 0:
        esearch_header = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term="
        esearch_url = "%s%s" % (esearch_header, seq_convertor.unmatch_list)
        try :
            seq_convertor.read_get_beauty(esearch_url)
        except urllib2.HTTPError:
            print "Error in HTTP"
            return seq_convertor.json_data

        seq_convertor.accession_to_uid()
        efetch_header = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id="
        efetch_url = "%s%s&retmode=xml" % (efetch_header, seq_convertor.uid_list)
        try:
            seq_convertor.read_get_beauty(efetch_url)
        except urllib2.HTTPError:
            print "Error in HTTP"
            return seq_convertor.json_data

        seq_convertor.find_details('nucore')

        esearch_header = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucest&term="
        esearch_url = "%s%s" % (esearch_header, seq_convertor.unmatch_list)
        try :
            seq_convertor.read_get_beauty(esearch_url)
        except urllib2.HTTPError:
            print "Error in HTTP"
            return seq_convertor.json_data


        seq_convertor.accession_to_uid()
        efetch_header = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucest&id="
        efetch_url = "%s%s&retmode=xml" % (efetch_header, seq_convertor.uid_list)
        try:
            seq_convertor.read_get_beauty(efetch_url)
        except urllib2.HTTPError:
            print "Error in HTTP"
            return seq_convertor.json_data

        seq_convertor.find_details('nucore')
        seq_convertor.reverse_match_details()

        print "##### section of nucore #####"
        print "this is the detail_dict %s " % seq_convertor.detail_dict
        print "this is the accession_map %s " % seq_convertor.accession_uid_map
        print "this is the reverse dict %s " % seq_convertor.reverse_dict
        print "this  is self.original_dict %s" % seq_convertor.original_dict

    seq_convertor.build_return_array()
    return seq_convertor.return_array


class efetch_one(object):

    def __init__(self, accession_id):
        self.accession_id = accession_id


    def esearch_url(self, db):
        esearch_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=%s&term=%s" % (db, self.accession_id)
        return esearch_url

    def efetch_url(self, db, uid):
        efetch_url  = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=%st&id=%s&retmode=xml" % (db, uid)
        return efetch_url

    def read_get_beauty(self, url_terms):
        url_response = urllib2.urlopen(url_terms)
        url_response = url_response.read()
        url_response = BeautifulSoup(url_response)
        self.url_response = url_response

    def check_results(self):
        url_response = self.url_response
        count = url_response.find("count").get_text()
        self.uid = str(url_response.find("id").get_text())
        return count

    def build_return(self, db):
        "<a href=http://www.ncbi.nlm.nih.gov/nuccore/"






def cmsexportor_convertseq(accession_id):
    convertseq = efetch_one(accession_id)
    esearch_url = convertseq.esearch_url("nucleotide")
    convertseq.read_get_beauty(esearch_url)

    if convertseq.check_results() == "1":








convertseq.read_get_beauty(efetch_url)




