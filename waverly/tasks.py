from celery import task
from .models import Podcast, Event, User
from .parser import Mercury
from contextlib import closing
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
from langdetect import detect
import boto3
import requests
import os
import sys
from .voices import voices, save_new_voice_url
voices = voices()

@task
def process_podcast(pod_id, S3_BUCKET):

    print ('\n💻  processing podcast id:', pod_id)

    podcast = Mercury(pod_id)
    podcast.process()

    # saving article data to the db
    podcast_object = Podcast.objects.get(id=pod_id)
    podcast_object.title = podcast.title
    podcast_object.text1 = podcast.text1
    podcast_object.text2 = podcast.text2
    podcast_object.content = podcast.content
    podcast_object.status = podcast.status
    podcast_object.pages = podcast.pages
    podcast_object.domain = podcast.domain
    podcast_object.authors = podcast.authors
    podcast_object.url_image = podcast.image

    podcast_object.save()

    # storing image on s3
    if (podcast_object.url_image == None) or (podcast_object.url_image == '') or (podcast_object.url_image == '[ could not get content ]'):
        print ('\n💻  no image detected')
    else:
        s3_image_url = upload_image(podcast_object.url_image, podcast_object.id, S3_BUCKET)

        # updating db with s3 image url (url_image)
        podcast_object.url_image = s3_image_url
        podcast_object.save()
        print ('\n💻  podcast image was saved on db + s3')

    # getting audio from polly + storing audio file on s3
    s3_audio_url, status = upload_audio(pod_id, S3_BUCKET, 0)

    # updating db with: s3 audio url (url_audio)
    podcast_object.url_audio1 = s3_audio_url

    # updating db with: audio durarion (duration)
    try:
        filename, headers = urlretrieve(s3_audio_url.replace("https", "http"))
        audio_file_name = MP3(filename)
        podcast_object.duration = time_to_string(audio_file_name.info.length)
        print ('\n💻  podcast duration was retrieved')
    except Exception as e:
        print ('\n💻  ❗️  could not get file duration. ~ERR:', str(e), '~WHERE:', sys._getframe().f_code.co_name)

    # updating db with: podcast status (status)
    podcast_object.status = status

    # saving new data :)
    podcast_object.save()
    print ('\n💻  podcast processing is DONE:', podcast_object.title)
    print ('\n💻  podcast status:', podcast_object.status)
    print ('💻  podcast audio url:', podcast_object.url_audio1)


@task
def process_voice(pod_id, S3_BUCKET, voice_id):

    # adding temp url as 'processing' status
    save_new_voice_url(pod_id, voice_id, 'http://0.com')

    # getting audio from polly + storing audio file on s3
    s3_audio_url, status = upload_audio(pod_id, S3_BUCKET, voice_id)

    # saving new voice url to db
    save_new_voice_url(pod_id, voice_id, s3_audio_url)


def upload_image(url_image, pod_id, S3_BUCKET):

    # getting image from url
    img = requests.get(url_image)

    # instantiating s3 object and bucket object
    s3 = boto3.resource(
        's3',
        aws_access_key_id=S3_BUCKET['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=S3_BUCKET['AWS_SECRET_ACCESS_KEY']
        )

    bucket_name = os.environ.get('BUCKET_IMAGES')
    bucket = s3.Bucket(bucket_name)

    # posting to s3
    file_name = str(pod_id) + '.' + img.headers['content-type'].split("/")[1]
    data = img.content
    bucket.put_object(Key=file_name, Body=data, ACL='public-read')

    # get url to s3
    s3_image_url = 'https://%s.s3.amazonaws.com/%s' % (bucket_name, file_name)
    return s3_image_url


def upload_audio(pod_id, S3_BUCKET, voice_id):

    s3_audio_url = ''
    status = -1

    # getting relevant voice name
    voice_name = voices[voice_id]['name']

    # getting text from podcast object
    podcast_object = Podcast.objects.get(id=pod_id)

    # instantiating s3 object and bucket object
    polly = boto3.client(
        'polly',
        aws_access_key_id=S3_BUCKET['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=S3_BUCKET['AWS_SECRET_ACCESS_KEY'],
        region_name='us-east-2'
        )

    s3 = boto3.resource(
        's3',
        aws_access_key_id=S3_BUCKET['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=S3_BUCKET['AWS_SECRET_ACCESS_KEY']
        )

    bucket_name = os.environ.get('BUCKET_AUDIO')
    bucket = s3.Bucket(bucket_name)

    # checking if article is in English
    try:
        detect(podcast_object.text1)

        if detect(podcast_object.text1) == 'en':

            # splitting text to chunks < 3000 characters
            # using: html2text
            text_chunks = split_lines(podcast_object.text1)

            # getting audio streams from polly for each chunk (text1)
            # concatenating audio streams to a single file
            audio_file_data = ''

            # getting audio for article title
            try:
                title = '<speak>' + podcast_object.title + '.<break time="1.1s"/></speak>'

                response1 = polly.synthesize_speech(
                    Text=title,
                    OutputFormat="mp3",
                    VoiceId=voice_name,
                    TextType="ssml")
                print ('💻  received audio for mercury (title) from polly.')

                with closing(response1["AudioStream"]) as data:
                    audio_object = data
                    # audio_object = response1["AudioStream"]
                    audio_binary = audio_object.read()
                    if (audio_file_data == ''):
                        audio_file_data = audio_binary
                    else:
                        audio_file_data = audio_file_data + audio_binary

            except Exception as e:
                print ('💻  ❗️  could not get audio for the title. ERR:', str(e))


            for i in range(len(text_chunks)):

                try:
                    response1 = polly.synthesize_speech(
                        Text=text_chunks[i],
                        OutputFormat="mp3",
                        VoiceId=voice_name,
                        TextType="ssml")
                    print ('💻  received audio for mercury from polly.')

                    with closing(response1["AudioStream"]) as data:
                        audio_object = data
                        # audio_object = response1["AudioStream"]
                        audio_binary = audio_object.read()
                        if (audio_file_data == ''):
                            audio_file_data = audio_binary
                        else:
                            audio_file_data = audio_file_data + audio_binary

                except Exception as e:
                    print ('💻  ❗️  could not get audio for one of the text chunks. ERR:', str(e))

            # posting to concatenated file to s3
            file_name = str(pod_id) + '_' + str(voice_id) + '.mp3'
            if not (audio_file_data == ''):
                try:
                    print ('💻  uploading complete audio file to s3...')
                    bucket.put_object(Key=file_name, Body=audio_file_data, ACL='public-read')
                    print ('💻  stored mercury stream on s3.')

                    # get url to s3
                    s3_audio_url = 'https://%s.s3.amazonaws.com/%s' % (bucket_name, file_name)
                    status = 1
                    print (s3_audio_url)
                    return s3_audio_url, status

                except Exception as e:
                    print ('💻  ❗️  could not upload the complete audio file on s3. ERR:', str(e))
                    return s3_audio_url, status
            else:
                print ('💻  ❗️  no audio data to store on s3.')
                return s3_audio_url, status

        # article is not in English
        else:
            print ('💻  ❗️  article is not in English.')
            return s3_audio_url, status

    except:
        print ('💻  ❗️  article is not in English.')
        return s3_audio_url, status


def split_lines(text):

    text_list = text.split('\n')

    chunks = ['<speak><p>']
    index = 0
    line_cut_right = ''

    for line in text_list:

        if line == '':
            line = '</p><p>'

        line += ' '

        if ( len(chunks[index] + line) > 1500-len('</p></speak>')-100 ):

            current_chunk = chunks[index]
            for c in range(len(current_chunk)):
                string = current_chunk[len(current_chunk)-(c+1):]
                if string[0] == '.':
                    right = current_chunk[len(current_chunk)-c:]
                    left = current_chunk[:len(current_chunk)-c]
                    line_cut_right = right
                    chunks[index] = left
                    break

            chunks[index] += '</p></speak>'
            index += 1
            new_chunk = '<speak><p>' + line_cut_right
            chunks.append(new_chunk)

        chunks[index] += line

    chunks[index] += '</p></speak>'
    return chunks

def time_to_string(length):
    minutes = int(length)//60
    seconds = int(length)%60
    string = '%(min)s:%(sec)s' %{'min':minutes, 'sec':str(seconds).zfill(2)}
    return string
