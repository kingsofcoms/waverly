from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.forms import ModelForm
from django import forms
import unidecode
from unidecode import unidecode

class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)

class Podcast(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=True, max_length=600, null=True)
    text1 = models.TextField(blank=True, null=True)
    text2 = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url_article = models.URLField()
    url_audio1 = models.URLField(blank=True, null=True)
    url_audio2 = models.URLField(blank=True, null=True)
    url_audio3 = models.URLField(blank=True, null=True)
    url_audio4 = models.URLField(blank=True, null=True)
    url_audio5 = models.URLField(blank=True, null=True)
    url_audio6 = models.URLField(blank=True, null=True)
    url_audio7 = models.URLField(blank=True, null=True)
    url_audio8 = models.URLField(blank=True, null=True)
    url_audio9 = models.URLField(blank=True, null=True)
    url_audio10 = models.URLField(blank=True, null=True)
    url_image = models.URLField(blank=True, null=True)
    url_podcast = models.SlugField(blank=True, max_length=600)
    duration = models.CharField(blank=True, null=True, max_length=20)
    status = models.IntegerField(default=-1)
    pages = models.IntegerField(blank=True, null=True)
    domain = models.CharField(blank=True, max_length=600, null=True)
    authors = models.CharField(blank=True, max_length=600, null=True)

    def save(self, *args, **kwargs):
        try:
            self.url_podcast = slugify(self.title)
            super(Podcast, self).save(*args, **kwargs)
        except:
            pass

    def __str__(self):
        return self.url_article

class User(models.Model):
    name = models.CharField(max_length=120)
    name_slug = models.SlugField(blank=True)
    # email = models.EmailField(blank=True, null=True)
    # password = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(unidecode(self.name))
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name_slug

class Event(models.Model):
    podcast = models.ForeignKey(Podcast)
    user = models.ForeignKey(User)
    date_saved = models.DateTimeField(auto_now_add=True)


class PodcastForm(ModelForm):
    class Meta:
        model = Podcast
        fields = ['url_article']
        labels = {
            'url_article': (''),
        }
        widgets = {
            'url_article': forms.TextInput(attrs={'placeholder': 'enter an article URL...'}),
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name']
        labels = {
            'name': (''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'enter your username...'}),
        }
