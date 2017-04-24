from django.db import connection



def mostPosted(redditor):
	cur = connection.cursor()
	cur.execute("""select subreddit from posted_in, posted_by where posted_by.author = '"""+inRedditor+"""' and posted_by.id = posted_in.id group by subreddit order by count(subreddit) desc limit 3""")

	query = cur.fetchall()
	for sub in range(len(query)):
		query[sub] = query[sub][0]
	return query