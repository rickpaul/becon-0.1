# Taken from https://docs.python.org/2/library/csv.html
# CSV Reader/Writer that handles unicode
# I've modified it to cast as string

import csv, codecs, cStringIO

class UTF8Recoder:
	"""
	Iterator that reads an encoded stream and reencodes the input to UTF-8
	"""
	def __init__(self, f, encoding):
		self.reader = codecs.getreader(encoding)(f)

	def __iter__(self):
		return self

	def next(self):
		n = self.reader.next()
		try:
			return n.encode("utf-8")
		except UnicodeDecodeError:
			return n.decode('iso-8859-1').encode("utf-8")

class UnicodeReader:
	"""
	A CSV reader which will iterate over lines in the CSV file "f",
	which is encoded in the given encoding.
	"""

	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		f = UTF8Recoder(f, encoding)
		self.reader = csv.reader(f, dialect=dialect, **kwds)

	def next(self):
		row = self.reader.next()
		return [unicode(s, "utf-8") for s in row]

	def __iter__(self):
		return self

class UnicodeWriter:
	"""
	A CSV writer which will write rows to CSV file "f",
	which is encoded in the given encoding.
	"""


	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		# Redirect output to a queue
		self.queue = cStringIO.StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
		self.stream = f
		self.encoder = codecs.getincrementalencoder(encoding)()
		self.ERROR_STRING = 'ERROR'.encode("utf-8")

	def encodeString(self, s):
		'''
		TODOS:
					Deal with error better
		'''
		try:
			if type(s) == unicode or type(s) == str:
				s = s.replace(u'\u201c', u'\u0022') # "
				s = s.replace(u'\u201d', u'\u0022') # "
				s = s.replace(u'\u2018', u'\u0027') # '
				s = s.replace(u'\u2019', u'\u0027') # '
				return s.encode('utf-8')
			elif type(s) == int or type(s) == float:
				return str(s).encode('utf-8')
		except UnicodeEncodeError:
			print 'Encode error ', s
			return s.encode('utf-8', 'ignore')
		except Exception as e:
			return self.ERROR_STRING

	def writerow(self, row):
		for s in row:
			self.encodeString(s)
		self.writer.writerow([self.encodeString(s) for s in row])
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		data = data.decode("utf-8")
		# ... and reencode it into the target encoding
		data = self.encoder.encode(data)
		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)