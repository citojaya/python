""" Calculate profit for a given period
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

user_id = []

def read_userid(f_name):
  print ("Reading CSV file "+f_name)
  with open(f_name) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      user_id.append(row['user_id'])
      #print(row['user_id'])
  return user_id

def get_ebay_customers(db_name, u_id):
  user = "cito"
  passwd = "citoKUKU123"
  email_list = []

  """ Get database connection
  """
  db = Database(db_name,user,passwd)
  db.getConnection()
  for user_name in u_id:
    sql_string = "SELECT  buyer_email, buyer_fullname FROM ebay_sales_tbl WHERE \
    user_id='"+user_name+"'"
    print(sql_string)
    # prepare a cursor object using cursor() method
    cursor = db.selectSQL(sql_string)
    for row in cursor:
      # 1-customer name
      # 0-email
      email_list.append(str(row[0])+"\n")
 
  """ Close database
  """
  db.closeDatabase()

  f = open("email_list-1month.dat","w")
  f.writelines(email_list)
  f.close()

# parse command line
p = OptionParser(usage="""usage: %prog [options]
Extract email and buyer_name from sales


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

# if len(args) < 1:
#   print "Input paramaters should be greater than one"
#   sys.exit(0)

if (store_type=="ebay"):
  u_id = read_userid("../../CinnamonGarden/MailchimpCampaign/positive-feedback-list-1month.csv")
  get_ebay_customers(db_name,u_id)
    

sys.exit(0)



