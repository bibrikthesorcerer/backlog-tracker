from service_objects_autodocs.exceptions import get_access_denied_error_yasg_response


def get_no_ownership_response():
    return get_access_denied_error_yasg_response(details="You are not an owner of this resource")
