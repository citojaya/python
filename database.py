import glob
import pymysql
#import pymysql
import csv
import os
import sys
import re
import datetime
import math
#from optparse import OptionParser, OptionValueError
from dateutil import parser
from re import sub
from decimal import Decimal

""" Module used for mysql database access
"""
class Database:	
	def __init__(self, name, user, pw):
		"""
		Args:
			name(string): Name of the database
			user(string): Database user
			pw(string): Password for database access
		Attributes:
			name(string): Name of the database
			user(string): Database user
			password(string): Password for database access		
		"""
		self.name = name
		self.user = user
		self.password = pw
	
	def getConnection(self):
		""" Get database connection
		Returns: 
			db: Database connection
		"""
		try:
		   self.db = pymysql.connect("localhost", self.user, self.password, self.name)
		   return self.db
		except Exception as e:
			raise
	
	def closeDatabase(self):
		""" Close database connection
		"""
		if self.db:
			self.db.close()
 			
	def selectSQL(self,sql_string):
		""" Execute SQL select command and returns a data set
		Args: 
			sql_string(string): SQL string to be executed
		Returns: 
			cursor: SQL result set
		""" 
		try:
			cursor = self.db.cursor()
			cursor.execute(sql_string)
			self.db.commit()
		except Exception as e:
			self.db.rollback()
			raise
		return cursor
 	
	def insertSQL(self, sql_string):
		""" Execute SQL insert command
		Args: 
			sql_string(string): SQL string to be executed
		Returns: 
			inserted(boolean): If successful return True else False
		"""
		try:
			cursor = self.db.cursor()
			cursor.execute(sql_string)
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			print ("Entry Not Inserted")
	
		return False

	def updateSQL(self, sql_string):
		""" Update database
		Args: 
			sql_string(string): SQL string to be executed
		Returns: 
			inserted(boolean): If successful return True else False
		"""
		try:
			cursor = self.db.cursor()
			cursor.execute(sql_string)
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			print ("Entry Not Updated")
			
		return False
		

#db = Database("ebay_database", "cito", "citoKUKU123")
#db.getDatabse()
