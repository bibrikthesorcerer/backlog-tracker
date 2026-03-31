from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.models import MediaItem


class UpdateMediaItem(ServiceWithResult):
    media_item = ModelField(MediaItem)
    title = forms.CharField(max_length=64, required=False)
    status = forms.ChoiceField(choices=MediaItem.Status, required=False)
    rating = forms.ChoiceField(choices=MediaItem.RATING_CHOICES, required=False)
    media_type = forms.ChoiceField(choices=MediaItem.MediaType, required=False)
    priority = forms.ChoiceField(choices=MediaItem.PriorityLevel, required=False)
    notes = forms.CharField(max_length=512, required=False)
    started_at = forms.DateTimeField(required=False)
    finished_at = forms.DateTimeField(required=False)
    
    def process(self):
        media_item:MediaItem = self.cleaned_data.get("media_item")
        upd_names = []
        for f_name, field in self.declared_fields.items():
            if f_name is "media_item":
                continue
            f_val = self.cleaned_data.get(f_name) or None
            if f_val is not None:
                setattr(media_item, f_name, f_val)
                upd_names.append(f_name)
        media_item.save(update_fields=upd_names) # db optimization
        self.result = media_item
        return self