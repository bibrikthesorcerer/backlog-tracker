from django.db import models

from models_app.models import BaseModel, MediaItem


class Tag(BaseModel):
    """
    Tag is a model which 
    """
    title = models.CharField(max_length=64)
    media_items = models.ManyToManyField(to=MediaItem, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "tag"
        verbose_name = "tag"
        verbose_name_plural = "tags"