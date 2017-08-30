import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool

class Singleton(object):
	engine = None
	connection = None	

	@staticmethod
	def get_connection(host='localhost', port=3306, user='root', passwd='', db='sentiment_db', charset='utf8mb4', use_unicode=True):
		if Singleton.engine is None:
			Singleton.engine = create_engine('mysql+mysqldb://%s:%s@%s:%d/%s?charset=%s&use_unicode=%d'%(user, passwd, localhost, port, charset, use_unicode), poolclass=SingletonThreadPool)	
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
		pass
