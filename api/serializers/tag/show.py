from rest_framework.serializers import ModelSerializer

from models_app.models import Tag


class ShowTagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["user"]