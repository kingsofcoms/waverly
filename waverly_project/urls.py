from django.conf.urls import url
from django.contrib import admin
from waverly import views

urlpatterns = [
    url(r'^admin/', admin.site.urls), # admin
    url(r'^$', views.index, name="index"), #login
    url(r'^(?P<user_name>[\w\-]+)/$', views.account, name="account"), #account page
    url(r'^podcast/(?P<podcast_id>[\w\-]+)/$', views.podcast, name="podcast_page"), #podcast page
    url(r'^podcast/(?P<podcast_id>[\w\-]+)/voicestatus/$', views.voicestatus, name="voicestatus_endpoint"), #check voices availablity per podcast
    url(r'^podcast/(?P<podcast_id>[\w\-]+)/voiceadd/(?P<voice_id>[\w\-]+)/$', views.voiceadd, name="voiceadd_endpoint"), #process new voice end point
]
