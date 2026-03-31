from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome

from api.views import BaseView
from api.serializers import ShowTagSerializer
from api.services import CreateTag, ListTags, ShowTag, DeleteTag
from api.permissions import IsOwner


class TagsView(BaseView):
    method_permissions = {
        "GET": [IsAuthenticated],
        "POST": [IsAuthenticated],
    }
    
    def get(self, request, *args, **kwargs):
        tags = ServiceOutcome(
            ListTags,
            {"user": request.user}
        ).result 
        data = ShowTagSerializer(tags, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)

    def post(self, request, *args, **kwargs):
        tag = ServiceOutcome(
           CreateTag,
           ({"user": request.user} | request.data) 
        ).result
        data = ShowTagSerializer(tag).data
        return Response(status=status.HTTP_201_CREATED, data=data)


class SingleTagView(BaseView):
    method_permissions = {
        "GET": [IsOwner],
        "DELETE": [IsOwner],
    }
    
    def _get_item_with_permission_check(self):
        item = ServiceOutcome(ShowTag, self.kwargs).result
        self.check_object_permissions(self.request, item)
        return item
    
    def get(self, request, *args, **kwargs):
        tag = self._get_item_with_permission_check()
        data = ShowTagSerializer(tag).data
        return Response(status=status.HTTP_200_OK, data=data)

    def delete(self, request, *args, **kwargs):
        tag = self._get_item_with_permission_check()
        ServiceOutcome(
            DeleteTag,
            {"tag": tag}
        )
        return Response(status=status.HTTP_204_NO_CONTENT)