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
Read the CSV containing sales_record_number and shipping cost and update shipping column in item_cost table
Update cost column in item_cost table

Ex: python update_item_cost.py -d "ebay_database" -f "ebay_file"
 -d = database name
 -f = csv file containing shipping cost

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
#p.add_option("-a", action="store_true", dest="ascii",  help="ASCII, instead of binary, VTK output")
p.add_option("-d", "--dbase", action="store", type="str", default="NONE", dest="readdb", help="Website Database")
p.add_option("-f", "--file", action="store", type="str", default="NONE", dest="readf", help="CSV file containing shipping cost")

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


""" Read CSV file and insert sales_record_number, shipping into item_cost table
"""
print ("Reading CSV file "+f_name+".csv")
csvfile = Fileio(f_name+".csv")
dataset = csvfile.getDataSet()
print ("Inserting into item_cost table")
for dict in dataset:
  seq = str(dict['sales_record_number'])+","+str(dict['shipping'])
  sql_string = "INSERT INTO item_cost (sales_record_number,shipping) VALUES("+seq+")"
  db.insertSQL(sql_string)



""" Read CSV file and update shipping column in item_cost table
"""
# print ("Reading CSV file "+f_name+".csv")
# csvfile = Fileio(f_name+".csv")
# dataset = csvfile.getDataSet()
# print ("Updating shipping values in item_cost table")
# for dict in dataset:
#   seq = str(dict['sales_record_number'])+","+str(dict['shipping'])
#   sql_string = "UPDATE item_cost SET shipping="+str(dict['shipping'])+" WHERE sales_record_number="+str(dict['sales_record_number'])
#   db.updateSQL(sql_string)


""" Select sales_record_number, custom_lable and cost from item_cost by using 
inner join with sales_tbl, stock and sku_tbl 
"""
sql_string = "select a.sales_record_number,b.custom_lable, \
b.quantity*c.units_per_order*d.unit_cost*d.unit_cost_conversion+c.package_cost from item_cost a\
 inner join sales_tbl b on a.sales_record_number=b.sales_record_number\
 inner join sku_tbl c on b.custom_lable=c.custom_lable inner join stock d \
 on c.stock_reference=d.stock_reference"

cursor = db.selectSQL(sql_string)

print ("Updating cost values in item_cost table")
for row in cursor:
  sql_string = "UPDATE item_cost set cost="+str(row[2])+" WHERE sales_record_number="+str(row[0])
  db.updateSQL(sql_string)


""" Select from stock and insert into package_cost
"""
# sql_string = "SELECT stock_reference FROM stock"
# cursor = db.selectSQL(sql_string)
# for row in cursor:
#   sql_string = "INSERT INTO package_cost (custom_lable) VALUES('"+str(row[0])+"')"
#   db.insertSQL(sql_string)
#   print(sql_string)

# print("Sucessfully updated stock table")

""" Close database
"""
db.closeDatabase()
sys.exit(0)


#dataset = csvfile.getDataSet()
# for dict in dataset:
# 	#seq = str(dict['sales_record_number'])+","+str(dict['cost'])
# 	sql_string = "UPDATE cost SET item_cost="+str(dict['item_cost'])+" WHERE sales_record_number="+str(dict['sales_record_number'])
# 	print(sql_string)
# 	db.updateSQL(sql_string)


""" Read cost and shipping from sales_tbl and update records in cost table
"""
# result_set = db.selectSQL("SELECT a.sales_record_number, a.quantity, b.cost, a.shipping from sales_tbl a, stock b \
# 	where a.custom_lable=b.sku and a.sales_record_number >5152 and a.sales_record_number<5476")
# for row in result_set:
# 	sql_string = "INSERT INTO cost(sales_record_number, item_cost) VALUES("+str(row[0])+","+str(row[1]*row[2])+")"
# 	#print sql_string
# 	if (db.insertSQL(sql_string)):
# 		print ("INSERTED "+str(row[0]))
# 	else:
# 		#sql_string = "UPDATE cost set item_cost="+str(row[1]*row[2])+" WHERE sales_record_number="+str(row[0])
# 		sql_string = "UPDATE cost set shipping="+str(row[3])+" WHERE sales_record_number="+str(row[0])
# 		db.updateSQL(sql_string)
		#print(sql_string)
		#print ("NOT INSERTED "+str(r0]))
	#print (row[0],row[1], row[2])

""" Read expenses.csv and insert records into database
"""
# for dict in csvfile.getDataSet():
# 	comma = ","
# 	seq = ("'"+str(parser.parse(dict['Date']))+"'","'"+dict['Description']+"',"+dict['Cost'][1:])
# 	sql = "INSERT INTO expenses_tbl (date, item_description, amount) VALUES ("+comma.join(seq)+")"
# 	print (sql)
# 	ebay_db.insertSQL(sql)
	# if (dict['Cost'] and dict['Description']):
	# 	comma = ","
	# 	seq = ("'"+str(parser.parse(dict['Date']))+"'","'"+dict['Description']+"'","'"+dict['Reference']+"'",dict['Cost'])
	# 	sql = "INSERT INTO expenses_tbl (date, item_description, payment_method, amount) VALUES ("+comma.join(seq)+")"
	# 	print (sql)
	# 	ebay_db.SQL_insert(sql)
		

""" Select shipping cost from sales_tbl and insert those records into shipping table
"""
#sql = "select sales_record_number, shipping from sales_tbl where sale_date>'2017-06-30'"
#cursor = ebay_db.SQL_select(sql)
#for row in cursor:
#	sql = "INSERT IGNORE INTO shipping (sales_record_number, cost) VALUES ("+str(row[0])+","+str(row[1])+")"




#cost = 6.78
#text = "Hello"
#print "{0}\t{1}".format(text, cost)

#print(db.getDatabase())

