""" Delete records from selected table
    option -d defines database name and option -t defines database table which contains records to be deleted
"""
import sys
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub


def delete_record(f_name,db_name,tb_name):
  """ Read CSV file which contains records to be deleted
  """
  print ("Reading CSV file "+f_name)
  csvfile = Fileio(f_name)
  dataset = csvfile.getDataSet()

  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  for dict in dataset:
    sql_string = "DELETE FROM "+tb_name+" WHERE order_id="+str(dict['Order_id'])
    db.updateSQL(sql_string)
    #print(sql_string)
    
  """ Close database
  """
  db.closeDatabase() 

# parse command line
p = OptionParser(usage="""usage: %prog [options]
Delete records from a given database

Ex: 
  ./delete_record.py -f 'sales.csv' -d ebay_database -t table
  -f = CSV file containing records
  -d = database name
  -t = table name

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Database Name")
p.add_option("-f", "--file", action="store", type="str", default="NONE", dest="readf", help="CSV file containing records to be deleted")
p.add_option("-t", "--table", action="store", type="str", default="NONE", dest="readt", help="Database table")

(opts, args) = p.parse_args()

if opts.readdb == "NONE":
  print("Database not defined")
  sys.exit(0)
if opts.readf == "NONE":
  print("Input file not defined")
  sys.exit(0)
if opts.readt == "NONE":
  print("Table not defined")
  sys.exit(0)
else:
  delete_record(opts.readf,opts.readdb,opts.readt)

sys.exit(0)


