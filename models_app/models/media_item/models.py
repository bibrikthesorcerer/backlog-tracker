from django.db import models 
from django.contrib.auth import get_user_model

from models_app.models import BaseModel, Tag


class MediaItem(BaseModel):
    """
    MediaItem is an entry for a piece of Media with which user is interacting.
    """

    class Status(models.TextChoices):
        WANT = "want", "Want"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        DROPPED = "dropped", "Dropped"

    RATING_CHOICES = [(i/2, str(i/2)) for i in range(0, 11)]
    
    class MediaType(models.TextChoices):
        GAME = "game", "Game"
        BOOK = "book", "Book"
        MUSIC = "music", "Music"
        MOVIE = "movie", "Movie"
        TV_SHOW = "series", "TV Show"
        MANGA = "manga", "Manga"
        ANIME = "anime", "Anime"
    
    class PriorityLevel(models.IntegerChoices):
        VERY_LOW = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        VERY_HIGH = 5

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    status = models.CharField(
        choices=Status, default=Status.WANT, max_length=16, blank=True
    )
    rating = models.FloatField(
        choices=RATING_CHOICES, null=True, blank=True
    )
    media_type = models.CharField(
        choices=MediaType, max_length=16
    )
    tags = models.ManyToManyField(to=Tag)
    priority = models.IntegerField(choices=PriorityLevel, null=True, blank=True)
    notes = models.TextField(max_length=512, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    external_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"({self.id}) {self.title}"

    class Meta:
        ordering = ['-updated_at']
        db_table = "media_item"
        verbose_name = "media_item"
        verbose_name_plural = "media_items" 