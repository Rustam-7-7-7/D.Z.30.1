from rest_framework import serializers

def validate_youtube_url(value):
    if not value.startswith("https://www.youtube.com/"):
        raise serializers.ValidationError("URL must be a valid YouTube link.")
    return value
