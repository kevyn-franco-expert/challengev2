from rest_framework import serializers

from challenge.shorturls.models import UrlShort


class ShortUrlSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        url_obj, created = UrlShort.objects.get_or_create(url=validated_data.get('url'))
        return url_obj

    class Meta:
        model = UrlShort
        fields = "__all__"
