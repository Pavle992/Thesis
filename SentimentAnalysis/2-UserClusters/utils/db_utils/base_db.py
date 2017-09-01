from sqlalchemy import create_engine, exc
from sqlalchemy.pool import SingletonThreadPool
import pandas as pd
import numpy as np

class Singleton(object):
	engine = None
	connection = None

	@staticmethod
	def get_connection(host='localhost', port=3306, user='root', passwd='', db='sentiment_db', charset='utf8mb4', use_unicode=True):
		if Singleton.engine is None:
			Singleton.engine = create_engine('mysql+mysqldb://%s:%s@%s:%d/%s?charset=%s&use_unicode=%d' % (user, passwd, host, port, db, charset, use_unicode), poolclass=SingletonThreadPool)
		Singleton.connection = Singleton.engine.connect()

		return Singleton.connection

class Database(object):
	def __init__(self, host='localhost', port=3306, user='root', passwd='', db='sentiment_db'):
		self.db = db
		self.host = host
		self.port = port
		self.user = user
		self.passwd = passwd
		self.connection = None

	def connect(self):
		if self.connection is not None:
			print('Db connection already exist')
		try:
			self.connection = Singleton.get_connection(
				host = self.host,
				port = self.port,
				user = self.user,
				passwd = self.passwd,
				db = self.db,
				charset = 'utf8mb4',
				use_unicode = True
				)
			print("Database connection created: %s" % str(self.connection))
		except exc.SQLAlchemyError as e:
			print("Error in connecting to db: %s" % e)

	def fetch_all(self, select='*', from_clause='', where='', order_by='', data_as_dataframe=True):
		
		stmt = 'SELECT %s FROM %s' % (select, from_clause)

		if where != '':
			stmt +=' WHERE %s' % where

		if order_by != '':
			stmt +=' ORDER BY %s' % order_by

		try:
			results = self.connection.execute(stmt).fetchall()
			if data_as_dataframe:
				return self.to_dataframe(results, column_names=select)
			return results						
		except exc.SQLAlchemyError as e:
			print('Error executing query: %s' % e)
			raise Exception(e)

	def insert(self, table='', column_value={}):

		columns=""
		values = ""

		for column, value in column_value.items():
			columns += "`%s`," % column
			values += "%s," % value

		columns = columns[:-1] # removing last comma(,)
		values = values[:-1] # removing last comma(,)

		stmt = "INSERT INTO `%s`.`%s` (%s) VALUES (%s)" % (self.db, table, columns, values)
		try:
			self.connection.execute(stmt)
			print("Inserting into table %s" % table)
			print("Setting (%s) to values (%s)" % (columns, values))
		except exc.SQLAlchemyError as e:
			print('Error inserting database: %s' % e)

	def update(self, table, set_values={}, where=''):
		set_value_string = ""
		for column, value in set_values.items():
			set_value_string += "`%s` = '%s',"

		set_value_string = set_value_string[:-1]

		stmt = "UPDATE `%s` SET %s WHERE %s" % (table, set_value_string, where)

		try:
			self.connection.execute(stmt)
			print("Updating table %s" % table)
			print("Setting %s" % set_value_string)
		except exc.SQLAlchemyError as e:
			print('Error updating database: %s' % e)
			raise Exception(e)
	def close(self):
		self.connection.close()
		print('Closing database connection %s' % str(self.connection))

	def table_names(self):
		if Singleton.engine is not None:
			return Singleton.engine.table_names()
		else:
			print('Database connection is not created')

	def to_dataframe(self, data, column_names=''):
		if column_names != '' and column_names != '*':
			return pd.DataFrame(data, columns=column_names.split(','))
		return pd.DataFrame(data)