from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .renderers import UserJSONRenderer
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer




class RegistrationAPIView(APIView):
    permission_class = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        
        serializer = self.serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_class = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    # Burada yaptığımız gibi `serializer.save()` çağırmadığımıza dikkat edin. # kayıt bitiş noktası.
    #Bunun nedeni, aslında sahip olmadığımız kaydedilecek her şey. Bunun yerine, serileştiricimizdeki 'validate' yöntemi # ihtiyacımız olan her şeyi halleder.
    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer(data=user)
        serializer.is_valid(raise_exception=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):

        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def update(self, request, *args, **kwargs):

        user_data = request.data.get('user', {})

        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            
            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('iamge', request.user.profile.image)
            }
        }

        serializer = self.serializer_class( request.user, data=serializer_data, partial=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)