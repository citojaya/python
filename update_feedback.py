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
stock_id = input("Enter stock id:")

""" Select item_description and qunatity from sku_tbl and stock
"""
sql_string = "SELECT a.item_description, b.quantity, b.stock_reference FROM sku_tbl a inner join stock b \
ON a.stock_reference=b.stock_reference WHERE a.id="+str(stock_id)

cursor = db.selectSQL(sql_string)

for row in cursor:
  print("  "+row[0])
  print("  Current Stock = "+str(row[1]))
  new_stock = input("Enter new quantity:")
  sql_string = "UPDATE stock SET quantity="+str(new_stock)+" WHERE stock_reference='"+row[2]+"'"
  db.updateSQL(sql_string)
  print("Stock updated successfully")
  #print(sql_string)


""" Close database
"""
db.closeDatabase()
sys.exit(0)


