# stad/helper.py

from django.db import connection
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

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
	subtract = 0


	analyzer = SentimentIntensityAnalyzer()
	for c in comms:
		sentences.extend(sent_tokenize(c[0]))
	for sen in sentences:
		thisScore = analyzer.polarity_scores(sen)['compound']
		scores.append(thisScore)
		avgScore += thisScore
		if thisScore == 0:
			subtract +=1

	if 0 != len(sentences):
		avgScore = avgScore/(len(sentences)-subtract)
	else:
		avgScore = 0
	minScore = sentences[scores.index(min(scores))], min(scores)
	maxScore = sentences[scores.index(max(scores))], max(scores)

	return avgScore, minScore, maxScore

def mostPostedSub(subreddit):
	"""return most post-igious users in a sub"""
	cur.execute("""select author, count(author) from posted_in, posted_by where subreddit = '"""+subreddit+"""' and posted_by.id = posted_in.id and author != '[deleted]' group by author order by count(author) desc limit 3""")
	return cur.fetchall()
	
def topScoringSub(subreddit):
	"""return top scoring comment in a sub"""
	cur.execute("""select body, author, score from posted_in, posted_by, comment where subreddit = '"""+subreddit+"""' and posted_by.id = posted_in.id and comment.id = posted_by.id and author not like '%AutoModerator%' order by score desc limit 1""")
	return cur.fetchone()

def sentimentAnalysisSub(subreddit):
	"""return sentiment analysis summary stats for sub"""

	cur.execute("""select body from posted_in, comment where posted_in.id = comment.id and posted_in.subreddit = '"""+subreddit+"""' limit 100""")

	comms = cur.fetchall()
	sentences = []
	avgScore = 0
	scores = []
	subtract = 0

	analyzer = SentimentIntensityAnalyzer()
	for c in comms:
		sentences.extend(sent_tokenize(c[0]))
	for sen in sentences:
		thisScore = analyzer.polarity_scores(sen)['compound']
		scores.append(thisScore)
		avgScore += thisScore
		if thisScore == 0:
			subtract +=1

	newScores = [x for x in scores if x!=0]
	
	if 0 != len(sentences):
		avgScore = avgScore/(len(sentences) - subtract)
	else:
		avgScore = 0
		
	medScore = np.median(np.array(newScores))
	stdScore = np.std(np.array(newScores))

	return avgScore, stdScore, medScore