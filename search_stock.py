""" Update item_cost table
    option -d defines database name and option -f defines input CSV file which contains shipping cost
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
Update stock for a given database

Ex: python update_stock.py -d "ebay_database" 
 -d = database name
 
""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Website Database")

(opts, args) = p.parse_args()

if opts.readdb == "NONE":
  print("Database not defined")
  sys.exit(0)
else:
  db_name = opts.readdb


""" Get database connection
"""
user = "cito"
passwd = "citoKUKU123"

db = Database(db_name,user,passwd)
db.getConnection()

""" Read input id for the stock
"""
this_string = input("Enter item description:")

""" Select item_description and qunatity from sku_tbl and stock
"""
sql_string = "SELECT stock_id, item_description, quantity, stock_reference FROM stock WHERE \
item_description LIKE '%"+str(this_string)+"%'"

print sql_string
#sys.exit(0)

cursor = db.selectSQL(sql_string)

for row in cursor:
  print("  "+str(row[0])+" "+row[1])


""" Close database
"""
db.closeDatabase()
sys.exit(0)


