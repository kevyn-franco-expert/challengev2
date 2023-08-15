import requests
from bs4 import BeautifulSoup
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from challenge.common.convert import Covert


class UrlShort(models.Model):
    url = models.URLField()

    # TODO validate max_length per short link
    short = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    title = models.TextField(
        null=True,
        blank=True
    )

    access_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str


@receiver(post_save, sender=UrlShort)
def convert_id_to_short_code(sender, instance, created, **kwargs):
    if created:
        convert = Covert()
        instance.short = convert.encode_to_base64(instance.id)
        url = requests.get(instance.url)
        soup = BeautifulSoup(url.content, 'html.parser')
        title = soup.find('title').getText() if soup.find('title') else None
        instance.title = title
        instance.save()
