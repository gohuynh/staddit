# stad/urls.py
from django.conf.urls import url
from stad import views
from stad.views import index
from stad.views import subred
from stad.views import user
#from stad.views import subredresult

urlpatterns = [
	url(r'^$', index, name = 'home'),
    #url(r'^$', views.HomePageView.as_view()),
    url(r'^about/$', views.AboutPageView.as_view()), #add about page
    #url(r'^subred/$', views.subred.as_view()),
 	url(r'^user/$', user, name = 'user'),
 	url(r'^subred/$', subred, name = 'subred'),
 	#url(r'^subredresult/$', subredresult, name = 'subredresult'),
 #	url(r'^(?P<author>\s+))/$', usearch, name = 'search')
]