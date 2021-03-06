from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# Django rest framework ün login işlemlerini halleden bir login api view ı var.
# Tek problemi API view olarak ayarlı ve viewset option yok. Bu da demek oluyor
# ki standart default router ı url ayarlamak için kullanamayız.
# ObtainAuthToken bir APIView, bunu kullanıcam ancak kullandığım sınıfı ViewSet
# ten inherit edicem ki sistemi viewset kullanıyormuşum gibi kandırabileyim.
# Eğer kandırabilirsem url de router a register edebilirim. Ama bu hileyi
# yapmayıp api view kullanarak devam edersem admin panelinde api rootunda
# api/hello-viewset/, api/profile/ görürüm ancak api/login göremem
# api/login/ e gittiğimde HTTP Not allowed görme sebebim loginde sadece post
# yapılabilmesi loginde iken get yapamam.
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

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

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)'
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code'
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an object."""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handles updating part of an object."""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    """authentication_classes ve permission_classes değişkenlerinin tuple olarak
    tanımlanma sebebi immutable olmasını sağlaması ve sonrasında birden çok
    authentication class ya da permission class eklemek isteyebilirim. Tuple
    olması buna olanak sağlar. """
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save(user_profile=self.request.user)
