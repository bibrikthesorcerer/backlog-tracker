from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.core.paginator import Page, Paginator
from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q, F, ExpressionWrapper, FloatField, DurationField
from django.db.models.functions import Ln, Now, ExtractDay, Cast
from config import proj_settings
from django import forms

from models_app.models import MediaItem


class ListMediaItems(ServiceWithResult):
    search = forms.CharField(required=False)
    tag_id = forms.IntegerField(required=False) #TODO: make it a list?
    status =forms.ChoiceField(required=False, choices=MediaItem.Status)
    user = ModelField(get_user_model())
    
    __fields = [
        "title", "status", "rating",
        "media_type", "created_at", "priority",
        "started_at", "finished_at"
    ]
    __orderings = [val for f in __fields for val in ((f, ''), (f'-{f}', ''))]
    order = forms.ChoiceField(choices=__orderings, required=False)
    
    def process(self):
        self.result = self._form_queryset()
        return self
    
    def _form_queryset(self) -> QuerySet:
        qs = MediaItem.objects.all()
        # search ordering takes priority over field ordering
        qs = self._apply_ordering(qs)
        qs = self._search_for_entry(qs)
        qs = self._prefetch_tags(qs)
        qs = self._select_rel_user(qs)
        qs = self._apply_filters(qs)
        return qs
        
    def _search_for_entry(self, qs: QuerySet) -> QuerySet:
        search_query = self.cleaned_data.get("search")
        if search_query:
            qs = qs.annotate(
                search=SearchVector("title", weight="A") + SearchVector("notes", weight="B"),
                similarity=TrigramSimilarity("title", search_query)
            ).filter(search=search_query).order_by("-similarity")
        return qs
        
    def _apply_ordering(self, qs: QuerySet) -> QuerySet:
        order = self.cleaned_data.get("order")
        if order:
            qs = qs.order_by(order, "-id")
        return qs

    def _prefetch_tags(self, qs: QuerySet) -> QuerySet:
        qs = qs.prefetch_related("tags")        
        return qs

    def _select_rel_user(self, qs: QuerySet) -> QuerySet:
        qs = qs.select_related("user")
        return qs

    def _build_filters(self) -> Q:
        filters = Q()

        tag_id = self.cleaned_data.get("tag_id")
        if tag_id:
            filters &= Q(tags_in=[tag_id])
        
        status = self.cleaned_data.get("status") 
        if status:
            filters &= Q(status=status)

        filters &= Q(user=self.cleaned_data.get("user"))
        return filters

    def _apply_filters(self, qs: QuerySet) -> QuerySet:
        qs = qs.filter(self._build_filters())
        return qs


class ListMediaItemsWithPagination(ListMediaItems):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)

    def process(self):
        qs = super().process().result
        self.result = self._add_pagination_to_qs(qs)
        return self
        
    def _add_pagination_to_qs(self, qs: QuerySet) -> Page:
        per_page = self.cleaned_data.get("per_page") or proj_settings.get("PAGINATION.media_items", 10)
        page = self.cleaned_data.get("page")
        return Paginator(qs, per_page).get_page(page)


class ListMediaItemsQueue(ListMediaItems):
    
    def process(self):
        qs = super().process().result
        self.result = self._calc_score(qs)
        return self

    def _build_filters(self) -> Q:
        filters = super()._build_filters()
        filters &= Q(priority__isnull=False)
        filters &= Q(status=MediaItem.Status.WANT)
        return filters

    def _calc_score(self, qs: QuerySet) -> QuerySet:
        days = ExtractDay(ExpressionWrapper(
            Now() - F("created_at"),
            output_field=DurationField()
        ))
        qs = qs.annotate(score=ExpressionWrapper(
            F("priority") * 7 + 3/(Ln(Cast(days, FloatField())+2) * 10),
            output_field=FloatField()
        ))
        qs = qs.order_by("-score", "-created_at", "-id")[:proj_settings.get("PAGINATION.queue_N", 5)]
        return qs