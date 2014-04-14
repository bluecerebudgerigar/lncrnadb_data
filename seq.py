#!/usr/bin/env python

import re
import urllib2 as url
from bs4 import BeautifulSoup as bs4
test = url.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=371502118,146001389&retmode=xml")
result = test.read()
content = bs4(result)
gbseq = content.find_all("gbseq")

dict_accession = {}
for i in gbseq:
    try:
        qq = i.find("gbseq_primary")
        qq = qq.get_text()
        dict_accession[i] = [blah for blah in qq.split() if re.match("^[a-zA-Z0-9\.]+$", blah) is not None]
    except AttributeError:
        #dict_accession[i] = i.find("gbseq_accession-version").get_text()
        pass
        
        
        
#print dict_accession
   #if length(qq) > 1:
   #    accession_id = [blah for blah in qq.split() if re.match("^[a-zA-Z0-9\.]+$", blah) is not None]
   #     = accession_id
   #else :
   #     = i.find("GBSeq_accession-version").get_text()