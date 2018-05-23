import unicodecsv

class Fileio:
	""" This module is used for input and output files
	"""
	def __init__(self, filename):
		""" 
    	Args:
    		filename(string): Name of the CSV file
    	Attributes:
    		filename(string): Name of the CSV file
		"""
		self.filename = filename

	def getDataSet(self):
		""" Returns a list of dictionaries which contains data in the CSV file
    	Returns:
    		list: A list of dictionaries which contains data 
    	""" 
		with open(self.filename, 'rb') as f:
			reader = unicodecsv.DictReader(f)
			dataSet = list(reader)
			return dataSet