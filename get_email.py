""" Calculate profit for a given period
"""
import sys
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub


def get_ebay_customers(db_name,sql_string):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  email_list = []
  print (sql_string)
  """ Select custom_lable, cost from package_cost and store in a dictionary
  """
  # prepare a cursor object using cursor() method
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    # 1-customer name
    # 0-email
    email_list.append(str(row[0])+"\n")
    #print row[3],row[2]

  """ Close database
  """
  db.closeDatabase()

  f = open("email_list.dat","w")
  f.writelines(email_list)
  f.close()

# parse command line
p = OptionParser(usage="""usage: %prog [options]
Extract email and buyer_name from sales

Ex: calculate_profit.py <date1> <date2> <database> <sku>
 date1 = starting date
 date2 = end date
 sku = item to be checked

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Database")
p.add_option("-s", "--store", action="store", type="str", default="NONE", dest="store", help="Store type")

(opts, args) = p.parse_args()

sql_string = db_name = ""

if opts.readdb == "NONE":
  print("Database not defined")
  sys.exit(0)
else:
  db_name = opts.readdb
if opts.store == "NONE":
  print("Store not defined")
  sys.exit(0)
else:
  store_type = opts.store

if len(args) < 1:
  print "Input paramaters should be greater than one"
  sys.exit(0)
elif len(args) == 1:
  (num) = args[0]
  if (store_type=="web"):
    sql_string = "SELECT sales_record_number FROM shipping_tbl WHERE sales_record_number="+num
    get_web_customers(db_name,sql_string)
elif len(args) ==2:
  (start_date, end_date) = args
  if (store_type=="web"):
    sql_string = "SELECT a.sales_record_number FROM shipping_tbl a INNER JOIN web_item_cost b ON\
    a.sales_record_number = b.sales_record_number INNER JOIN web_sales_tbl c ON b.sales_record_number=c.sales_record_number\
    WHERE c.sale_date>='"+start_date+"' AND c.sale_date<='"+end_date+"'"
    
    get_web_customers(db_name,sql_string)

  if (store_type=="ebay"):
    sql_string = "SELECT  buyer_email, buyer_fullname FROM ebay_sales_tbl WHERE \
    sale_date>='"+start_date+"' AND sale_date<='"+end_date+"'"
    #print(sql_string)
    #sys.exit(0)
    get_ebay_customers(db_name,sql_string)
    

elif len(args) == 3:
  (start_date, end_date, item) = args
  sql_string = "SELECT  buyer_email, buyer_fullname FROM ebay_sales_tbl WHERE \
    sale_date>='"+start_date+"' AND sale_date<='"+end_date+"'AND custom_lable='"+item+"'"


sys.exit(0)



