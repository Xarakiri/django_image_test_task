from rest_framework import parsers, permissions, status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Image
from .serializers import (ImageSerializer, LoginSerializer,
                          RegistrationSerializer, UserSerializer)


class RegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user
    
    def get_object(self):
        return self.get_queryset()


class ImageView(GenericAPIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        images = dict((request.data).lists())['image']
        for image in images:
            serializer = ImageSerializer(data={'image': image})
            if serializer.is_valid():
                Image.objects.create(image=image)
            else:
                 return Response({'error': 'Failed to load images'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_200_OK)
