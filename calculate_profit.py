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


def calculate_web_sales(db_name,sql_string):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  sales_record = {}
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    sales_record[row[0]] = row[0]

  total_sale_price = total_postage = total_cost = total_shipping = total_discount = total_refunds = 0.0
  
  for k,v in sales_record.iteritems():
    sql_string = "SELECT discount,shipping,total FROM shipping_tbl WHERE sales_record_number="+str(k)
    cursor = db.selectSQL(sql_string)
    for row in cursor: 
      total_sale_price += float(row[2])
      total_postage += float(row[1])
      total_discount += float(row[0])
    
    sql_string = "SELECT amount FROM refunds WHERE sales_record_number="+str(k)
    cursor = db.selectSQL(sql_string)
    for row in cursor: 
      total_refunds += float(row[0])

    sql_string = "SELECT cost,shipping FROM web_item_cost WHERE sales_record_number="+str(k)
    cursor = db.selectSQL(sql_string)
    for row in cursor: 
      total_cost += float(row[0])
      total_shipping += float(row[1])
 
  total_sale_price = total_sale_price - total_refunds
  print("Total")
  print("  Sales",total_sale_price)
  print("  Discount",total_discount)
  #print("  Postage Paid By Buyer",total_postage)
  print("  Cost",total_cost)
  print("  Shipping",total_shipping)
  print("  Paypal charges",total_sale_price*0.05)
  print("  Refunds ",total_refunds)
  profit = total_sale_price+total_discount-total_sale_price*0.05-total_cost-total_shipping
  print("  Profit ",profit)
  if (total_sale_price != 0):
    print ("  Margin Percentage", 100*profit/total_sale_price)
  if (total_cost != 0):
    print ("  Profit/Cost Percentage", 100*profit/(total_cost))  



  """ Select custom_lable, cost from package_cost and store in a dictionary
  """

  """ Close database
  """
  db.closeDatabase()

def calculate_ebay_sales(db_name,sql_string):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  total_sale_price = total_postage = total_cost = total_shipping = total_discount = total_refunds = 0.0
 
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    total_sale_price += float(row[1])
    total_postage += float(row[2])
    total_cost += float(row[3])
    total_shipping += float(row[4])
      
    sql_string = "SELECT amount FROM refunds WHERE sales_record_number="+str(row[0])
    cursor = db.selectSQL(sql_string)
    for row in cursor: 
      total_refunds += float(row[0])
  
  total_sale_price = total_sale_price - total_refunds
  print("Total")
  print("  Sales",total_sale_price)
  #print("  Postage Paid By Buyer",total_postage)
  print("  Cost",total_cost)
  print("  Shipping",total_shipping)
  print("  Paypal charges",total_sale_price*0.05)
  print("  Refunds ",total_refunds)
  profit = total_sale_price+total_discount-total_sale_price*0.05-total_cost-total_shipping
  print("  Profit ",profit)
  if (total_sale_price != 0):
    print ("  Margin Percentage", 100*profit/total_sale_price)
  if (total_cost != 0):
    print ("  Profit/Cost Percentage", 100*profit/(total_cost))  



  """ Select custom_lable, cost from package_cost and store in a dictionary
  """

  """ Close database
  """
  db.closeDatabase()


def calculate(db_name,sql_string):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  print (sql_string)
  """ Select custom_lable, cost from package_cost and store in a dictionary
  """
  package_cost_dict = {}
  sql_string2 = "SELECT custom_lable, cost FROM package_cost"
  cursor = db.selectSQL(sql_string2)
  for row in cursor:
    package_cost_dict[row[0]] = row[1]
    
  """ Select sales_record_number, custom_lable and cost from item_cost by using 
  inner join with sales_tbl, stock and sku_tbl 
  """
  print ("Reading sale records")

  total_sale_price = total_postage = total_cost = total_shipping = total_package_cost = 0.0
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    total_sale_price += float(row[1])
    total_postage += float(row[2])
    total_cost += float(row[3])
    total_shipping += float(row[4])
    if row[5] in package_cost_dict:
      total_package_cost += float(package_cost_dict[row[5]])
    else:
      print (str(row[5])+" not in package_cost")

  print ("Total")
  print ("  Sales",total_sale_price)
  print("  Postage Paid By Buyer",total_postage)
  print("  Cost",total_cost)
  print ("  Total Package cost",total_package_cost)
  print("  Shipping",total_shipping)
  print("  Ebay+Paypal charges",total_sale_price*0.15)
  #profit = total_sale_price-total_sale_price*0.15-total_cost-total_shipping-total_package_cost
  profit = total_sale_price+total_postage-total_sale_price*0.15-total_cost-total_shipping
  print("  Profit ",profit)
  print ("  Margin Percentage", 100*profit/total_sale_price)
  print ("  Profit/Cost Percentage", 100*profit/(total_cost+total_package_cost))

  """ Close database
  """
  db.closeDatabase()

# parse command line
p = OptionParser(usage="""usage: %prog [options]
Calculate profit for a given period

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

if len(args) < 2:
  print "Input paramaters should be greater than one"
  sys.exit(0)
elif len(args) ==2:
  (start_date, end_date) = args
  if (store_type=="web"):
    sql_string = "SELECT a.sales_record_number FROM shipping_tbl a INNER JOIN web_item_cost b ON\
    a.sales_record_number = b.sales_record_number INNER JOIN web_sales_tbl c ON b.sales_record_number=c.sales_record_number\
    WHERE c.sale_date>='"+start_date+"' AND c.sale_date<='"+end_date+"'"
    
    calculate_web_sales(db_name,sql_string)

  if (store_type=="ebay"):
    sql_string = "SELECT a.sales_record_number,a.sale_price,\
    a.postage, b.cost, b.shipping, a.custom_lable FROM "\
    +store_type+"_sales_tbl a INNER JOIN "+store_type+"_item_cost b\
     ON a.sales_record_number=b.sales_record_number WHERE \
    a.sale_date>='"+start_date+"' AND a.sale_date<='"+end_date+"'"
    # print(sql_string)
    # sys.exit(0)
    calculate_ebay_sales(db_name,sql_string)
    

elif len(args) == 3:
  (start_date, end_date, item) = args
  sql_string = "SELECT a.sales_record_number from shipping_tbl a inner join web_item_cost b on\
  a.sales_record_number = b.sales_record_number inner join web_sales_tbl c on b.sales_record_number=c.sales_record_number\
  WHERE c.sale_date>='"+start_date+"' and c.sale_date<='"+end_date+"' AND c.custom_lable='"+item+"'"


#calculate_web_sales(db_name,sql_string)

sys.exit(0)



