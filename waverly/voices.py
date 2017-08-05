from waverly.models import Podcast

# amazon polly voices mapping
def voices():
    voices = [
        {
            'name': 'Joey',
            'country': 'us',
            'column': 'url_audio1',
            'title': '👱 Joey'
        },

        {
            'name': 'Joanna',
            'country': 'us',
            'column': 'url_audio2',
            'title': '👩 Joanna'
        },

        {
            'name': 'Salli',
            'country': 'us',
            'column': 'url_audio3',
            'title': '👧 Salli'
        },

        {
            'name': 'Kimberly',
            'country': 'us',
            'column': 'url_audio4',
            'title': '👵 Kimberly'
        },

        {
            'name': 'Kendra',
            'country': 'us',
            'column': 'url_audio5',
            'title': '👩 Kendra'
        },

        {
            'name': 'Ivy',
            'country': 'us',
            'column': 'url_audio6',
            'title': '👧 Ivy'
        },

        {
            'name': 'Justin',
            'country': 'us',
            'column': 'url_audio7',
            'title': '👦 Justin'
        },

        {
            'name': 'Emma',
            'country': 'uk',
            'column': 'url_audio8',
            'title': '👧 Emma'
        },

        {
            'name': 'Amy',
            'country': 'uk',
            'column': 'url_audio9',
            'title': '👩 Amy'
        },

        {
            'name': 'Brian',
            'country': 'uk',
            'column': 'url_audio10',
            'title': '👴 Brian'
        },

    ]

    return voices


def save_new_voice_url(pod_id, voice_id, url):

    pod_object = Podcast.objects.get(id=pod_id)

    if voice_id == 0:
        pod_object.url_audio1 = url

    elif voice_id == 1:
        pod_object.url_audio2 = url

    elif voice_id == 2:
        pod_object.url_audio3 = url

    elif voice_id == 3:
        pod_object.url_audio4 = url

    elif voice_id == 4:
        pod_object.url_audio5 = url

    elif voice_id == 5:
        pod_object.url_audio6 = url

    elif voice_id == 6:
        pod_object.url_audio7 = url

    elif voice_id == 7:
        pod_object.url_audio8 = url

    elif voice_id == 8:
        pod_object.url_audio9 = url

    elif voice_id == 9:
        pod_object.url_audio10 = url

    else:
        pass

    pod_object.save()
