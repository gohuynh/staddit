 # stad/views.py
from django.db import connection
from django.db.models import Q
from django.shortcuts import render
from stad import forms
from stad import helper
from stad import models
import django_tables2 as tables


# Create your views here.
curTab = '' #Oh great! A global variable!
cur = connection.cursor()

class post_by_Table(tables.Table):
	author = tables.Column(order_by='author')
	id = tables.Column()

	class Meta:
		model = models.Posted_By;
		attrs = {'class': 'table table-bordered table-striped table-hover', 'border': 1}
		template = 'django_tables2/bootstrap.html'


class post_in_Table(tables.Table):
	subreddit = tables.Column(order_by='subreddit')
	id = tables.Column()

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

	form = forms.subredditForm(request.POST or None)
	inSubreddit = ''
	if request.method == "POST":
		print(request.POST)

		if form.is_valid():
			print('hi')
			inSubreddit = form.cleaned_data['subreddit']

			#THIS IS A QUERY BELOW
			qs = models.Posted_In.objects.filter(subreddit = inSubreddit)
			table = post_in_Table(qs, order_by = '-id')
			curTab = table
			if table:
				table.paginate(page = request.GET.get('page', 1), per_page = 12)

			context = {
				"table": table,
				"form": form,
				"title": title,
			}

			return render(request, 'subred.html',context)

	elif request.GET:
		print('not empty')
		if curTab: print('woohoo!')
		curTab.paginate(page = request.GET.get('page', 1), per_page = 12)
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

	#qs = models.Posted_By.objects.filter(Q(author = 'DrunkGirl69') | Q(author = 'Thaddel') )

	context = {
		"title": title,
		"form": form,
	}
	
	
	#table = postbyTable(ans1)
	return render(request, 'index.html',context)#, 'form': form})

def user(request):
	title = 'User search'
	global curTab

	form = forms.redditorForm(request.POST or None)
	inSubreddit = ''

	if request.method == 'POST':
		print(request.POST)
		#form = forms.redditorForm(request.POST or None)

		if form.is_valid():
			inRedditor = form.cleaned_data['author']
			
			subQuer = helper.mostPosted(inRedditor)
			topCom = helper.topScoring(inRedditor)
			scores = helper.sentimentAnalysis(inRedditor)

			avgScore = scores[0]
			minScore = scores[1]
			maxScore = scores[2]

			qs = models.Posted_By.objects.select_related().filter(author = inRedditor)
			table = post_by_Table(qs, order_by = '-id')
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
			return render(request, 'user.html', context)

	elif request.GET:
		curTab.paginate(page = request.GET.get('page', 1), per_page = 12)
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


