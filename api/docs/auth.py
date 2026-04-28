from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from service_objects_autodocs.auto_parameters_spectacular import prepare_request_body_for_docs
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_validation_error_yasg_response
)
    
from api.services import CreateUserService


register_docs = {
    "summary": "Register user with given username and password",
    "request": prepare_request_body_for_docs(CreateUserService),
    "responses": {
        "200": "",
        "400": get_validation_error_yasg_response(),
    },
}

login_docs = {
    "summary": "Log a User in and get SessionID with CSRFToken.",
    "request": inline_serializer(
        name="CustomLoginRequest",
        fields={
            "username": serializers.CharField(),
            "password": serializers.CharField() 
        },
    ),
    "responses": {
        "200": "",
        "401": get_authentication_failed_yasg_response(),
    }
}

logout_docs = {
    "summary": "Log User out. Request must contain CSRFToken and SessionID headers.",
    "responses": {
        "200": "",
    }
}