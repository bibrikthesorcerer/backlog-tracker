from service_objects.services import ServiceWithResult
from django.db.models import QuerySet
from django import forms

from models_app.models import MediaItem


class ShowMediaItem(ServiceWithResult):
    id = forms.IntegerField()
    
    def process(self):
        qs = MediaItem.objects.all()
        qs = self._prefetch_tags(qs)
        qs = self._select_rel_user(qs)
        self.result = qs.get(id=self.cleaned_data.get("id"))
        return self

    def _prefetch_tags(self, qs: QuerySet):
        qs = qs.prefetch_related("tags")
        return qs

    def _select_rel_user(self, qs: QuerySet):
        qs = qs.select_related("user")
        return qs
