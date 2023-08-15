import pytest
from django.urls import reverse
from rest_framework import status

from challenge.shorturls.models import UrlShort


@pytest.mark.django_db
def test_short_url(client):
    url = reverse('short-url')
    data = {'url': 'https://google.com/'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'short_url' in response.data


@pytest.mark.django_db
def test_short_url_fail(client):
    url = reverse('short-url')
    data = {}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_short_url_to_origin(client):
    origin_url = 'https://google.com/'
    url_obj = UrlShort.objects.create(url=origin_url)
    short_code = url_obj.short
    url = reverse('short-url-redirect', args=[short_code])
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == origin_url


@pytest.mark.django_db
def test_short_url_top(client):
    url = reverse('top-100')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
