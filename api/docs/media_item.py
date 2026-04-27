from drf_spectacular.utils import OpenApiResponse
from service_objects_autodocs.auto_parameters_spectacular import prepare_parameters_for_docs, prepare_request_body_for_docs
from service_objects_autodocs.common import add_pagination_to_data_serializer
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response, get_not_found_error_yasg_response,
    get_validation_error_yasg_response
)
    
from api.services import ListMediaItems, CreateMediaItem, ShowMediaItem, UpdateMediaItem, DeleteMediaItem
from api.serializers import ShowMediaItemSerializer
from api.docs.utils import get_no_ownership_response


list_media_items_docs = {
    "summary": "Get a paginated list of Media Items",
    "description": "Returns paginated list of Media Items with applied pagination, search, order and filters.",
    "parameters": prepare_parameters_for_docs(ListMediaItems, exclude=["user"]),
    "responses": {
        "200": OpenApiResponse(
            response=add_pagination_to_data_serializer(ShowMediaItemSerializer)
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    },
}


create_media_item_docs = {
    "summary": "Create Media Item",
    "description": "Uses given data to create Media Item. Provide at least `title` and `media_type`.",
    "request": prepare_request_body_for_docs(CreateMediaItem, exclude=("user",)),
    "responses": {
        "201": OpenApiResponse(
            response=ShowMediaItemSerializer
        ),
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
    }
}


show_media_item_docs = {
    "summary": "Show single Media Item",
    "description": "Shows Media Item according to given ID. Also includes associated Tags.",
    "parameters": prepare_parameters_for_docs(ShowMediaItem, exclude=("id",)),
    "responses": {
        "200": ShowMediaItemSerializer,
        "401": get_authentication_failed_yasg_response(),
        "403": get_no_ownership_response(),
        "404": get_not_found_error_yasg_response()
    },
}

update_media_item_docs = {
    "summary": "Partially update Media Item",
    "description": "Update Media Item with given values. Only given parameters will be updated.",
    "request": prepare_request_body_for_docs(UpdateMediaItem, exclude=("media_item",)),
    "responses": {
        "200": ShowMediaItemSerializer,
        "400": get_validation_error_yasg_response(),
        "401": get_authentication_failed_yasg_response(),
        "403": get_no_ownership_response(),
        "404": get_not_found_error_yasg_response(),
    }
}


delete_media_item_docs = {
    "summary": "Delete Media Item",
    "description": "Delete Media Item with given ID. *Only owner of Media Item can delete it.*",
    "parameters": prepare_parameters_for_docs(DeleteMediaItem, exclude=("media_item",)),
    "responses": {
        "204": "",
        "401": get_authentication_failed_yasg_response(),
        "403": get_no_ownership_response(),
        "404": get_not_found_error_yasg_response(),
    }
}