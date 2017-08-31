import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool

class Singleton(object):
	engine = None
	connection = None	

	@staticmethod
	def get_connection(host='localhost', port=3306, user='root', passwd='', db='sentiment_db', charset='utf8mb4', use_unicode=True):
		if Singleton.engine is None:
			Singleton.engine = create_engine('mysql+mysqldb://%s:%s@%s:%d/%s?charset=%s&use_unicode=%d' % (user, passwd, localhost, port, charset, use_unicode), poolclass=SingletonThreadPool)	
		
		Singleton.connection = Singleton.engine.raw_connection()
		return Singleton.connection

class Database(object):
	def __init__(self, host='localhost', port=3306, user='root', passwd='', db='sentiment_db'):
		self.db = db
		self.host = host
		self.port = port
		self.user = user
		self.password = passwd
		self.cursor = None
		self.connection = None

	def connect(self):
		if self.connection is not None:
			print('Connection already exist')
		try:
			self.connection = Singleton.get_connection(
					db = self.db,
					host = self.host,
					port = self.port,
					user = self.user,
					passwd = self.passwd,
					charset = 'utf8mb4',
					use_unicode = True
				)
			self.cursor = self.connection.cursor()
			print('Using database connection %s' % str(self.cursor))
		except MySQLdb.Error as e:
			print('Error in connecting to db: %s' % e)

	def fetch_all(self, select='*', from_clause='', where='', order_by=''):
		sql = 'SELECT %s FROM %s' % (select, from_clause)

		if where != '':
			sql += ' WHERE %s ' % where 

		if order_by != '':
			sql += 'ORDER BY %s' % order_by

		self.cursor.execute(sql)
		return self.cursor.fetch_all()

	def insert(self, table='', column_value={}):
		columns = ''
		values = ''
		for column, value in column_value.items():
			columns += "'%s'," % column
			values += "'%s'," % value

		columns = columns[:-1] # remove last comma (,)
		values = values[:-1] # remove last comma (,)

		sql = "INSERT INTO '%s' VALUES '%s'" % (columns, values)

		try:
			self.cursor.execute("SET @@sql_mode:=''")
			self.cursor.execute(sql)
			self.connection.commit()
			print('Inserting into table: %s' % table)
			print('Setting (%s) to values %s' % (columns, values))
			print("... %d row%s affected" % (self.cursor.rowcount, 's' if self.cursor.rowcount != 1 else ''))
		except MySQLdb.Error as e:
			print('Error inserting in db: %s' % e)
			raise Exception(e)

	def update(self, table='', set={}, where=''):
		set_query = ''
		for column, value in set.items():
			set_query += "'%s' = '%s', " % (column, value)

		set_query = set_query[:-1] # remove last comma (,)
		sql = 'UPDATE %s SET %s WHERE %s' % (table, set_query, where)
		try:
			self.cursor.execute(sql)
			self.connection.commit()
			print("Updating table %s" % table)
			print("Setting %s" % set_query)
			print("Where %s " % where)
			print("... %d row%s affected" % (self.cursor.rowcount, 's' if self.cursor.rowcount != 1 else ''))
		except MySQLdb.Error as e:
			print('Error in updating db: %s' % e)

	def close(self):
		self.cursor.close()
		self.connection.close()
		print('Closing database connection %s' % str(self.cursor))

