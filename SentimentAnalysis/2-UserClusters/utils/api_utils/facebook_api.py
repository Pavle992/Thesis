from .base_api import BaseAPI
import facebook

class FacebookAPI(BaseAPI):
	def __init__(self, token=''):
		self.token = token
		self.graph=None

	def connect(self):
		self.graph = facebook.GraphAPI(self.token)

	def request(self, ids=[], fields='birthday,about,business,emails,description,genre,location,season,category,founded'):
		ids_string = ','.join(x for x in ids)
		self.response = self.graph.request('/?ids=%s&fields=%s' % (ids_string, fields))
		return self.response