#!/bin/sh
gunicorn -w 4 --bind=0.0.0.0:4444 --pythonpath /app app:app
