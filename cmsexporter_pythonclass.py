#!/usr/bin/env python 

import re 
import os
import sys
from collections import defaultdict
import csv
from pprint import PrettyPrinter as Pprint
import json
from itertools import *


class GenericReader(object):
    def __init__(self,prefix):
        self.files = {}
        self.fixed = {}
        self.prefix = prefix

        
        
    def __str___(self):
        return "The file are %s" % self.file_list
        
    
    def read_file(self, filename, content):
        self.files[content]={}
        with open(filename) as file:
            for line in file:
                try:
                    entry_id = line.split("\t")[0]
                    if re.search("^[0-9]+$",entry_id): 
                        self.files[content][entry_id]=line
                    else: 
                        print "Wrong Entry ID %s" % entry_id
                except KeyError as ERR:
                    print "keyerror : %s entry : %s line : %s" % (ERR, entry_id, line)
        file.close()
    
    def read_csv(self, filename, content):
        self.files[content]={}
        
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                line = ';'.join(row)
                self.files[content][str(row[0])]= line
            
    def print_content(self):
        Pp = Pprint(indent=4)
        Pp.pprint(self.files)
        
        
    def print_fixed(self):
        for value, key in self.fixed.iteritems():
            print value
            print key
            
    def write_csv(self, filename):
        with open(filename, 'ab') as csvfile:
            fixedwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL)
            for key, value in self.fixed.iteritems():
                value[5]=json.dumps(value[5])
                fixedwriter.writerow(value)
                
    def match(self, content='associatedcomp', identifier='annotation'):
         
         unmapped = set(self.files[content].keys()) - set(self.files[identifier].keys())
         for x in unmapped:
             del self.files[content][x]
             
             
    def name(self):
        return self.__class__.__name__                
    
        
        
        
        
                

class SequenceWorker(GenericReader):   
    def __init__(self,prefix):
        
        self.publisher_prefix = 600000
        GenericReader.__init__(self,prefix)  
               
    def match(self, content='sequences', identifier='annotation'):
        self.seq_entries = {}
        for entry in self.files[identifier].keys():
            annotation = self.files[identifier][entry].split("\t") ## split annotation file by tab
            lncrnadb_id = annotation[0]
            seqid_list = annotation[4].rstrip().split(';')
            accesion_list = annotation[3].split(';')
            seq_species_list = annotation[2].split(';')
            entry_list = []
            for seq_id, accession_id, seq_species in zip(seqid_list, accesion_list, seq_species_list):
                sequence = seq_species,self.files[content][seq_id].split("\t")
                sequence = sequence[1][1]
                entry_list.append([seq_id, accession_id, seq_species, sequence])
                
            self.seq_entries[lncrnadb_id] = entry_list
        self.files['sequences'] = self.seq_entries
            
    def fixup(self, content='sequences'):
        name = content.title()
        
        for transcript_id, value  in self.files[content].iteritems():
            cmsptr_id = self.prefix + int(transcript_id)
            seq_array =  [str(cmsptr_id),name,1,0,0]
            data_column = [["Sequence Name","Sequence Accession IDs","Species","Fasta Sequence"]]
            for sequences in value:
                data_column.append(sequences)
            seq_array.append(data_column)
            
            self.fixed[str(transcript_id)] = seq_array
        print len(self.fixed.keys())
        #    print value
        #    print "cms_id;%s;1;0;0;%s" % (content, seq_entry)
         
            
                
            
class CharacterWorker(GenericReader):
    def __init__(self,prefix):
        
        self.publisher_prefix = 200000
        
        GenericReader.__init__(self,prefix)   
        
    def read_csv(self, filename, content):
        self.files[content]={}
        
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                line = ';'.join(row)
                try:
                    self.files[content][row[0]][";".join([row[3],row[1]])] = row[2]
                except KeyError as ERR:
                    #print "Creating New Hash %s" % ERR
                    self.files[content][row[0]] = {}
                    self.files[content][row[0]][";".join([row[3],row[1]])] = row[2]                    
    
                    
           

    
    

    
    def fixup(self, content='characteristics'):
        name = content.title()
        
        for transcript_id in self.files[content].keys(): ##
            cmsptr_id = self.prefix + int(transcript_id)
            
            characteristics_array = [str(cmsptr_id),name,"0","1","0"]
            data_column = []
            
            order = self.files[content][transcript_id].keys()
            order.sort()
            print order
            for annotation_class in order:
                value = self.files[content][transcript_id][annotation_class]
                annotation_class = annotation_class.split(";")[1]
                data_column.append([annotation_class, value])
            characteristics_array.append(data_column)
            self.fixed[str(transcript_id)] = characteristics_array
                
     #       for annotation_class, value in self.files[content][transcript_id].iteritems():
     #           data_column.append([annotation_class,value])
     #       characteristics_array.append(data_column)
     #       self.fixed[str(transcript_id)] = characteristics_array
     #           
     #          # print "cms_id;Annotation;0;1;0;%s" % (characteristics_array)
     #           



     
    
             
             
class LiteratureWorker(GenericReader):
    def __init__(self,prefix):
        
        self.publisher_prefix = 400000
        
        GenericReader.__init__(self,prefix) 
        
    
    def read_csv(self, filename, content):
        self.files[content]={}
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                line = ';'.join(row)
                try:
                    self.files[content][row[0]].append(line)
                except KeyError as ERR:
                    #print "Creating New Hash %s" % ERR
                    self.files[content][row[0]] = []
                    self.files[content][row[0]].append(line)
        
        
    
            
                
    def fixup(self, content='literature'):
        name = content.title()
        
        for transcript_id in self.files['annotation'].keys(): ##
        #   
            cmsptr_id = self.prefix + int(transcript_id)
            literature_array = [str(cmsptr_id),name,"1","0","0"]
            
            data_column = [["Pub Med ID","Author","Title","Year"]]
            pub_list = self.files[content][transcript_id]
            for pubmed in pub_list:
                data_column.append(pubmed.split(";")[1:])
            literature_array.append(data_column)
            self.fixed[str(transcript_id)] = literature_array

          #      print "cms_id;%s;1;0;0;%s" % ( content, data_column)

class SpeciesWorker(GenericReader):
    def __init__(self,prefix):
        
        self.publisher_prefix = 300000
        
        GenericReader.__init__(self,prefix) 
        
    def read_csv(self, filename, content):
        self.files[content]={}
        
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                line = ';'.join(row)
                try:
                    self.files[content][row[0]][row[1]] = row[3]
                except KeyError as ERR:
                    #print "Creating New Hash %s" % ERR
                    self.files[content][row[0]] = {}
                    self.files[content][row[0]][row[1]] = row[3]
                 

    def fixup(self, content='species'):            
        name = content.title()
        for transcript_id in self.files[content].keys(): ##
            cmsptr_id = self.prefix + int(transcript_id)
            species_array = [str(cmsptr_id),name,"1","0","0"]

            data_column = [['Species','UCSC Genome Browser Link']]
            for species in self.files[content][transcript_id].keys():
                data_column.append([species,self.files[content][transcript_id][species]])
            species_array.append(data_column)
            self.fixed[str(transcript_id)] = species_array
                
                #print "cms_id;%s;1;0;0;%s" % (content, data_column)
        ## Cms,name,1,0,0,[[Species,UCSC Genome Browser Link],[Species1,Link],[Species2,link]]
               
    

class AssocWorker(GenericReader):
    def __init__(self,prefix):
        
        self.publisher_prefix = 500000
        
        
        GenericReader.__init__(self,prefix) 

    def read_csv(self, filename, content):
        self.files[content]={}
        
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                line = ';'.join(row)
                try:
                    self.files[content][row[0]][row[1]] = row[3]
                except KeyError as ERR:
                    #print "Creating New Hash %s" % ERR
                    self.files[content][row[0]] = {}
                    self.files[content][row[0]][row[1]] = line
                    
   
        
    def fixup(self, content='associatedcomp'):
        name = content.title()
        
        for transcript_id in self.files[content].keys(): ##
            cmsptr_id =  self.prefix + int(transcript_id)
            associated_array = [str(cmsptr_id),name,"1","0","0"]
            data_column = [["Component Type","Component ID","Description","Pub Med ID"]]
            for key, value in self.files[content][transcript_id].iteritems():
                data_list = value.split(";")
                data_column.append(data_list[1:])
            associated_array.append(data_column)
            self.fixed[str(transcript_id)] = associated_array
                
                #print "cms_id;Associated Component;1;0;0;%s" % (data_column)
                 
        


class AliasWorker(GenericReader):
    def __init__(self,prefix):
        
        
        
        GenericReader.__init__(self,prefix) 

    def read_csv(self, filename, content):
        self.files[content]={}
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            for row in csv_reader:
                line = ';'.join(row)    
                try:
                    self.files[content][row[0]] =  row[1:]
                except KeyError as ERR:
                    self.files[content][row[0]] = []
                    self.files[content][row[0]] =  row[1:]
    
    def fixup(self, content='nomenclature'):
        name = content.title()
        
        for transcript_id, value in self.files[content].iteritems():
            cmsptr_id = self.prefix + int(transcript_id)
            value = [re.sub(r'\r|\n', ',', x) for x in value]
            value = [re.sub(r',,',', ',x) for x in value]
            nomenclature_array = [str(cmsptr_id),value[0],"1","0","0"]
            data_column=[["Name","Alias"],value]
            nomenclature_array.append(data_column)
            self.fixed[str(transcript_id)] = nomenclature_array
            


class MasterController():
    def __init__(self):
        self.collection = {}
        self.plugin_types = {'1':'NomenclaturePlugin','2':'AnnotationPlugin','3':'SpeciesPlugin','4':'LiteraturePlugin','5':'AssociatedcompPlugin','6':'SequencesPlugin'}
        self.position_types = {'1':'0','2':'1','3':'2','4':'3','5':'4','6':'5'}
        self.consenses_entries = []
        self.cmsplugins_format = {}
        self.cms_page_format = {}
        self.cmsplaceholder = {}
        self.cms_page_placeholder = {}
        self.cms_title = {}
        self.cms_page = {}
        self.identifier = {}
        self.master_collection = {x : {} for x in ["cms_cmsplugins","cms_placeholder","cms_page_placeholders","cms_page","cms_title"]}
    
    def add_identifer(self, filename):
        with open(filename, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter="\t")
            for row in csv_reader:
                self.identifier[row[0]] = row[1]
        
    
        
    def additems(self, *args):
        self.placeholder_id = 0
        self.dict_dict = {}
        for a in args:
            dict_entry = a.fixed
            self.dict_dict[a.name()] = a.fixed
            self.collection
    
    def check_consenses(self):
        check_dict_length = []
        for d in self.dict_dict:
            check_dict_length.append(self.dict_dict[d].keys())
        missing_entries = list(reduce(set.union, (starmap(set.difference, combinations(map(set, check_dict_length), 2)))))
        print missing_entries
        consenses_entries = list(reduce(set.union, (starmap(set.intersection,  combinations(map(set, check_dict_length), 2)))))
        consenses_entries = [int(x) for x in consenses_entries]
        consenses_entries.sort()
        consenses_entries = [str(x) for x in consenses_entries]
        self.consenses_entries = consenses_entries
        for i in consenses_entries:
            for d in self.dict_dict:
                try:
                    self.dict_dict[d][i]
                except KeyError as ERR:
                    print "The following entries are missing : From Table : %s\t Transcript ID : %s" % (d, ERR) ## i think i should add this to another list then. 
        
    def build_cmsplugin(self): ## build cmsplugins and cmsPlceholder
        placeholder_id = 0
        for i in self.consenses_entries:
            self.cms_page_format[i] = []
            self.cms_page[i] = []
            self.cms_title[i] = []
            for d in self.dict_dict:
                try:
                    row = []
                    value = self.dict_dict[d][i]
                
                    cmp_id = value[0][0]
                    placeholder_id = placeholder_id + 1
                    parent_id = "\N"
                    position = self.position_types[cmp_id]
                    level = 0
                    lft = 1
                    right = 2
                    tree_id = placeholder_id
                    language = "en"
                    create_date="2014-02-07 14:49:32"
                    change_date = create_date
                    create_by = "quek"
                    plugin_type = self.plugin_types[cmp_id]
                    row = [value[0], placeholder_id,parent_id,position,language,plugin_type,create_date,change_date,level,lft,right,tree_id]
                    null = "\N"
                    slug = self.identifier[i].replace(" ","") 
                    slug = slug.replace("/","")
                    cms_page_id = int(i) + 10000
                    
                    self.master_collection["cms_cmsplugins"][placeholder_id] = row
                    self.master_collection["cms_placeholder"][placeholder_id] = [placeholder_id, plugin_type,null]
                    self.master_collection["cms_page_placeholders"][placeholder_id] = [placeholder_id, i, placeholder_id]
                    self.master_collection["cms_page"][i] = [i, create_by, create_by, null, create_date, create_date, null, null, 0,0,null,null, 0,"entry_template.html", 1,0,1,2,i,0,null, 1, cms_page_id, 1 ] 
                    self.master_collection["cms_title"][i] = [i, language, self.identifier[i], null, slug, self.identifier[i], "0", null, null, null, null, null,cms_page_id,create_date ]
                    
                except KeyError as ERR:
                    pass
                    
                    
                    
                    
    def build_cmsplugin_publisher(self):
        placeholder_id = 10000
        for i in self.consenses_entries:
            self.cms_page_format[i] = []
            self.cms_page[i] = []
            self.cms_title[i] = []
            for d in self.dict_dict:
                try:
                    row = []
                    value = self.dict_dict[d][i]
                    cmp_id = value[0][0]
                    cms_cmsplugin_id = int(value[0]) + 10000
                    placeholder_id = placeholder_id + 1
                    parent_id = "\N"
                    position = self.position_types[cmp_id]
                    level = 0
                    lft = 1
                    right = 2
                    tree_id = placeholder_id
                    language = "en"
                    create_date="2014-02-07 14:49:32"
                    change_date = create_date
                    create_by = "quek"
                    plugin_type = self.plugin_types[cmp_id]
                    cms_page_id = int(i) + 10000
                    row = [cms_cmsplugin_id, placeholder_id,parent_id,position,language,plugin_type,create_date,change_date,level,lft,right,tree_id]
                    null = "\N"
                    slug = self.identifier[i].replace(" ","") 
                    slug = slug.replace("/","")
                    
                    self.master_collection["cms_cmsplugins"][placeholder_id] = row
                    self.master_collection["cms_placeholder"][placeholder_id] = [placeholder_id, plugin_type,null]
                    self.master_collection["cms_page_placeholders"][placeholder_id] = [placeholder_id, i, placeholder_id]
                    self.master_collection["cms_page"][i] = [cms_page_id, create_by, create_by, null, create_date, create_date, null, null, 0,0,null,null, 0,"entry_template.html", 1,0,1,2,cms_page_id,0,null, 1, i, 1 ] 
                    self.master_collection["cms_title"][i] = [cms_page_id, language, self.identifier[i], null, slug, self.identifier[i], "0", null, null, null, null, 1,i,create_date ]
                         
                     
                     
                     
              #   self.cmsplugins_format[placeholder_id] =  row
              #   self.cmsplaceholder[placeholder_id] = [placeholder_id, plugin_type,null]            
              #   self.cms_page_format[i].append(placeholder_id)
              #   self.cms_page_placeholder[placeholder_id] = [placeholder_id, i, placeholder_id]
              #               
              #   self.cms_page[i]= [i, create_by, create_by, null, create_date, create_date, null, null, 0,0,null,null, 0,"entry_template.html", 1,0,1,2,1,0,null, 1, null, 1 ] 
              #   
              #   ## id/createby/changeby/parentid/creationdate/changeddata/publicationdata/plublicationen/ \ innavigation/softroot/reverseid/navigation_enx/published/template/siteid/ 
              #   ##\login/required/limit_vis/level/lft/rght/treeid/publishedisdraf/published/
              #   self.cms_title[i]=[i, language, self.identifier[i], null, self.identifier[i], null, 0, null, null, null, null, null,i,create_date ]
                except KeyError as ERR:
                    pass
    
        
              
          
    def write_csv(self, prefix=""):
        print "writing"
        for key, value in self.master_collection.iteritems():  
            filename  = "output/%s%s" % (prefix, key )
            with open(filename, 'ab') as csvfile:
                fixedwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL)  
                
                for i in value: 
                    fixedwriter.writerow(value[i])   
                


