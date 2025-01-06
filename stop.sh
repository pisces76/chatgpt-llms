pkill -f 'gunicorn -w 3 -b :8080 -t 100 wsgi:app'
