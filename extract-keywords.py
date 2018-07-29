""" Extract keywords from CSV file which is imported from LongTailPro. 
Replace spaces with '-'. Insert comman between keywords.
"""
import sys
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub


# parse command line
p = OptionParser(usage="""usage: %prog [options]
Extract keywords from CSV file which is imported from LongTailPro. 
Replace spaces with '-'. Insert comman between keywords.

Ex: 
./extract_keywords.py -f 'keywords.csv'
 -f = csv file downloaded from LongTailPro

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
#p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Database Name")
p.add_option("-f", "--file", action="store", type="str", default="NONE", dest="readf", help="CSV file containing sales")

(opts, args) = p.parse_args()

if opts.readf == "NONE":
  print ("CSV file not defined")
  sys.exit(0) 
else:
  f_name = opts.readf

""" Read CSV file which contains ebay sales
"""
print ("Reading CSV file "+f_name)
csvfile = Fileio(f_name)
dataset = csvfile.getDataSet()

string = ""
for dict in dataset:
  string += dict['Keywords'].replace(" ","-")+","
  #string = ''.join((dict['Keywords'].replace(" ","-")).strip()+",")

print(string)

sys.exit(0)


