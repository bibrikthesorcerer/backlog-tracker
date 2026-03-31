from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from service_objects.services import ServiceOutcome

from api.services import CreateMediaItem, ListMediaItems, ShowMediaItem, DeleteMediaItem, UpdateMediaItem
from api.serializers import ShowMediaItemSerializer, PageSerializer
from api.permissions import IsOwner
from api.views import BaseView


class MediaItemsView(BaseView):
    method_permissions = {
        "POST": [IsAuthenticated]
    }

    def get(self, request, *args, **kwargs):
        paginated_set = ServiceOutcome(
            ListMediaItems,
            request.query_params,
        ).result
        data = PageSerializer(
            instance=paginated_set, objects_serializer=ShowMediaItemSerializer
        ).data
        return Response(status=status.HTTP_200_OK, data=data)

    def post(self, request, *args, **kwargs):
        r = ServiceOutcome(
            CreateMediaItem,
            ({"user": request.user} | request.data),
        ).result
        data = ShowMediaItemSerializer(r).data 
        return Response(status=status.HTTP_201_CREATED, data=data)


class SingleMediaItemView(BaseView):
    method_permissions = {
        "DELETE": [IsOwner],
        "PATCH": [IsOwner]
    }

    def _get_item_with_permission_check(self):
        item = ServiceOutcome(ShowMediaItem, self.kwargs).result
        self.check_object_permissions(self.request, item)
        return item

    def get(self, request, *args, **kwargs):
        media_item = ServiceOutcome(
            ShowMediaItem,
            kwargs 
        ).result
        data = ShowMediaItemSerializer(media_item).data
        return Response(status=status.HTTP_200_OK, data=data)

    def patch(self, request, *args, **kwargs):
        item = self._get_item_with_permission_check()
        media_item = ServiceOutcome(
            UpdateMediaItem,
            ({"media_item": item} | request.data)
        ).result
        data = ShowMediaItemSerializer(media_item).data
        return Response(status=status.HTTP_200_OK, data=data)

    @extend_schema(**MI_docs.delete_media_item_docs)
    def delete(self, request, *args, **kwargs):
        self._get_item_with_permission_check()
        ServiceOutcome(
            DeleteMediaItem,
            kwargs
        )
        return Response(status=status.HTTP_204_NO_CONTENT)