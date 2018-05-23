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
Calculate profit for a given period

Ex: calculate_profit.py <date1> <date2> <database> <sku>
 date1 = starting date
 date2 = end date
 sku = item to be checked

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")

(opts, args) = p.parse_args()

if len(args) < 3:
  print "Input paramaters should be greater than two"
elif len(args) ==3:
  (start_date, end_date, database) = args
  sql_string = "select a.sales_record_number,a.sale_price,\
  a.postage, b.cost, b.shipping, a.custom_lable from sales_tbl a\
  inner join item_cost b on a.sales_record_number=b.sales_record_number where b.cost is not null\
  and a.sale_date>='"+start_date+"'and a.sale_date<='"+end_date+"'"
  print (sql_string)

elif len(args) == 4:
  (start_date, end_date, database, item) = args
  sql_string = "select a.sales_record_number,a.sale_price,\
  a.postage, b.cost, b.shipping, a.custom_lable from sales_tbl a\
  inner join item_cost b on a.sales_record_number=b.sales_record_number where b.cost is not null\
  and a.sale_date>='"+start_date+"'and a.sale_date<='"+end_date+"'and custom_lable='"+item+"'"

# sys.exit(0)

""" Get database connection
"""
user = "cito"
passwd = "citoKUKU123"

db = Database(database,user,passwd)
db.getConnection()

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
cursor = db.selectSQL(sql_string)

print ("Reading sale records")
total_sale_price = total_postage = total_cost = total_shipping = total_package_cost = 0.0

for row in cursor:
  total_sale_price += float(row[1])
  total_postage += float(row[2])
  total_cost += float(row[3])
  total_shipping += float(row[4])
  if row[5] in package_cost_dict:
    total_package_cost += float(package_cost_dict[row[5]])
  else:
  	print (str(row[5])+" not in package_cost")
  
  # print(row[0],row[1],row[2],row[3])
print ("Total")
print ("  Sales",total_sale_price)
print("  Postage Paid By Buyer",total_postage)
print("  Cost",total_cost)
print("  Shipping",total_shipping)
print("  Ebay+Paypal charges",total_sale_price*0.15)
profit = total_sale_price-total_sale_price*0.15-total_cost-total_shipping
print("  Profit ",profit)
print ("  Margin Percentage", 100*profit/total_sale_price)
print ("  Profit/Cost Percentage", 100*profit/total_cost)

""" Close database
"""
db.closeDatabase()
sys.exit(0)



