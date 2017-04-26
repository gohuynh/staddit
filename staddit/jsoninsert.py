import psycopg2
import ast
import time
from psycopg2.extras import execute_batch
import datetime
#connect to sql server
try:
	conn = psycopg2.connect("dbname = 'reddit' user = 'postgres' host = 'localhost' password = 'gordon'")
except:
	print("L2type baddie (Can't connect to the database)")

#list of attributes we want
ourKeys = ["body", "score", "id", "controversiality", "author_flair_css_class", "author_flair_text", "parent_id", "author", "link_id", "gilded", "created_utc", "subreddit"]

cur = conn.cursor()

#sql insertion statements (format strings to prevent injections)
sqlRedditor = '''INSERT INTO redditor(author) VALUES (%(author)s) ON CONFLICT(author) DO NOTHING'''
sqlComment = '''INSERT INTO comment(id, body, created_utc, gilded, score, controversiality) VALUES (%(id)s, %(body)s, %(created_utc)s, %(gilded)s, %(score)s, %(controversiality)s) ON CONFLICT(id) DO NOTHING'''
sqlPostedIn = ''' INSERT INTO posted_in(id, subreddit) VALUES(%(id)s, %(subreddit)s)'''
sqlSubreddit = '''INSERT INTO subreddit(subreddit) VALUES( %(subreddit)s) ON CONFLICT(subreddit) DO NOTHING'''
sqlPostedby = '''INSERT INTO posted_by(author, id) VALUES(%(author)s, %(id)s)''' 
startTime = time.time()
dicList = []
### CHANGE THE RANGE DEPENDING ON HOW MANY FILES YOU WANT TO LOAD. SUGGEST range(0,2)
for x in range(0,5):
	#### CHANGE THIS TO THE PROPER DIRECTORY 
	with open('C:/Users/Gordon/Desktop/json/jan17('+str(x).zfill(12)+')', 'r', encoding = "utf-8") as f:
		for line in f:
			deletionList = []
			if line[-1:] == '\n':
				line = line[:-1]

			#prevent errors from line breaks; transform each line from a string to dictionary
			line = line.replace("\n", "\\n")
			line = ast.literal_eval(line)

			#remove attributes that are not in our desired list
			for key in line.keys():
				if key not in ourKeys:
					deletionList.append(key)
			for key in deletionList:
				del line[key]
			
			#add missing attributes from our desired list; instantiate with null value
			for key in ourKeys:
				if key not in line.keys():
					line[key]='null'
			line["created_utc"] = str(datetime.datetime.fromtimestamp(int(line["created_utc"])).strftime('%Y-%m-%d %H:%M:%S'))
			dicList.append(line)
		
print("Done creating dictionaries. Elapsed: "+format(time.time()-startTime))
#psycop requires tuples
dicList = tuple(dicList)

#executemany: 577s (136+100+134+95+112)
#execute sql statements using list of dictionaries
try:
	startTime = time.time()
	execute_batch(cur, sqlComment, dicList)
	#cur.executemany(sqlComment,dicList)
	print("comment db updated. Elapsed: "+format(time.time()-startTime))
except Exception as e:
	print("failed to add to db 'comment'", e)
#"""
try:
	startTime = time.time()
	execute_batch(cur, sqlRedditor, dicList)
	#cur.executemany(sqlRedditor,dicList)
	print("redditor db updated. Elapsed: "+format(time.time()-startTime))
except:
	print("failed to add to db 'redditor'")
#"""
try:
	startTime = time.time()
	execute_batch(cur, sqlSubreddit, dicList)
	#cur.executemany(sqlSubreddit,dicList)
	print("subreddit db updated. Elapsed: "+format(time.time()-startTime))
except:
	print("failed to add to db 'subreddit'")
try:
	startTime = time.time()
	execute_batch(cur, sqlPostedIn, dicList)
	#cur.executemany(sqlPostedIn,dicList)
	print("posted_in db updated. Elapsed: "+format(time.time()-startTime))
except Exception as e:
	print("failed to add to db 'posted_in'", e)

try: 
	startTime = time.time()
	execute_batch(cur, sqlPostedby, dicList)
	#cur.executemany(sqlPostedby, dicList)
	print("posted_by db updated. Elapsed: "+format(time.time()-startTime))
except:
	print("failed to add to db 'posted_by'")
	

conn.commit()
cur.close()

if conn is not None:
	conn.close()
