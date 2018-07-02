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
Read the CSV file containing ebay sales and insert new records into sales_tbl

Ex: 
./salereport.py -f 'sales.csv' -d ebay_database
 -d = database name
 -f = csv file downloaded from ebay

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Database Name")
p.add_option("-f", "--file", action="store", type="str", default="NONE", dest="readf", help="CSV file containing sales")

(opts, args) = p.parse_args()

if opts.readdb == "NONE":
  print("Database not defined")
  sys.exit(0)
else:
  db_name = opts.readdb

if opts.readf == "NONE":
  print ("CSV file not defined")
  sys.exit(0) 
else:
  f_name = opts.readf

""" Get database connection
"""
user = "cito"
passwd = "citoKUKU123"

db = Database(db_name,user,passwd)
db.getConnection()


""" Read CSV file which contains ebay sales
"""
print ("Reading CSV file "+f_name)
csvfile = Fileio(f_name)
dataset = csvfile.getDataSet()
#print ("Inserting into item_cost table")
for dict in dataset:
  #print (dict['Sales Record Number'])
  sale_price = Decimal(sub(r'[^\d.]', '', dict['Sale Price']))
  postage=Decimal(sub(r'[^\d.]', '', dict['Postage and Handling']))
  sql_string = "INSERT INTO sales_tbl (sales_record_number,user_id,buyer_fullname,buyer_phone,buyer_email,\
  buyer_address_1,buyer_address_2,buyer_city,buyer_state,\
  buyer_postcode,buyer_country,item_description,\
  quantity,sale_price,postage,sale_date,paypal_transaction_id,transaction_id,item_number,paid_date,posted_date,\
  buyer_phone,feedback,custom_lable,variation)\
  VALUES("+dict['Sales Record Number']+\
  ",'"+dict['User ID']+"'"+\
  ",'"+dict['Buyer Fullname']+"'"+\
  ",'"+dict['Buyer Phone Number']+"'"+\
  ",'"+dict['Buyer Email']+"'"+\
  ",'"+dict['Post To Address 1']+"'"+\
  ",'"+dict['Post To Address 2']+"'"+\
  ",'"+dict['Post To City']+"'"+\
  ",'"+dict['Post To State']+"'"+\
  ",'"+dict['Post To Postcode']+"'"+\
  ",'"+dict['Post To Country']+"'"+\
  ",'"+dict['Item Title']+"'"+\
  ","+dict['Quantity']+\
  ","+str(sale_price)+\
  ","+str(postage)+\
  ",'"+dict['Sale Date']+"'"+\
  ",'"+dict['PayPal Transaction ID']+"'"+\
  ",'"+dict['Transaction ID']+"'"+\
  ",'"+dict['Item ID']+"'"+\
  ",'"+dict['Paid on Date']+"'"+\
  ",'"+dict['Posted on Date']+"'"+\
  ",'"+dict['Phone']+"'"+\
  ",'"+dict['Feedback Received']+"'"+\
  ",'"+dict['Custom Label']+"'"+\
  ",'"+dict['Variation Details']+"'"+\
  ")"
  print (sql_string)
  # seq = str(dict['sales_record_number'])+","+str(dict['shipping'])
  # sql_string = "INSERT INTO item_cost (sales_record_number,shipping) VALUES("+seq+")"
  #db.insertSQL(sql_string)


""" Close database
"""
db.closeDatabase()
sys.exit(0)


