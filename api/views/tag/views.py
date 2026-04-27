from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome
from drf_spectacular.utils import extend_schema

from api.views import BaseView
from api.serializers import ShowTagSerializer
from api.services import CreateTag, ListTags, ShowTag, DeleteTag
from api.permissions import IsOwner
from api.docs import tag as TAG_docs


class TagsView(BaseView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(**TAG_docs.list_tags_docs)
    def get(self, request, *args, **kwargs):
        tags = ServiceOutcome(
            ListTags,
            {"user": request.user}
        ).result 
        data = ShowTagSerializer(tags, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)

    @extend_schema(**TAG_docs.create_tag_docs)
    def post(self, request, *args, **kwargs):
        tag = ServiceOutcome(
           CreateTag,
           ({"user": request.user} | request.data) 
        ).result
        data = ShowTagSerializer(tag).data
        return Response(status=status.HTTP_201_CREATED, data=data)


class SingleTagView(BaseView):
    permission_classes = [IsOwner]
    
    def _get_item_with_permission_check(self):
        item = ServiceOutcome(ShowTag, self.kwargs).result
        self.check_object_permissions(self.request, item)
        return item
    
    @extend_schema(**TAG_docs.show_tag_docs)
    def get(self, request, *args, **kwargs):
        tag = self._get_item_with_permission_check()
        data = ShowTagSerializer(tag).data
        return Response(status=status.HTTP_200_OK, data=data)

    @extend_schema(**TAG_docs.delete_tag_docs)
    def delete(self, request, *args, **kwargs):
        tag = self._get_item_with_permission_check()
        trulyDeleted = ServiceOutcome(
            DeleteTag,
            ({"tag": tag, "user": request.user} | request.data)
        ).result
        return Response(status=status.HTTP_200_OK, data={"trulyDeleted": trulyDeleted})