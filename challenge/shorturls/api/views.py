from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.common.convert import Covert
from challenge.shorturls.models import UrlShort
from .serializers import ShortUrlSerializer


class ShortURLView(APIView):
    permission_classes = ()
    serializer_class = ShortUrlSerializer

    def post(self, request):

        url = self.request.data.get('url')

        if not url:
            return Response({'error': 'URL not provided', }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data={'url': url})
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response(
                {
                    'short_url': f"{request.build_absolute_uri('/')} {result.short}",
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({'error': 'INTERNAL ERROR', }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RedirectURLView(APIView):
    permission_classes = ()

    def get(self, request, short_code):
        convert = Covert()
        url_id = convert.decode_from_base64(short_code)
        url_obj = get_object_or_404(UrlShort, id=url_id)
        url_obj.access_count += 1
        url_obj.save()
        return redirect(url_obj.url)


class RedirectURLTOP100View(APIView):
    permission_classes = ()

    def get(self, request):
        url = UrlShort.objects.all().order_by('-access_count').values('title', 'short')[:100]
        return Response(
            url,
            status=status.HTTP_200_OK
        )
