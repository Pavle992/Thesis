from .base_api import BaseAPI
import facebook # pip freeze | grep face # command to support python 3.6.1

class FacebookAPI(BaseAPI):
	def __init__(self, token=''):
		self.token = token
		self.graph=None

	def connect(self):
		self.graph = facebook.GraphAPI(self.token)

	def request(self, ids=[], fields='birthday,about,business,emails,description,genre,location,season,category'):
		ids_string = ','.join(x for x in ids)
		try:
			self.response = self.graph.request('/?ids=%s&fields=%s' % (ids_string, fields))
			if len(self.response.items()) == 1:
				return self.__format_json(self.response[ids[0]])
				# return self.response
			elif len(self.response.items()) > 1:
				return self.response
		except Exception as e:
			#print("Id dont exist or need permission")
			pass

	def __format_json(self, jsn):
	    acc_val = {'city', 'country', 'zip'}
	    new_jsn = {}
	    for key, value in jsn.items():
	        if key == 'emails':
	            new_jsn[key] = value[0]
	        elif key == 'id':
	            continue
	        elif key != 'location':
	            new_jsn[key] = value
	        else:
	            for k, v in jsn[key].items():
	                if k in acc_val:
	                    new_jsn[k] = v
	    return new_jsn