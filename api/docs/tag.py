from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers
from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs 
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response, get_not_found_error_yasg_response,
    get_yasg_response_with_nested_exception_details, get_validation_error_yasg_response
)
    
from api.services import ListTags, CreateTag, ShowTag, DeleteTag
from api.serializers import ShowTagSerializer
from api.docs.utils import get_no_ownership_response


list_tags_docs = {
    "summary": "Get a list of user's Tags",
    "description": "Returns plain list of user's Tags",
    "parameters": prepare_parameters_for_docs(ListTags, exclude=("user",)),
    "responses": {
        "200": OpenApiResponse(
            response=ShowTagSerializer
        ),
        "401": get_authentication_failed_yasg_response()
    }
}

create_tag_docs = {
    "summary": "Create a Tag on a MediaItem",
    "description": "Creates a Tag with given title for a MediaItem with specified ID. If tag with given title is present, it'll just bind it to MediaItem.",
    "request": prepare_request_body_for_docs(CreateTag, exclude=("user",)),
    "responses": {
        "201": OpenApiResponse(
            response=ShowTagSerializer
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
        "404": get_yasg_response_with_nested_exception_details(
            description="Not found",
            exception_type="NotFound",
            message="MediaItem with given ID does not exist.",
            translation_key="not_found",
            debug_message="Specify existing MediaItem ID",
            details_dict={}
            )
    }
}


show_tag_docs = {
    "summary": "Show user's Tag",
    "description": "Returns single Tag with corresponding data. Only Tag's owner can view it.",
    "parameters": prepare_parameters_for_docs(ShowTag),
    "responses": {
        "200": OpenApiResponse(
            response=ShowTagSerializer
        ),
        "401": get_authentication_failed_yasg_response(),
        "403": get_no_ownership_response(),
        "404": get_not_found_error_yasg_response()
    }
}

delete_tag_docs = {
    "summary": "Delete user's Tag from specified MediaItem",
    "description": "Only Tag's owner can delete it. If a Tag becomes an orphan, it will be deleted from DB.",
    "parameters": prepare_parameters_for_docs(DeleteTag, exclude=("tag", "user",)),
    "responses": {
        "200": OpenApiResponse(
            response=inline_serializer(
                name="CustomTagDeleteResponse",
                fields={"trulyDeleted": serializers.BooleanField()},
            ),
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
        "403": get_no_ownership_response(),
        "404": get_not_found_error_yasg_response()
    }
}