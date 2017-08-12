# Project WAVERLY

![project WAVERLY](static/images/favicon.png)


## Overview
Project WAVERLY is a web application, that uses text-to-speech technology provided by [Amazon Polly](https://aws.amazon.com/polly/) to allow users to save textual articles and to convert them into an audio snippet (similar to a short podcast episode) that sounds human-like.

WAVERLY supports only English articles.

![WAVERLY app ios](static/images/waverly_gif.gif)

## WAVERLY is live 🙌
Go to [https://waverly1.herokuapp.com/](https://waverly1.herokuapp.com/) and see how it works.

## Standalone Web Application
WAVERLY works beautifully as a standalone web application. Just go the [WAVERLY URL](https://waverly1.herokuapp.com/) on your mobile device, go to your account page, and save the URL to your home screen.  
This was tested only on iPhone's Safari.

> ⚠️ Because of an [iOS's limited support for HTML5](http://debuggerdotbreak.judahgabriel.com/2016/12/13/its-almost-2017-and-html5-audio-is-still-broken-on-ios/), when triggering WAVERLY from the home screen, playing an audio file won't work while the app is in the background won't work. For this reason, the recommendation to the user to save the app to the home screen has been commented in the JS code.</br><img src="static/images/homescreen.png" width="240"/>


## Deploy WAVERLY to Heroku
> 💡 WAVERLY was built on AWS's S3 and Polly. Before starting the deployment process, please make sure you have the following details for your AWS account:
  1. AWS Access Key
  1. AWS Secret Access Key
  1. S3 bucket for storing article image files
  1. S3 bucket for storing audio files

Follow these steps:

1. Clone WAVERLY's repository

2. Create heroku app
```bash
$ heroku create <APP_NAME>
```

3. Install CloudAMQP on Heroku to serve as a queue DB for worker jobs
```bash
$ heroku addons:add cloudamqp
```

4. Add worker to Heroku
```bash
$ heroku ps:scale worker=1
```

5. Set Django's secret key as environment variable on Heroku's virtual environment
```bash
$ heroku config:set SECRET_KEY=<DJANGO_SECRET_KEY>
```

6. Set AWS's access keys as environment variable on Heroku's virtual environment
```bash
$ heroku config:set AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

7. Set S3's access keys as environment variable on Heroku's virtual environment
```bash
$ heroku config:set BUCKET_IMAGES=<S3_IMAGE_FILES_BUCKET>
$ heroku config:set BUCKET_AUDIO=<S3_AUDIO_FILES_BUCKET>
```

8. Upload repository to Heroku
```bash
$ git push heroku master
```

9. Run Django migrations on Heroku
```bash
$ heroku run python3 manage.py migrate
```

## Attributions
> Built by [Dror Ayalon](https://twitter.com/drorayalon), Summer 2017.  

> Help and support by the [World Wide Web](https://www.youtube.com/watch?v=nZEw_6Y0hhU).

> Graphical resource 🖼 for the WAVERLY logo by [mikicon](https://thenounproject.com/mikicon/collection/siri/) from the noun project.
