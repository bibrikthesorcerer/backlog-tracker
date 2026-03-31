from rest_framework import serializers

from models_app.models import MediaItem
from api.serializers.tag import ShowTagSerializer


class ShowMediaItemSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username") 
    tags = ShowTagSerializer(many=True)
    class Meta:
        model = MediaItem 
        exclude = ["external_id", "user"]