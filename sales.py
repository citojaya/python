""" Update item_cost table
    option -d defines database name and option -f defines input CSV file which contains shipping cost
"""
import sys
import csv
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub


def insertRecord(db_name,f_name):
  """ Get database connection
  """
  user = "cito"
  passwd = "citoKUKU123"

  db = Database(db_name,user,passwd)
  db.getConnection()


  """ Read CSV file which contains ebay sales
  """
  print ("Reading CSV file "+f_name)
  # csvfile = Fileio(f_name)
  # dataset = csvfile.getDataSet()

  #print ("Inserting into item_cost table")
  previous_record = 0

  with open(f_name) as csvfile:
    dataset = csv.DictReader(csvfile)

    for dict in dataset:
      record_exists = False
      #print (dict['Sales Record Number'])
      if (dict['Sale Price']):
        sale_price = Decimal(sub(r'[^\d.]', '', dict['Sale Price']))
      if (dict['Postage and Handling']):
        postage=Decimal(sub(r'[^\d.]', '', dict['Postage and Handling']))
      else:
        postage = 0.0

      if (previous_record != dict['Sales Record Number']):
        # Check for an existing record, suppossed to be the fastest method to check
        sql_string="SELECT EXISTS(SELECT 1 FROM ebay_sales_tbl WHERE sales_record_number ="+dict['Sales Record Number']+" LIMIT 1)"
        cursor = db.selectSQL(sql_string)

        for row in cursor: #cursor has only one row
          if row[0] == 1: #record exists
            record_exists = True
      if (record_exists == False):
        paid_on_date = ""
        posted_on_date = ""
        buyer_phone =""
        transaction_id = dict['Transaction ID']
        item_id = dict['Item ID']
        if dict['Paid on Date'] == "":
          paid_on_date = "0000-01-01"
        else:
          paid_on_date = str(parser.parse(dict['Paid on Date']))
        if dict['Posted on Date'] == "":
          posted_on_date = "0000-01-01"
        else:
          posted_on_date = str(parser.parse(dict['Posted on Date']))
        if transaction_id == "":
          transaction_id = 0
        if item_id =="":
          item_id = 0

        sql_string = "INSERT INTO ebay_sales_tbl (sales_record_number,user_id,buyer_fullname,buyer_phone,buyer_email,\
        buyer_address_1,buyer_address_2,buyer_city,buyer_state,\
        buyer_postcode,buyer_country,item_description,\
        quantity,sale_price,postage,sale_date,paypal_transaction_id,transaction_id,item_number,\
        paid_date,posted_date,feedback,custom_lable,variation)\
        VALUES ("+dict['Sales Record Number']+\
          ",'"+dict['User ID']+"'"+\
          ",'"+dict['Buyer Fullname'].replace("'"," ")+"'"+\
          ",'"+dict['Buyer Phone Number']+"'"+\
          ",'"+dict['Buyer Email']+"'"+\
          ",'"+dict['Post To Address 1'].replace("'"," ")+"'"+\
          ",'"+dict['Post To Address 2'].replace("'"," ")+"'"+\
          ",'"+dict['Post To City']+"'"+\
          ",'"+dict['Post To State']+"'"+\
          ",'"+dict['Post To Postcode']+"'"+\
          ",'"+dict['Post To Country']+"'"+\
          ",'"+dict['Item Title'].replace("'"," ")+"'"+\
          ","+dict['Quantity']+\
          ","+str(sale_price)+\
          ","+str(postage)+\
          ",'"+str(parser.parse(dict['Sale Date']))+"'"+\
          ",'"+dict['PayPal Transaction ID']+"'"+\
          ","+str(transaction_id)+\
          ","+str(item_id)+\
          ",'"+paid_on_date+"'"+\
          ",'"+posted_on_date+"'"+\
          ",'"+dict['Feedback Received']+"'"+\
          ",'"+dict['Custom Label']+"'"+\
          ",'"+dict['Variation Details']+"'"+\
          ")"
        if(db.insertSQL(sql_string)):
          previous_record = dict['Sales Record Number'] # Keep a record of sales record number which is used for multiple records
          print ("Record "+dict['Sales Record Number']+" inserted")
        else:
          print ("Record "+dict['Sales Record Number']+" NOT inserted")
          print (sql_string)
        
      elif(record_exists == True):
        print("Record "+dict['Sales Record Number']+" exist")

  """ Close database
  """
  db.closeDatabase()

# parse command line
p = OptionParser(usage="""usage: %prog [options]
Read the CSV file containing ebay sales and insert new records into ebay_sales_tbl

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
if opts.readf == "NONE":
  print ("CSV file not defined")
  sys.exit(0) 
elif opts.readdb == "ct_database":
  db_name = opts.readdb
  f_name = opts.readf
  insertRecord(db_name,f_name)
elif opts.readdb == "cg_database":
  db_name = opts.readdb
  f_name = opts.readf
  insertRecord(db_name,f_name)


sys.exit(0)


