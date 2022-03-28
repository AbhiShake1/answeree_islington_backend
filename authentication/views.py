from typing import Optional

from braces.views import CsrfExemptMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


# Create your views here.
class SignupView(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request: HttpRequest) -> Response:
        def get(key: str) -> Optional[str]:
            return request.POST[key] if key in request.POST else None

        try:
            uid = get('uid')
            email = get('email')
            password = get('password')
            user: User = User.objects.create_user(uid, email=email, password=password)
            user.save()
            seerializer = UserSerializer(user)
            return Response(seerializer.data)
        except:
            return Response('User already exists', status=401)


class SigninView(CsrfExemptMixin, APIView):
    authentication_classes = []

    def post(self, request: HttpRequest) -> Response:
        def get(key: str) -> Optional[str]:
            return request.POST[key] if key in request.POST else None

        try:
            uid = get('uid')
            password = get('password')
            user: User = authenticate(username=uid, password=password)
            user.save()
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return Response('Invalid credentials', status=401)


class SignoutView(CsrfExemptMixin, APIView):
    authentication_classes = []

    def get(self, request: HttpRequest) -> Response:
        try:
            user: User = request.user
            if user is not None:
                logout(user)
                return Response('Successful')
        except:
            return Response('Something went wrong', status=403)
        return Response('No user found.', status=403)
