echo "" > service.log
date '+%Y-%m-%d %H:%M:%S' >> service.log
nohup gunicorn -w 3 -b :8080 -t 100 wsgi:app >> service.log &
echo "Start llm service complete!"
tail -f service.log

