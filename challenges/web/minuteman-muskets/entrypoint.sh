#!/bin/sh
echo $RANDOM > /app/token
gunicorn -w 4 --bind=0.0.0.0:8080 --pythonpath /app app:app