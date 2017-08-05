from django.contrib import admin
from waverly.models import Podcast, User, Event

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'status', 'url_article', 'domain', 'title', 'url_audio1', 'url_image')
    ordering = ('-date_created',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_slug')

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_saved', 'user', 'podcast')
    ordering = ('-date_saved',)

admin.site.register(Podcast, PodcastAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
