from django.db import models
from django.contrib.auth import get_user_model

from models_app.models import BaseModel


class Tag(BaseModel):
    """
    Tag can represent certain aspects of MediaItems in a short text form (1-2 word)
    """

    title = models.CharField(max_length=64)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = "tag"
        verbose_name = "tag"
        verbose_name_plural = "tags"