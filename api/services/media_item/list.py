from service_objects.services import ServiceWithResult
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from config import proj_settings
from django import forms

from models_app.models import MediaItem


class ListMediaItems(ServiceWithResult):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    search = forms.CharField(required=False)
    
    __fields = [
        "title", "status", "rating",
        "media_type", "created_at", "priority",
        "started_at", "finished_at"
    ]
    __orderings = [val for f in __fields for val in ((f, ''), (f'-{f}', ''))]
    order = forms.ChoiceField(choices=__orderings, required=False)
    
    def process(self):
        self.result = self._get_paginated_queryset()
        return self

    def _get_paginated_queryset(self) -> Page:
        qs = MediaItem.objects.all()
        # search ordering takes priority over field ordering
        qs = self._apply_ordering(qs)
        qs = self._search_for_entry(qs)
        qs = self._prefetch_tags(qs)
        qs = self._select_rel_user(qs)
        per_page = self.cleaned_data.get("per_page") or proj_settings.PAGINATION.media_items
        page = self.cleaned_data.get("page")
        return Paginator(qs, per_page).get_page(page)
        
    def _search_for_entry(self, qs: QuerySet):
        search_query = self.cleaned_data.get("search")
        if search_query:
            qs = qs.annotate(
                search=SearchVector("title", weight="A") + SearchVector("notes", weight="B"),
                similarity=TrigramSimilarity("title", search_query)
            ).filter(search=search_query).order_by("-similarity")
        return qs
        
    def _apply_ordering(self, qs: QuerySet):
        order = self.cleaned_data.get("order")
        if order:
            qs = qs.order_by(order)
        return qs

    def _prefetch_tags(self, qs: QuerySet):
        qs = qs.prefetch_related("tags")        
        return qs

    def _select_rel_user(self, qs: QuerySet):
        qs = qs.select_related("user")
        return qs