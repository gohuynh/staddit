# stad/helper.py

from django.db import connection
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

cur = connection.cursor()

def mostPosted(redditor):
	"""return top 3 most poted in subreddits for a redditor"""

	cur.execute("""select subreddit from posted_in, posted_by where posted_by.author = '"""+redditor+"""' and posted_by.id = posted_in.id group by subreddit order by count(subreddit) desc limit 3""")

	query = cur.fetchall()
	for sub in range(len(query)):
		query[sub] = query[sub][0]
	return query

def topScoring(redditor):
	"""return a redditor's top scoring comment"""

	cur.execute("""select body, score, subreddit from comment, posted_in, posted_by where posted_by.author = '"""+redditor+"""' and posted_by.id = posted_in.id and comment.id = posted_by.id order by score desc limit 1""")
	return cur.fetchone()

def sentimentAnalysis(redditor):
	"""return sentiment analysis summary stats"""

	cur.execute("""select body from posted_by, comment where posted_by.id = comment.id and posted_by.author = '"""+redditor+"""' limit 100""")

	comms = cur.fetchall()
	sentences = []
	avgScore = 0
	scores = []

	analyzer = SentimentIntensityAnalyzer()
	for c in comms:
		sentences.extend(sent_tokenize(c[0]))
	for sen in sentences:
		thisScore = analyzer.polarity_scores(sen)['compound']
		scores.append(thisScore)
		avgScore += thisScore

	avgScore = avgScore/len(sentences)
	minScore = sentences[scores.index(min(scores))], min(scores)
	maxScore = sentences[scores.index(max(scores))], max(scores)

	return avgScore, minScore, maxScore

