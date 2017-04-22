from django.contrib import admin
from .models import Subreddit
from .models import Comment
from .models import Redditor
from .models import Posted_By
from .forms import postedByForm
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
	list_display = ('body',)
	search_fields = ['body']

class SubredditAdmin(admin.ModelAdmin):
	list_display = ('subreddit',)
	search_fields = ['subreddit']

class postedByAdmin(admin.ModelAdmin):
	list_display = ['author', 'id',]
	#form = postedByForm


admin.site.register(Comment, CommentAdmin)
admin.site.register(Subreddit, SubredditAdmin)
admin.site.register(Posted_By, postedByAdmin)