from django.db import models 
from django.contrib.auth import get_user_model

from models_app.models import BaseModel


class MediaItem(BaseModel):
    """
    MediaItem is an entry for a piece of Media with which user is interacting.
    """

    class Status(models.TextChoices):
        WANT = "WAN", "Want"
        IN_PROGRESS = "PRG", "In Progress"
        COMPLETED = "CMP", "Completed"
        DROPPED = "DRP", "Dropped"

    # RATING_CHOICES = [
    #     (0, "0"), (0.5, "0.5"),
    #     (1, "1"), (1.5, "1.5"),
    #     (2, "2"), (2.5, "2.5"),
    #     (3, "3"), (3.5, "3.5"),
    #     (4, "4"), (4.5, "4.5"),
    #     (5, "5"),
    # ]
    RATING_CHOICES = [(i/2, str(i/2)) for i in range(0, 11)]
    
    class MediaType(models.TextChoices):
        GAME = "GAM", "Game"
        BOOK = "BOK", "Book"
        MUSIC = "MUS", "Music"
        MOVIE = "MOV", "Movie"
    
    class PriorityLevel(models.IntegerChoices):
        VERY_LOW = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        VERY_HIGH = 5

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    status = models.CharField(
        choices=Status, default=Status.WANT, max_length=16
    )
    rating = models.FloatField(
        choices=RATING_CHOICES, default=RATING_CHOICES[0], null=True
    )
    media_type = models.CharField(
        choices=MediaType
    )
    priority = models.IntegerField(choices=PriorityLevel)
    notes = models.TextField(max_length=512, null=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    metadata = models.JSONField()
    external_id = models.IntegerField(null=True)

    class Meta:
        db_table = "media_item"
        verbose_name = "media_item"
        verbose_name_plural = "media_items" 