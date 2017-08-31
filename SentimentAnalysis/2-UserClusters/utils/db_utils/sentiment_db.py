from base_db import Database

class CommentDbConnection(Database):
	def __init__(self, host='localhost', port='3306', user='root', passwd='', db='sentiment_db'):
		Database.__init__(
			self,
			host = host,
			port = port,
			user = user,
			passwd = passwd)
		self.table = 'im_commento'
		self.select = 'id, content, id_post, from_id'

	def fetch_all(self, where=''):
		return super(CommentDbConnection, self).fetch_all(select=self.select, from_clause=self.table, where=where)

	def fetch_by_id(self, id=''):
		return super(CommentDbConnection, self).fetch_all(select=self.select, from_clause=self.table, where="id='%d'" % id)
