 # stad/views.py
from django.db import connection
from django.db.models import Q
from django.shortcuts import render
from stad import forms
from stad import helper
from stad import models
import django_tables2 as tables


#global variables to handle next page GET requests
curTab = '' 
subContext = ''
userContext = ''


cur = connection.cursor()

class post_by_Table(tables.Table): 
	"""django-tables table with authors and comments"""
	author = tables.Column()
	id = tables.Column(accessor = 'id.id')
	body = tables.Column(accessor = 'id.body')
	created_utc = tables.Column(accessor = 'id.created_utc')
	gilded = tables.Column(accessor = 'id.gilded')
	score = tables.Column(accessor = 'id.score', order_by='score')
	created_utc = tables.Column(accessor = 'id.created_utc')

	class Meta:
		model = models.Posted_By
		attrs = {'class': 'table table-bordered table-striped table-hover', 'border': 1}
		template = 'django_tables2/bootstrap.html'


class post_in_Table(tables.Table):
	subreddit = tables.Column()
	id = tables.Column(accessor = 'id.id')
	body = tables.Column(accessor = 'id.body')
	created_utc = tables.Column(accessor = 'id.created_utc')
	gilded = tables.Column(accessor = 'id.gilded')
	score = tables.Column(accessor = 'id.score', order_by='score')
	redditor = tables.Column(accessor = 'id.Posted_By.author')

	class Meta:
		model = models.Posted_In;
		attrs = {'class': 'table table-bordered table-striped table-hover', 'border': 1}
		template = 'django_tables2/bootstrap.html'


def index (request):
	title = "Main page"
	form = forms.subredditForm()

	context = {
		"title": title,
		"form": form,
	}
	

	return render(request, 'index.html',context)

def subred(request):
	title = "Sub search"
	global curTab
	global subContext

	form = forms.subredditForm(request.POST or None)
	inSubreddit = ''
	if request.method == "POST":
		print(request.POST)

		if form.is_valid():
			print('hi')
			inSubreddit = form.cleaned_data['subreddit']

			mostPostSub = helper.mostPostedSub(inSubreddit)
			topComm = helper.topScoringSub(inSubreddit)
			scores = helper.sentimentAnalysisSub(inSubreddit)

			avgScore = scores[0]
			stdScore = scores[1]
			medScore = scores[2]

			#THIS IS A QUERY BELOW
			qs = models.Posted_In.objects.filter(subreddit = inSubreddit)
			table = post_in_Table(qs, order_by = '-id')
			curTab = table
			if table:
				table.paginate(page = request.GET.get('page', 1), per_page = 17)

			context = {
				"subreddit": inSubreddit,
				"table": table,
				"form": form,
				"title": title,
				"mostPosted": mostPostSub,
				"topComm": topComm,
				"avgScore": avgScore,
				"stdScore": stdScore,
				"medScore": medScore,

			}
			subContext = context
			return render(request, 'subred.html',context)

	elif request.GET:
		print('not empty')
		if curTab: print('woohoo!')
		curTab.paginate(page = request.GET.get('page', 1), per_page = 12)
		if subContext:
			context = subContext
		else:
			context = {
				'table': curTab,
				'form': form,
				'title': title,
			}
		return render(request, 'subred.html', context)


	else:
		if not curTab: print("yayayaya")
		print('empty')
		print(request.GET)
		form = forms.subredditForm()


	context = {
		"title": title,
		"form": form,
	}
	
	
	return render(request, 'index.html',context)

def user(request):
	title = 'User search'
	global curTab
	global userContext

	form = forms.redditorForm(request.POST or None)
	inSubreddit = ''

	if request.method == 'POST':
		print(request.POST)

		if form.is_valid():
			inRedditor = form.cleaned_data['author']
			
			subQuer = helper.mostPosted(inRedditor)
			topCom = helper.topScoring(inRedditor)
			scores = helper.sentimentAnalysis(inRedditor)

			avgScore = scores[0]
			minScore = scores[1]
			maxScore = scores[2]

			qs = models.Posted_By.objects.filter(author = inRedditor).select_related("id").order_by('comment.score')
			table = post_by_Table(qs)#, order_by = '-id')
			curTab = table
			if table:
				table.paginate(page = request.GET.get('page', 1), per_page = 12)

			context = {
				'user': inRedditor,
				'table': table,
				'form': form,
				'title': title,
				'subQuer': subQuer,
				'topCom' :topCom,
				'avgScore' :avgScore,
				'minScore' :minScore,
				'maxScore': maxScore,
			}
			userContext = context
			return render(request, 'user.html', context)

	elif request.GET:
		print(request.GET.get)
		curTab.paginate(page = request.GET.get('page', 1), per_page = 12)
		if userContext:
			context = userContext
		else:
			context = {
				'table': curTab,
				'form': form,
				'title': title,
			}
		return render(request, 'user.html', context)

	else:
		form = forms.redditorForm()

	context = {
		'title':title,
		'form': form,	
	}

	return render(request, 'index.html', context)



#class AboutPageView(TemplateView):
   # template_name = "about.html"


