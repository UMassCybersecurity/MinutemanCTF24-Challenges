#!/bin/sh
mkdir static
zip static/web_minuteman_http.zip -r src Dockerfile docker-compose.yaml entrypoint.sh