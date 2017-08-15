import pymysql

hostname = 'localhost'
username = 'root'
password = ''
database = 'im_dump'

def doQuery(conn, queryText):
	cur = conn.cursor()
	cur.execute(queryText)
	print("Executin query: ", queryText)
	return cur
	# for cnt in cur.fetchall() :
	#     print(cnt)

def db_connect() :
	myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, charset='utf8')
	print("Connected to DB..")
	return myConnection

def db_close(conn):
	conn.close()
	print("Closed DB connection..")




