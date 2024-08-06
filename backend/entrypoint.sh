#!/bin/sh

# Ensure the media directory exists and has the correct permissions
chown -R appuser:appuser /app/media
chmod -R 777 /app/media

exec "$@"