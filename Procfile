web: gunicorn waverly_project.wsgi --log-file -
worker: celery -A waverly_project worker -B --loglevel=info
