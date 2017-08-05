from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import Http404
from waverly.models import Podcast, User, Event, PodcastForm, UserForm
from django.template.defaultfilters import slugify
from .voices import voices
from .tasks import process_podcast, process_voice
from unidecode import unidecode
import json
import os

voices = voices()

def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            print ('\n🙎  user name is valid:', slugify(unidecode(form.name)))
            try:
                user = User.objects.get(name_slug=slugify(unidecode(form.name)))
                print ('\n🙎  user exists:', user.name_slug)
            except:
                user = form
                user.save()
                print ('\n🙎  saved new user:', user.name_slug)

            return redirect('account', user.name_slug)
        else:
            print ('\n🙎  User login failed')
            return render(request, 'waverly/index.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'waverly/index.html', {'form': form})


def account(request, user_name):

    if request.method == 'POST':

        form = PodcastForm(request.POST)

        if form.is_valid():

            # get url
            print ('\n🙎  ✅  form is valid!')
            form = form.save(commit=False)
            form.status = 0
            print ('\n🙎  podcast url:', form.url_article)

            # check if podcast exists
            try:
                podcast_object = Podcast.objects.get(url_article=form.url_article)
                print ('\n🙎  podcast already exists :) podcast id:', podcast_object.id)

                # if status is -1, delete the podcast and try again
                if (podcast_object.status == -1):
                    print ('\n🙎  podcast status is -1. podcast id:', podcast_object.id)
                    print ('🙎  podcast was deleted. podcast id:', podcast_object.id)
                    podcast_object.delete()
                    podcast_object = create_new_podcast(form)
                else:
                    pass

            except:
                podcast_object = create_new_podcast(form)

            # check if event exists
            try:
                existing_event = Event.objects.get(podcast=podcast_object)
                e_id = existing_event.id
                print ('\n🙎  event already exists :\ event id:', e_id)

                existing_event.delete()
                print ('🙎  existing event was deleted :\ event id:', e_id)
            except:
                pass

            # save event
            event_object = Event()
            event_object.podcast = podcast_object
            event_object.user = User.objects.get(name_slug=user_name)
            event_object.save()
            print ('\n🙎  new event saved! event id:', event_object.id)


        else:
            print ('\n🙎  form is NOT valid!')


        user_object = User.objects.get(name_slug=user_name)
        data_obj = get_podcasts_by_account(user_object)
        # return render(request, 'waverly/account.html', data_obj)
        return HttpResponseRedirect(('/' + user_name + '/'), data_obj)

    else:

        # checking is user exists
        try:
            # getting user object
            user_object = User.objects.get(name_slug=user_name)

        except:
            print ('\n🙎  user does not exists. --> redirecting to home...')
            return redirect('/')

        data_obj = get_podcasts_by_account(user_object)
        return render(request, 'waverly/account.html', data_obj)


def podcast(request, podcast_id):

    try:
        pod_object = Podcast.objects.get(id=podcast_id)
        podcast = {
            'id': str(pod_object.id),
            'url_image': pod_object.url_image,
            'url_audio': pod_object.url_audio1,
            'title': pod_object.title,
            'authors': pod_object.authors,
            'domain': pod_object.domain,
            'text': pod_object.text1
        }
        return render(request, 'waverly/podcast.html', {'podcast': podcast})

    except:
        print ('\n🙎  had a problem redirecting to podcast id:',  podcast_id, '--> redirecting to home...')
        return redirect('/')


def voicestatus (request, podcast_id):
    if request.method == 'GET':
        try:
            pod_object = Podcast.objects.get(id=podcast_id)

            voices_status = voices
            voices_status[0]['status'] = pod_object.url_audio1
            voices_status[1]['status'] = pod_object.url_audio2
            voices_status[2]['status'] = pod_object.url_audio3
            voices_status[3]['status'] = pod_object.url_audio4
            voices_status[4]['status'] = pod_object.url_audio5
            voices_status[5]['status'] = pod_object.url_audio6
            voices_status[6]['status'] = pod_object.url_audio7
            voices_status[7]['status'] = pod_object.url_audio8
            voices_status[8]['status'] = pod_object.url_audio9
            voices_status[9]['status'] = pod_object.url_audio10

            return HttpResponse(json.dumps(voices_status), content_type="application/json")
        except:
            return HttpResponse(json.dumps(voices), content_type="application/json")

    else:
        return HttpResponse('not a GET request')

def voiceadd (request, podcast_id, voice_id):
    if request.method == 'GET':

        voice_id = int(voice_id)

        if (len(voices)-1 < int(voice_id)):
            data = {'content': 'voice number do not exist'}
            print ('\n🙎  ❗️  voice number do not exist. podcast id:', podcast_id)
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:

            voice_name = voices[voice_id]['name']

            S3_BUCKET = {
                'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
                'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID')
            }

            # sending task to worker
            process_voice.delay(podcast_id, S3_BUCKET, voice_id)

            data = {'content': 'processing new voice...'}

            print ('\n🙎  processing the voice of', voice_name, 'for podcast id:', podcast_id)
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        print ('\n🙎  ❗️  could not process the voice of', voice_name, 'for podcast id:', podcast_id)
        return HttpResponse('could not process voice')


def create_new_podcast(form):
    # save new podcast
    podcast_object = form
    podcast_object.save()
    print ('\n🙎  new podcast saved! podcast id:', podcast_object.id)

    # run podcast process function
    print ('\n🙎  starting to process the new podcast... podcast id:', podcast_object.id)

    # launch asynchronous task
    try:
        S3_BUCKET = {
            'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID')
        }
        process_podcast.delay(podcast_object.id, S3_BUCKET)
        print ('\n🙎  processing job sent to worker:', podcast_object.id)
    except:
        print ('\n🙎  ❗️  could not access aws env variables. audio will not be processed:', podcast_object.id)

    return podcast_object


# returns all the data need to be passed to the client's account page
def get_podcasts_by_account(user_object):

    # initializing lists for the return data object
    processing = []
    podcasts = []

    # getting all user's events sorted by date_saved
    user_events = Event.objects.filter(user=user_object).order_by('-date_saved')

    # arranging data for response
    for event in user_events:

        if event.podcast.status == 0:
            proc_object = {
                'status': event.podcast.status,
                'url_article': event.podcast.url_article,
                'date_saved': event.date_saved.strftime('%b %d, %Y, %I:%M%p').replace(' 0', ' ').replace('AM', 'am').replace('PM', 'pm')
            }
            processing.append(proc_object)

        else:
            pod_object = {
                'status': event.podcast.status,
                'url_article': event.podcast.url_article,
                'url_image': event.podcast.url_image,
                'title': event.podcast.title,
                'duration': event.podcast.duration,
                'domain': event.podcast.domain,
                'date_saved': event.date_saved.strftime('%b %d, %Y, %I:%M%p').replace(' 0', ' ').replace('AM', 'am').replace('PM', 'pm'),
                'id': event.podcast.id
            }
            podcasts.append(pod_object)

    # getting the original name that the user regeistered with
    original_name = user_object.name

    # initializing the form for the account page
    form = PodcastForm()

    # generating the account page data object
    data_obj = {
        'form': form,
        'user_name': user_object.name_slug,
        'original_name': original_name,
        'processing': processing,
        'podcasts': podcasts
    }
    return data_obj
