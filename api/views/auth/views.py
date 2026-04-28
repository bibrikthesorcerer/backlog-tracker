from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome

from api.views import BaseView
from api.services import CreateUserService
from api.docs import auth


class LoginView(BaseView):
    @extend_schema(**auth.login_docs)
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(BaseView):
    @extend_schema(**auth.logout_docs)
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class RegisterView(BaseView):
    @extend_schema(**auth.register_docs)
    def post(self, request, *args, **kwargs):
        ServiceOutcome(
            CreateUserService,
            request.data
        )
        return Response(status=status.HTTP_200_OK)