#!/usr/bin/env python
#import vtk
#reader = vtk.vtkDataSetReader()
#reader.SetFileName("frame1.vtu")
import glob
#import MySQLdb
import pymysql
import csv
import os
import sys
import re
import datetime
import math
from optparse import OptionParser, OptionValueError
from dateutil import parser
from re import sub
from decimal import Decimal

sales_record_no = []
user_id = []
buyer = []
phone = [] 
email = []
address_1 = []
address_2 = []
city = []
state = []
postcode = []
country = []
item_id = []
transaction_id = []
item_title = []
quantity = []
sale_price = []
postage = []
total_price = []
payment_method = []
paypal_transaction_id = []
sale_date = []
checkout_date = []
paid_date = []
posted_date = []
feedback_received = []
variation = []
post_to_address1 = []
post_to_address2 = []
post_to_city = []
post_to_state = []
post_to_post_code = []
post_to_country = []
custom_label = []
previous_record = 0
previous_data = ' '
previous_address_1 = ' '
previous_address_2 = ' '
previous_city = ' '
previous_name = ' '
previous_postage = 0.0
# Variables to store stock data                                                                                                                        
code = []
wholesale_price = []
quantity = []
margin = 0
sale_method = []
profit_margin = []

sale_method_dict = {}

# Read CSV file which contains suppliers stock                                                                                                         
def readCSVStock(list_of_files):
  for filename in list_of_files:
    print "Reading ",filename
    with open(filename, 'rb') as csvfile:
      spamreader = csv.DictReader(csvfile)
      for row in spamreader:
        if row['Code'] !='':
          code.append(str.strip(row['Code']))
          item_title.append(row['Description'])
          wholesale_price.append(row['Wholesale Price'])
          quantity.append(row['Qty'])
      
    csvfile.close()
#  print code
  return code

# Read CVS file which contains ebay sales
def readCSVFile(infile):
  with open(infile, 'rb') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
      sales_record_no.append(row['Sales Record Number'])
      user_id.append(row['User ID'])
      buyer.append(row['Buyer Fullname'])
      phone.append(row['Buyer Phone Number'])
      email.append(row['Buyer Email'])
      address_1.append(row['Buyer Address 1'])
      address_2.append(row['Buyer Address 2'])
      city.append(row['Buyer City'])
      state.append(row['Buyer State'])
      postcode.append(row['Buyer Postcode'])
      country.append(row['Buyer Country'])
      item_id.append(row['Item ID'])

      transaction_id.append(row['Transaction ID'])
      item_title.append(row['Item Title'])
      quantity.append(row['Quantity'])
      sale_price.append(row['Sale Price'])
      postage.append(row['Postage and Handling'])

      total_price.append(row['Total Price'])
      payment_method.append(row['Payment Method'])
      paypal_transaction_id.append(row['PayPal Transaction ID'])
      sale_date.append(row['Sale Date'])
      checkout_date.append(row['Checkout Date'])
      paid_date.append(row['Paid on Date'])
      posted_date.append(row['Posted on Date'])
      feedback_received.append(row['Feedback Received'])
      variation.append(row['Variation Details'])
      post_to_address1.append(row['Post To Address 1'])
      post_to_address2.append(row['Post To Address 2'])
      post_to_city.append(row['Post To City'])
      post_to_state.append(row['Post To State'])
      post_to_post_code.append(row['Post To Postcode'])
      post_to_country.append(row['Post To Country'])
      custom_label.append(row['Custom Label'])

  # Check for empty values
  for i in range(len(address_2)):
   if (address_1[i] == ''): address_1[i] = ' '
   if (address_2[i] == ''): address_2[i] = ' '
   if (user_id[i] == ''): user_id[i] = ' '
   if (buyer[i] == ''): buyer[i] = ' '
   if (phone[i] == ''): phone[i] = ' '
   if (feedback_received[i] == ''): feedback_received[i] = ' '
   if (email[i] == ''): email[i] = ' '
   if (city[i] == ''): city[i] = ' '
   if (state[i] == ''): state[i] = ' '
   if (item_title[i] == ''): item_title[i] = ' '
   if (quantity[i] == ''): quantity[i] = 0
   if (postcode[i] == ''): postcode[i] = ' '
   if (country[i] == ''): country[i] = ' '
   if (variation[i] == ''): variation[i] = ' '
   if (paypal_transaction_id[i] == ''): paypal_transaction_id[i] = ' '
   if (item_id[i] == ''): item_id[i] = ' '
   if (sale_price[i] == ''): sales_price[i] = 'AU $0.0'
   if (postage[i] == ''): postage[i] = 'AU $0.0'

   #print '---------------------------\n'
   #money = Decimal(sub(r'[^\d.]', '', sale_price[0]))
   #print money
   #sys.exit(0)

# Read stock table to get sale_method
def readStockTable():
  try:
    db = pymysql.connect("localhost","cito","citoKUKU123","ebay_database" )
  except:
    print "Database not connected"
  
  cursor = db.cursor()
  try:
    cursor.execute("SELECT custom_lable, sale_method FROM stock")
    for row in cursor:
      sale_method_dict[row[0]] = row[1]
    db.commit() 
  except:
    print "CANNOT READ stock table"
    db.rollback()
  #print sale_method_dict


# Update available quantities in stock table 
def updateStockTable(mrg, code):
  # Open database connection                                                                                                                                     
  try:
    db = pymysql.connect("localhost","cito","citoKUKU123","ebay_database" )
  except:
    print "Database not connected"
  count = 0
  # prepare a cursor object using cursor() method                                                                                                                                
  postage = 12.0  #Dropshipper shipping charges per order
  handling = 1.15 #Charges by dropshiiper
  gst = 1.1 #Dropshipper GST 
  shipping = 7.60 #Postage cost for shipping
  shipping2 = 6.0
  min_price = 8.00 #if the wholesale price is less than this value set margin to two fold

  cursor = db.cursor()
  for i in range(0,len(code)):
    if code[i] == 'PP1012':
      print code[i]

    #if code[i] in sale_method_dict.keys():
    #  print sale_method_dict[code[i]]
    if float(wholesale_price[i]) > 0.0:
    # execute SQL query                                                                                                                                          
      try:
      # Execute the SQL command                                                          
      # Commit changes in the database                                                                                                                           
        cursor.execute("UPDATE stock set units="+quantity[i]+", cost="+wholesale_price[i]+" WHERE custom_lable='"+str(str.strip(code[i]))+"'")
        #cursor.execute("UPDATE stock set units="+quantity[i]+" WHERE custom_lable='"+str(str.strip(code[i]))+"'")
        db.commit()
        
        if code[i] in sale_method_dict.keys():
          if (sale_method_dict[code[i]] == 1): # Dropshipping                                                                              
            sale_price = math.ceil(10*((float(wholesale_price[i])*handling+postage)*gst/(1.0-mrg/100.0)-shipping))/10
            cost = (float(wholesale_price[i])*handling+postage)*gst
            cursor.execute("UPDATE stock set sale_price="+str(sale_price)+", cost="+str(cost)+" WHERE custom_lable='"+str(code[i])+"'")
            db.commit()
            count += 1
          elif (sale_method_dict[code[i]] == 2): # Direct sale with GST charges by the supplier(Without dropshipping) 
            mrg1 = mrg      
            if float(wholesale_price[i]) < min_price:
              mrg1 = mrg*2.0
            else:
              mrg1 = mrg*1.5
            sale_price = math.ceil(10*(float(wholesale_price[i])*gst/(1.0-mrg1/100.0)))/10
            cost = float(wholesale_price[i])*gst        
            cursor.execute("UPDATE stock set sale_price="+str(sale_price)+", cost="+str(cost)+" WHERE custom_lable='"+str(code[i])+"'")
            db.commit()
            count += 1
          elif (sale_method_dict[code[i]] == 3): # Direct sale with wholesale price  
            mrg2 = mrg
            sale_price = shipping2+math.ceil(10*(float(wholesale_price[i])/(1.0-mrg2/100.0)))/10
            #sp = math.ceil(sale_price)
            cost = float(wholesale_price[i])
            cursor.execute("UPDATE stock set sale_price="+str(sale_price)+", cost="+str(cost)+" WHERE custom_lable='"+str(code[i])+"'")
            db.commit()
            count += 1 
          else:
            mrg2 = mrg
            sale_price = shipping2+math.ceil(10*(float(wholesale_price[i])/(1.0-mrg2/100.0)))/10
            cost = float(wholesale_price[i])
            cursor.execute("UPDATE stock set sale_price="+str(sale_price)+", cost="+str(cost)+" WHERE custom_lable='"+str(code[i])+"'")
            db.commit()
            count += 1

      except:
        # Rollback in case there is any error                                                                                                                    
        print "RECORD "+code[i]+" NOT UPDATED"
        db.rollback()
# disconnect from server                                                                                                                                         
  if db:
    db.close()

# Insert new records into sales_tbl
def updateSalesTable():
  # sales_record_number of the last row in sales_tbl
  last_record = 0
  # Keep a track of previous sales_record_number
  global previous_record, previous_data, previous_address_1, previous_address_2, previous_city, previous_name, previous_postage
  # Open database connection
  try:
    db = pymysql.connect("localhost","cito","citoKUKU123",db_name )
  except:
    print "Database not connected"

  count = 0
  # prepare a cursor object using cursor() method
  cursor = db.cursor()

  # Find maximum sales_record_number in sales_tbl    
  try:
    cursor.execute("select max(sales_tbl.sales_record_number) from sales_tbl")
    for row in cursor:
      last_record = row[0]
    db.commit()
  except:
    db.rollback()
  
  for i in range(1,len(sales_record_no)):
    # Check for multiple product selection under the same order
    if (previous_record == int(sales_record_no[i])):
      print 'PREVIOUS RECORD == SALES RECORD NO, Sales Record ',sales_record_no[i],' not entered'
      tuple = previous_data.split()
      postage_cost = previous_postage
      #postage_cost = Decimal(sub(r'[^\d.]', '', 'AU '+tuple[7]))
      try:
        # Execute the SQL command                                                                                                                                
        money = Decimal(sub(r'[^\d.]', '', sale_price[i]))
        #postage_cost = Decimal(sub(r'[^\d.]', '', postage[i]))
        cursor.execute("INSERT INTO sales_tbl (sales_record_number,user_id,buyer_fullname,buyer_email,buyer_phone,feedback,buyer_address_1,buyer_address_2,buyer_city,buyer_state,buyer_postcode,buyer_country,sale_date,paid_date,posted_date,paypal_transaction_id,transaction_id,item_number,item_description,quantity,sale_price,postage,variation,custom_lable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(sales_record_no[i],tuple[0],previous_name,tuple[1],tuple[2],feedback_received[i],previous_address_1,previous_address_2,previous_city,tuple[3],tuple[4],tuple[5],parser.parse(sale_date[i]),parser.parse(paid_date[i]),parser.parse(posted_date[i]),tuple[8],transaction_id[i],item_id[i],item_title[i],quantity[i],money,postage_cost,variation[i],custom_label[i]))
      except:
        print 'DUPLICATE SALES RECORD ',sales_record_no[i],' NOT INSERTED'

    # Check for new sales_record_number. If the new sales_record_number is less than the maximum sales_record_number
    # do not enter that record into sales_tbl
    elif(int(sales_record_no[i]) <= last_record):     
      print 'SALES RECORD NO < LAST RECORD, Sales Record ',sales_record_no[i],' not entered'
    else:
      previous_record = int(sales_record_no[i])
      previous_data = user_id[i]+' '+email[i]+' '+phone[i]+' '+state[i]+' '+postcode[i]+' '+country[i]+' '+postage[i]+' '+paypal_transaction_id[i]+' '+posted_date[i]
      previous_address_1 = address_1[i]
      previous_address_2 = address_2[i]
      previous_city = city[i]
      previous_name = buyer[i]
      previous_postage = Decimal(sub(r'[^\d.]', '', postage[i]))
      # execute SQL query
      try:
        # Execute the SQL command
        money = Decimal(sub(r'[^\d.]', '', sale_price[i]))
        postage_cost = Decimal(sub(r'[^\d.]', '', postage[i]))
        cursor.execute("INSERT INTO sales_tbl (sales_record_number,user_id,buyer_fullname,buyer_email,buyer_phone,feedback,buyer_address_1,buyer_address_2,buyer_city,buyer_state,buyer_postcode,buyer_country,sale_date,paid_date,posted_date,paypal_transaction_id,transaction_id,item_number,item_description,quantity,sale_price,postage,variation,custom_lable)\
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",\
(sales_record_no[i],user_id[i],buyer[i],email[i],phone[i],feedback_received[i],address_1[i],address_2[i],city[i],state[i],postcode[i],country[i],parser.parse(sale_date[i]),parser.parse(paid_date[i]),parser.parse(posted_date[i]),paypal_transaction_id[i],transaction_id[i],item_id[i],item_title[i],quantity[i],money,postage_cost,variation[i],custom_label[i]))

# Testing
#        cursor.execute("INSERT INTO sales_tbl (sales_record_number,user_id,buyer_fullname,buyer_email,buyer_phone,feedback,buyer_address_1,buyer_address_2,buyer_city,buyer_state,buyer_\
#postcode,buyer_country) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sales_record_no[i],user_id[i],buyer[i],email[i],phone[i],feedback_received[i],address_1[i],address_2[i],city[i],state[i],postcode[i],country[i])) 
        # Commit changes in the database                                                                                            
        db.commit()
        count += 1
      except:
        # Rollback in case there is any error
        print "RECORD "+sales_record_no[i]+" NOT INSERTED (database error)"
        db.rollback()

    print "NO OF ITEMS INSERTED "+str(count)
# disconnect from server
  if db:
    db.close()

# Update mypartysupplier_database oc_product_option_value.quantity
def updateMPSDatabase(database):
  # Open ebay_database and read sku, variation, units and store them in a list
  stock_sku = []
  stock_variation = []
  stock_units = []
  stock_price = []
  try:
    db = pymysql.connect("localhost","cito","citoKUKU123","ebay_database" )
  except:
    print "eBay_database not connected"
  # prepare a cursor object using cursor() method                                                                                                          
  cursor = db.cursor()

  try:
    cursor.execute("SELECT sku,variation,units,sale_price FROM stock WHERE sale_price IS NOT null")
    for row in cursor:
      stock_sku.append(row[0])
      stock_variation.append(row[1])
      stock_units.append(row[2])
      stock_price.append(row[3])
    db.commit()
  except:
    db.rollback()

  if db:
    db.close()

  # Open mypartysupplier_database and get product_id which are correspond to the sku values stored in stock_sku
  product_id = []
  try:
    db = pymysql.connect("localhost","cito","citoKUKU123",database )
  except:
    print "mypartysupplier_database not connected"
  # prepare a cursor object using cursor() method
  for i in range(len(stock_sku)): product_id.append(-1)                                                                                                          
  cursor = db.cursor()
  for i in range(len(stock_sku)):
    try:
      cursor.execute("select product_id from oc_product where sku='"+stock_sku[i]+"'")
      for row in cursor:
        product_id[i] = row[0]
      db.commit()
    except:
      db.rollback()

  # Update quantity and price for all the products that are in oc_product table
  for i in range(len(product_id)):
    if product_id[i] > 0: # update only products which are available in oc_product table
      if stock_variation[i] == 'none': # Update products which have no variation
        try:
          cursor.execute("UPDATE oc_product SET quantity="+str(stock_units[i])+" WHERE product_id="+str(product_id[i]))
          cursor.execute("UPDATE oc_product SET price="+str(stock_price[i])+" WHERE product_id="+str(product_id[i]))
          db.commit()
        except:
          print "oc_product "+stock_sku[i]+" NOT UPDATED"
          db.rollback()
      else: # Default quantity for products which have no variation is set to 100
        try:
          cursor.execute("UPDATE oc_product SET quantity=100 WHERE product_id="+str(product_id[i]))
          cursor.execute("UPDATE oc_product SET price="+str(stock_price[i])+" WHERE product_id="+str(product_id[i]))
          db.commit()
        except:
          print "oc_product "+stock_sku[i]+" NOT UPDATED"
          db.rollback()

  # Open mypartysupplier_database and get product_option_value_id
  product_option_value_id = []
  avail_quantity = []

  for i in range(len(product_id)):
    if int(product_id[i]) > 0:
      # Get price for products with variation
       if(stock_variation[i] != 'none'): # Products with variation
        try:
          cursor.execute("select a.product_option_value_id, b.name from oc_product_option_value a, oc_option_value_description b where a.option_value_id=b.option_value_id and a.product_id="+str(product_id[i])+" and b.name='"+stock_variation[i]+"'")
          for row in cursor:
            product_option_value_id.append(row[0])
            avail_quantity.append(stock_units[i])
          db.commit()
        except:
          db.rollback()

  # Update products which have variation (oc_product_option_value.quantity)
  for i in range(len(product_option_value_id)):
    try:
      cursor.execute("UPDATE oc_product_option_value SET quantity="+str(avail_quantity[i])+" WHERE product_option_value_id="+str(product_option_value_id[i]))
      db.commit()
    except:
      print "oc_product_option_value NOT UPDATED"
      db.rollback()
  if db:
    db.close()# Close mps_database                

# Return the postion of 'ch' in 'line'
def find(str, ch):
  string_list = []
  list =[]
  for i, ltr in enumerate(line):
    if ltr == ',':
      list.append(i)
  start_index = 0
  for i in range(0,len(list)-1):
    #print start_index
    end_index = int(list[i])
    
    str = line[start_index:end_index]
    string_list.append(str)

    start_index = end_index
    end_index = int(list[i+1])
  return string_list


# parse command line
p = OptionParser(usage="""usage: %prog [options] <inputfile>

Ex: 
./salereport.py -r 'sales.csv' : Read sale records and insert new records into sales_tbl
./salereport.py -u 'product-feed.csv : Read suppliers products feeds and update "stock", "oc_product" and "oc_product_option_value" tables   
""")
#p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-r", "--read", action="store", type="str", default="none", dest="readcsv", help="Read ebay sales history CSV file and insert sale records in sales_tbl")
p.add_option("-d", "--dbase", action="store", type="str", default="ebay_database", dest="readdb", help="Database options ebay_database, cg_database Default database=ebay_database")
p.add_option("-m", "--margin", action="store", type="int", default=30, dest="setmargin", help="Update available quntity and sale price accoring to the margin entered by the user: Profit margin = (sale_price-cost)/sale_price")
#p.add_option("-m", "--margin", action="store", type="int", default=30, dest="updatedb", help="Up")
(opts, args) = p.parse_args()

# read input output files
#if len(args) < 1:
#   print 'check input and output files'
#   sys.exit(0)
#(outfile) = args
if opts.readdb:
  db_name = opts.readdb

if opts.readcsv: 
  fname = opts.readcsv
  if fname != 'none':
    print "Reading CSV file "+fname 
    readCSVFile(fname)
    print "Updating sales_tbl"
    updateSalesTable()
  #else:# opts.readstock != 'none':
  #  database = opts.readdb
  #  margin = opts.setmargin
  #  print "Margin "+str(margin) 
  #  list_of_files = glob.glob('../suppliers/*.csv')    
  #  code = readCSVStock(list_of_files) #Read CSV file which is provided by the supplier
  #  print "Reading stock table"
  #  readStockTable()
  #  print "Updating stock table"
  #  updateStockTable(margin, code) #Update quantity, sale_price, ebay_price, margin of stock table in ebay_database
  #  print "Updating website database"
  #  updateMPSDatabase(database)

print "DONE"
sys.exit(0)







