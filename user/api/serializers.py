from rest_framework import serializers


class SocialMediaSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mode = serializers.CharField(required=True)
