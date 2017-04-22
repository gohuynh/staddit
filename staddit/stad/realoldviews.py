 # stad/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import HttpResponse
from stad import forms
from stad import models
from django.db.models import Q
import django_tables2 as tables

#from stad.forms import postedByForm
"""
import psycopg2
import psycopg2.extras

conn = psycopg2.connect('dbname = reddit host = localhost user = postgres password = butt')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute('select * from posted_in limit 10')
ans = cur.fetchall()
ans1 = []
for row in ans:
	ans1.append(dict(row))
"""
# Create your views here.

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
	title = "Sub search"
	form = forms.subredditForm()
	#data = models.Posted_In.objects.filter(subreddit = 'headphones')[:10]
	#data = models.Posted_By.objects.filter(author = 'DrunkGirl69')
	"""
	inSubreddit = ''
	if request.method == "POST":
		print(request.POST)
		form = forms.subredditForm(request.POST or None)

		if form.is_valid():
			#instance = form.save(commit =False)
			print('hi')
			#print(instance.subreddit)
			inSubreddit = form.cleaned_data['subreddit']

			qs = models.Posted_In.objects.filter(subreddit = inSubreddit)
			table = post_in_Table(qs)

			context = {
				"table": table,
				"form": form,
				"title": title,
			}

			return render(request, 'subred.html',context)

	else:
		form = forms.subredditForm()
"""
	#qs = models.Posted_By.objects.filter(Q(author = 'DrunkGirl69') | Q(author = 'Thaddel') )
	
	#form = forms.subredditForm(data = request.POST or None)
	context = {
		"title": title,
		"form": form,
	}
	
	
	#table = postbyTable(ans1)
	return render(request, 'index.html',context)#, 'form': form})

def subred(request):
	title = "Sub search"
	#data = models.Posted_In.objects.filter(subreddit = 'headphones')[:10]
	#data = models.Posted_By.objects.filter(author = 'DrunkGirl69')
	inSubreddit = ''
	if request.method == "POST":
		print(request.POST)
		form = forms.subredditForm(request.POST or None)

		if form.is_valid():
			#instance = form.save(commit =False)
			print('hi')
			#print(instance.subreddit)
			inSubreddit = form.cleaned_data['subreddit']

			qs = models.Posted_In.objects.filter(subreddit = inSubreddit)
			table = post_in_Table(qs)

			context = {
				"table": table,
				"form": form,
				"title": title,
			}

			return render(request, 'subred.html',context)

	else:
		form = forms.subredditForm()

	#qs = models.Posted_By.objects.filter(Q(author = 'DrunkGirl69') | Q(author = 'Thaddel') )
	
	#form = forms.subredditForm(data = request.POST or None)
	context = {
		"title": title,
		"form": form,
	}
	
	
	#table = postbyTable(ans1)
	return render(request, 'index.html',context)#, 'form': form})
	"""
	def do_subred(request):
		form = forms.subredditForm(request.POST or None)
		if request.method == "POST":
			instance = form.save(commit = False)
			x = instance.subreddit
			print(x)
			return x

	if request.method == "POST":
		qs = models.Posted_In.objects.filter(subreddit = do_subred(request))
		table = post_in_Table(qs)

		context = {
		"form": form,
		"table": table,
		}

		return render(request, 'subred.html', context)
	else:
		form = forms.subredditForm(request.POST or None)
		context = {
			'form': form,
		}
	return render(request, 'subredresult.html', context)
	"""
"""
	form = forms.subredditForm(request.POST or None)
	x = None; table = None

	if request.method == "POST":
		x = request.POST
		print(x)

		#if form.is_valid():
		instance = form.save(commit = False)
		x = instance.subreddit
"""
		
"""class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
"""

class AboutPageView(TemplateView):
    template_name = "about.html"

#class subred(TemplateView):
	#template_name = 'subred.html'

class user(TemplateView):
	template_name = 'user.html'

