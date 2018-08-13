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
  update_item_cost(db_name,store,"UPDATING item_cost_amz")
  # Update cost in item_cost_amz

def update_webcg_item_cost(db_name,store):
  # Insert shipping cost to item_cost_web
  update_item_cost(db_name,store,"UPDATING item_cost_web")
  # Update cost in item_cost_web

def update_item_cost2(db, sql_string,store,outstring):
  prev_sales_rec_num = 0
  prev_cost = 0
  total_cost = 0
  print (outstring)
  #print (sql_string)
  """ Get database connection
  """
  # user = "cito"
  # passwd = "citoKUKU123"

  # db = Database(db_name,user,passwd)
  # db.getConnection()
  
  previous_cost = {}

  cursor = db.selectSQL(sql_string)
  for row in cursor:
    previous_cost[row[0]] = 0.0
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    #print ("previous_cost"+str(row[0]),str(row[2]))
    previous_cost[row[0]] = float(previous_cost[row[0]]) + float(row[2]) + float(row[3])
  
  for k,v in previous_cost.iteritems():

    # if (prev_sales_rec_num == row[0]):
    #   total_cost = prev_cost + row[2]
    # else:
    #   total_cost = row[2]
    # prev_cost = total_cost
    
    sql_string = "UPDATE "+store+"_item_cost set cost="+str(round(int(v * 1000) / 1000.0,2))+" WHERE sales_record_number="+str(k)
    print(sql_string)
    db.updateSQL(sql_string)
 
    prev_sales_rec_num = row[0]


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
  while sales_record > 0:
    sales_record = input("  Enter sales record number (Exit 0): ")
    sql_string2 = "select a.sales_record_number,b.custom_lable, \
    b.quantity*c.units_per_order*d.unit_cost*d.unit_cost_conversion,b.quantity*c.package_cost from "+store+"_item_cost a\
    inner join "+store+"_sales_tbl b on a.sales_record_number=b.sales_record_number\
    inner join sku_tbl c on b.custom_lable=c.custom_lable inner join stock d \
    on c.stock_reference=d.stock_reference"
    #print(sql_string2)
    if sales_record == 0:
      update_item_cost2(db,sql_string2,store,outstring)
      db.closeDatabase()
      exit(1)
    shipping = input("  Enter postage cost: ")
    print("------------------------")
    sql_string = "INSERT INTO "+store+"_item_cost (sales_record_number, shipping) VALUES ("+str(sales_record)+","+str(shipping)+")"
    db.insertSQL(sql_string)

  update_item_cost2(db,sql_string2,store,outstring)
 
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


