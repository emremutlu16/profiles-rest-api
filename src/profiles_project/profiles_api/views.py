from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status

from . import serializers
# Create your views here.

class HelloApiView(APIView):
    """Test API View."""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        an_apiview= [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name."""

        serilizer = serializers.HelloSerializer(data=request.data)
        #serializer = self.serializer_class(data=request.data) kullanılabilir,
        # aynı işi görüyor. serializer_class tanımlanın temel amacı Django REST
        # Framework otomatik olarak generate edilen HTML formunda brow-sable API
        # için hangi alanın sağlanacağını biliyor olması.
        if serilizer.is_valid():
            name = serilizer.data.get('name')
            message = 'Hello {}'.format(name)
            return Response({'message': message})
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an object."""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})

    def delete(self, reques, pk=None):
        """Delete an object"""

        return Response({'method': 'delete'})
