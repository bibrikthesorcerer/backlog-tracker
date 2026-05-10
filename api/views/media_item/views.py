from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from service_objects.services import ServiceOutcome
from drf_spectacular.utils import extend_schema

from api.services import (
    CreateMediaItem,
    ListMediaItemsWithPagination, ListMediaItemsQueue,
    ShowMediaItem, DeleteMediaItem,
    UpdateMediaItem, HandleMediaItemLifecycle
)
from api.serializers import ShowMediaItemSerializer, PageSerializer
from api.permissions import IsOwner
from api.docs import media_item as MI_docs
from api.views import BaseView


class MediaItemsView(BaseView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**MI_docs.list_media_items_docs)
    def get(self, request, *args, **kwargs):
        inputs = request.query_params.dict() #NOTE: omits list values. see QueryDict.lists() for more
        inputs.update({"user": request.user})
        paginated_set = ServiceOutcome(
            ListMediaItemsWithPagination,
            inputs
        ).result
        data = PageSerializer(
            instance=paginated_set, objects_serializer=ShowMediaItemSerializer
        ).data
        return Response(status=status.HTTP_200_OK, data=data)

    @extend_schema(**MI_docs.create_media_item_docs)
    def post(self, request, *args, **kwargs):
        r = ServiceOutcome(
            CreateMediaItem,
            ({"user": request.user} | request.data),
        ).result
        data = ShowMediaItemSerializer(r).data 
        return Response(status=status.HTTP_201_CREATED, data=data)


class SingleMediaItemView(BaseView):
    permission_classes = [IsOwner]

    def _get_item_with_permission_check(self):
        item = ServiceOutcome(ShowMediaItem, self.kwargs).result
        self.check_object_permissions(self.request, item)
        return item

    @extend_schema(**MI_docs.show_media_item_docs)
    def get(self, request, *args, **kwargs):
        media_item = self._get_item_with_permission_check()
        data = ShowMediaItemSerializer(media_item).data
        return Response(status=status.HTTP_200_OK, data=data)

    @extend_schema(**MI_docs.update_media_item_docs)
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
        mi = self._get_item_with_permission_check()
        ServiceOutcome(
            DeleteMediaItem,
            ({"media_item": mi} | kwargs)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaItemLifecycleView(BaseView):
    permission_classes = [IsOwner]
    action = None

    def _get_item_with_permission_check(self):
        item = ServiceOutcome(ShowMediaItem, self.kwargs).result
        self.check_object_permissions(self.request, item)
        return item

    @extend_schema(**MI_docs.media_items_lifecycle_docs)
    def post(self, request, *args, **kwargs):
        item = self._get_item_with_permission_check()
        ServiceOutcome(
            HandleMediaItemLifecycle,
            {"media_item": item, "action": self.action}
        )
        return Response(status=status.HTTP_200_OK)


class MediaItemQueueView(BaseView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**MI_docs.media_items_queue_docs)
    def get(self, request, *args, **kwargs):
        items = ServiceOutcome(
           ListMediaItemsQueue,
           {"user": request.user}
        ).result
        data = ShowMediaItemSerializer(items, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)