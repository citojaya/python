""" Insert sale records into web_sales_tbl
    option -d defines database name
    Read oc_order, oc_order_product and oc_order_total and insert sales record into web_sales_tbl
"""
import sys
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub

sales_record = {}

def read_oc_order_product(db_name):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  sql_string = "select a.order_id, a.name, a.model, a.quantity, a.price from oc_order_product a inner join \
  oc_order b on a.order_id=b.order_id where b.order_status_id>0"
  cursor = db.selectSQL(sql_string)

  previous_record = 0
  for row in cursor:
    record_exists = False
    if (previous_record != row[0]):
      # Check for an existing record, suppossed to be the fastest method to check
      sql_string="SELECT EXISTS(SELECT 1 FROM web_sales_tbl WHERE sales_record_number ="+str(row[0])+" LIMIT 1)"
      cursor2 = db.selectSQL(sql_string)

      for row2 in cursor2: #cursor has only one row
        if row2[0] == 1: #record exists
          record_exists = True
    if (record_exists == False):
      sales_record [row[0]] = row[0]
      sql_string = "INSERT INTO web_sales_tbl (sales_record_number,item_description, custom_lable,\
      quantity,sale_price)\
      VALUES ("+str(row[0])+\
          ",'"+row[1]+"'"+\
          ",'"+row[2]+"'"+\
          ","+str(row[3])+\
          ","+str(row[4])+")"
      if(db.insertSQL(sql_string)):
        previous_record = row[0] # Keep a record of sales record number which is used for multiple records
        print("Record "+str(row[1])+" inserted")
      else:
        print("Record "+str(row[1])+" NOT inserted")
    elif(record_exists == True):
      print("Record "+str(row[0])+" exist")
    #print(sql_string)

  # Insert sales_record_number into shipping_tbl
  for k,v in sales_record.iteritems():
    sql_string = "INSERT INTO shipping_tbl (sales_record_number) VALUES("+str(k)+")"
    db.insertSQL(sql_string)
    #print(sql_string)

  """ Close database
  """
  db.closeDatabase()


def read_oc_order(db_name):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  sql_string = "select order_id, shipping_firstname, shipping_lastname, email, shipping_address_1,\
  shipping_address_2, shipping_city, shipping_postcode, shipping_country,\
  date_added, total from oc_order"

  cursor = db.selectSQL(sql_string)
  for row in cursor:
    sql_string = "UPDATE web_sales_tbl SET buyer_fullname='"+row[1]+" "+row[2]+"',\
    buyer_email='"+row[3]+"',buyer_address_1='"+row[4]+"',buyer_address_2='"+row[5]+"',\
    buyer_city='"+row[6]+"',buyer_postcode='"+row[7]+"',buyer_country='"+row[8]+"',\
    sale_date='"+str(parser.parse(str(row[9])))[:10]+"' WHERE sales_record_number="+str(row[0]) 
    db.updateSQL(sql_string)
    #print(sql_string)
  """ Close database
  """
  db.closeDatabase()

def read_oc_order_total(db_name):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()

  # Get discount from oc_order_total and update shipping_tbl
  sql_string = "SELECT order_id,value FROM oc_order_total WHERE code='coupon'"
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    sql_string = "UPDATE shipping_tbl SET discount="+str(row[1])+"\
    WHERE sales_record_number="+str(row[0])
    db.updateSQL(sql_string)
    #print(sql_string)

  # Get shipping from oc_order_total and update shipping_tbl
  sql_string = "SELECT order_id,value FROM oc_order_total WHERE code='shipping'"
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    sql_string = "UPDATE shipping_tbl SET shipping="+str(row[1])+"\
    WHERE sales_record_number="+str(row[0])
    db.updateSQL(sql_string)
    #print(sql_string)

 # Get total from oc_order_total and update shipping_tbl
  sql_string = "SELECT order_id,value FROM oc_order_total WHERE code='total'"
  cursor = db.selectSQL(sql_string)
  for row in cursor:
    sql_string = "UPDATE shipping_tbl SET total="+str(row[1])+"\
    WHERE sales_record_number="+str(row[0])
    db.updateSQL(sql_string)
    #print(sql_string)


  """ Close database
  """
  db.closeDatabase()


# parse command line
p = OptionParser(usage="""usage: %prog [options]
Read oc_order, oc_order_product and oc_order_total and insert sales record into web_sales_tbl

Ex: 
  ./web_sales.py -d cg_database
  -d = database name

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Database Name")
#p.add_option("-f", "--file", action="store", type="str", default="NONE", dest="readf", help="CSV file containing sales")

(opts, args) = p.parse_args()

if opts.readdb == "NONE":
  print("Database not defined")
  sys.exit(0)
else:
  db_name = opts.readdb
  read_oc_order_product(db_name)
  read_oc_order(db_name)
  read_oc_order_total(db_name)

sys.exit(0)


