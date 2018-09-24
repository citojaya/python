""" Update item_cost table
    option -d defines database name and option -o defines which item_cost table to be updated
Ex:
  -o = ebay -> item_cost_ebay
  -o = amz -> item_cost_amz
  -o = web -> item_cost_web
"""
import sys
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub

def update_ebay_item_cost(db_name,store):
  # Insert shipping cost to item_cost_ebay
  update_item_cost(db_name,store,"UPDATING shipping in ebay_item_cost")


def update_amz_item_cost(db_name,store):
  # Insert shipping cost to item_cost_amz
  update_item_cost(db_name,store,"UPDATING amz_item_cost")
  # Update cost in item_cost_amz

def update_webcg_item_cost(db_name,store):
  # Insert shipping cost to item_cost_web
  update_item_cost(db_name,store,"UPDATING web_item_cost")
  # Update cost in item_cost_web

def update_item_cost_table(db, sql_string,store,outstring):
  """ Update cost column in item_cost one by one 
  """
  prev_sales_rec_num = 0
  prev_cost = 0
  total_cost = 0
  print (outstring)

  
  total_cost = 0
  sales_record_number = 0
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    # print ("ROW IN CURSOR",row[0])
    # print ("ROW IN CURSOR",row[2])
    # print ("ROW IN CURSOR",row[3])
    sales_record_number = row[0]
    total_cost += float(row[2]) + float(row[3])
    sql_string = "UPDATE stock set quantity=quantity-"+str(row[4])+" WHERE stock_reference='"+str(row[5])+"'"
    print (sql_string)
    db.updateSQL(sql_string)   
  
  print("TOTAL COST",total_cost)

  sql_string = "UPDATE "+store+"_item_cost set cost="+str(round(int(total_cost * 1000) / 1000.0,2))+" WHERE sales_record_number="+str(sales_record_number)
  db.updateSQL(sql_string)
 

def update_item_cost(db_name,store,outstring):
  print (outstring)
  print ("-----------------------")
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()
  sales_record = 1
  record_list = []
  while sales_record > 0:
    sales_record = input("  Enter sales record number (Exit 0): ")
    if sales_record == 0:
      db.closeDatabase()
      exit(0)

    shipping = input("  Enter postage cost: ")
    sql_string = "INSERT INTO "+store+"_item_cost (sales_record_number, shipping) VALUES ("+str(sales_record)+","+str(shipping)+")"
    db.insertSQL(sql_string)

    sql_string2 = "select a.sales_record_number,b.custom_lable, \
    b.quantity*c.units_per_order*d.unit_cost*d.unit_cost_conversion,b.quantity*c.package_cost, \
    b.quantity*c.units_per_order,c.stock_reference from "+store+"_item_cost a\
    inner join "+store+"_sales_tbl b on a.sales_record_number=b.sales_record_number\
    inner join sku_tbl c on b.custom_lable=c.custom_lable inner join stock d \
    on c.stock_reference=d.stock_reference where a.sales_record_number="+str.strip(str(sales_record))
    
    update_item_cost_table(db,sql_string2,store,outstring)
    print("------------------------")
 
  """ Close database
  """
  db.closeDatabase() 


# parse command line
p = OptionParser(usage="""usage: %prog [options]
Update item_cost table
Option -d defines database name and option -s defines which item_cost to be updated

Ex: python update_item_cost.py -d "ebay_database" -s "ebay"
 -d = database name
 -s = store type

 Options for -s
 eBay - item_cost_ebay
 amz - item_cost_amz
 webcg - item_cost_cg

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Website Database")
p.add_option("-s", "--store", action="store", type="str", default="NONE", dest="store", help="Store Type")

(opts, args) = p.parse_args()

if opts.readdb == "NONE":
  print("Database not defined")
  sys.exit(0)
else:
  db_name = opts.readdb

if opts.store == "ebay":
  update_ebay_item_cost(db_name,opts.store)
elif opts.store == "amz":
  update_amz_item_cost(db_name,opts.store)
elif opts.store == "web":
  update_webcg_item_cost(db_name,opts.store)
else:
  print("item_cost table not defined")
  sys.exit(0)
 

sys.exit(0)


