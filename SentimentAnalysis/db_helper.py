import pymysql

hostname = 'localhost'
username = 'root'
password = 'Koliko90'
database = 'social_networks'

def doQuery(conn, queryText, cursorType= pymysql.cursors.Cursor):
	cur = conn.cursor(cursorType)
	cur.execute(queryText)
	print("Executin query: ", queryText)
	return cur
	

def db_connect() :
	myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database, charset='utf8mb4')
	print("Connected to DB..")
	return myConnection

def db_close(conn):
	conn.close()
	print("Closed DB connection..")

def getCommentById(id):
	conn = db_connect()
	query = 'select content from im_commento where id = %d' %id
	cur = doQuery(conn, query)

	result = cur.fetchone()

	db_close(conn)

	return result[0]

def getAllCommentsForPost(idpost):
	conn = db_connect()
	query = 'select content from im_commento where idpost = %d' %idpost
	cur = doQuery(conn, query)

	results = cur.fetchall()
	
	flattenedResult = [r[0] for r in results]

	db_close(conn)

	return flattenedResult

def insertSentForPost(idpost, sent):
	#TODO: check if the postid already exists
	
	conn = db_connect()

	query = """ CREATE TABLE IF NOT EXISTS `im_postsentiment` (
  				`id` int(11) NOT NULL AUTO_INCREMENT,
  				`idpost` int(11) DEFAULT NULL COMMENT 'post id', 
  				`text_sentiment` FLOAT(11,5),
  				`emoji_sentiment` FLOAT(11,5),
  				`combined_sentiment` FLOAT(11,5),
  				PRIMARY KEY (`id`)
				) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;"""

	cur = doQuery(conn, query)


	query = """ insert into im_postsentiment (idpost, text_sentiment, emoji_sentiment, combined_sentiment)
				values ({0}, {1}, {2}, {3});""".format(idpost, sent['text'], sent['emojis'], sent['combined'])
	
	cur = doQuery(conn, query)
	conn.commit()
	db_close(conn)






