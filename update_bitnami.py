""" Read ct_database and Update bn_database
    
"""
import sys
import datetime
from optparse import OptionParser, OptionValueError
from dateutil import parser
from database import Database
from fileio import Fileio
from decimal import Decimal
from dateutil import parser
from re import sub


# parse command line
p = OptionParser(usage="""usage: %prog [options]
Read records from source database and update destination database

Ex: python update_bitnami.py
 
 
""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
#p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Website Database")

(opts, args) = p.parse_args()

# if opts.readdb == "NONE":
#   print("Database not defined")
#   sys.exit(0)
# else:
#   db_name = opts.readdb


""" Get database connection
"""
user = "cito"
passwd = "citoKUKU123"

db1 = "ct_database" # source database
db2 = "bn_database" # destination database

ct_sku_prod_id = {}
ct_product = {}
ct_product_disc = {}

""" Read records from first database and store in a dictionary
"""
db = Database(db1,user,passwd)
db.getConnection()
sql_string = "SELECT sku,product_id,image,price,date_available from oc_product"
cursor = db.selectSQL(sql_string)

for row in cursor:
  ct_sku_prod_id[row[0]] = row[1]
  #ct_product[row[1]] = ' '.join([str(row[2]),str(row[3]),str(row[4])])
  ct_product[row[1]] = [row[2],row[3],row[4]]
  

sql_string = "SELECT product_id,name,description,meta_title,meta_description,meta_keyword from oc_product_description"
cursor = db.selectSQL(sql_string)
for row in cursor:
  #ct_product_disc[row[0]] = ' '.join([str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5])])
  ct_product_disc[row[0]] = [row[1],row[2],row[3],row[4],row[5]]
db.closeDatabase()

""" Map bn_database prodcut_id and ct_database product_id
"""
bn_sku_prod_id = {}
db = Database(db2,user,passwd)
db.getConnection()
sql_string = "SELECT product_id,sku from oc_product"
cursor = db.selectSQL(sql_string)
for row in cursor:
  bn_sku_prod_id[row[1]] = row[0]

bn_ct_prod_id = {}

for k,v in bn_sku_prod_id.iteritems():
  bn_ct_prod_id[v] = ct_sku_prod_id[k]
  #print(v,ct_sku_prod_id[k])


#sys.exit(0)
""" Update bn_database
k - product_id in bn_database
v - product_id in ct_database
"""
for k,v in bn_ct_prod_id.iteritems():
  print (k,v)
  #Update oc_product in bn_database  
  #data = ct_product[v].split()

  sql_string = "UPDATE oc_product set image='"+ct_product[v][0]+"', price="+str(ct_product[v][1])+", \
  date_available='"+str(ct_product[v][2])+"' WHERE product_id="+str(k)
  
  #print(sql_string)
  db.updateSQL(sql_string)

  # data = ct_product_disc[v].split()
  sql_string = "UPDATE oc_product_description SET name='"+ct_product_disc[v][0]+\
  "',description='"+ct_product_disc[v][1].replace("'"," ")+\
  "',meta_title='"+ct_product_disc[v][2]+\
  "',meta_description='"+ct_product_disc[v][3]+\
  "',meta_keyword='"+ct_product_disc[v][4]+"' WHERE product_id="+str(k)
  print(sql_string)
  db.updateSQL(sql_string)
db.closeDatabase()

#"',description='"+ct_product_disc[v][1].replace('"',' ')+\

sys.exit(0)


