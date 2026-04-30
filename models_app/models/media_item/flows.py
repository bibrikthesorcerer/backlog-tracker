from viewflow.fsm import State
from django.utils import timezone

from .models import MediaItem


class MediaItemLifecycle:
    state = State(states=MediaItem.Status, default=MediaItem.Status.WANT)
    
    def __init__(self, media_item):
        self.media_item: MediaItem = media_item
    
    @state.getter()
    def _get_media_item_status(self):
        return self.media_item.status

    @state.transition(MediaItem.Status.WANT, MediaItem.Status.IN_PROGRESS)
    def start(self):
        self.media_item.status = MediaItem.Status.IN_PROGRESS
        self.media_item.started_at = timezone.now()
        self.media_item.save()

    @state.transition(MediaItem.Status.IN_PROGRESS, MediaItem.Status.COMPLETED)
    def complete(self):
        self.media_item.status = MediaItem.Status.COMPLETED
        self.media_item.finished_at = timezone.now()
        self.media_item.save()

    @state.transition((MediaItem.Status.IN_PROGRESS, MediaItem.Status.WANT), MediaItem.Status.DROPPED)
    def drop(self):
        self.media_item.status = MediaItem.Status.DROPPED
        self.media_item.save()