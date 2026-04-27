from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.contrib.auth import get_user_model
from django import forms

from models_app.models import MediaItem


class CreateMediaItem(ServiceWithResult):
	user = ModelField(get_user_model())
	title = forms.CharField(max_length=64)
	status = forms.CharField(required=False)
	rating = forms.FloatField(required=False)
	media_type = forms.CharField(required=False)
	priority = forms.CharField(required=False)
	notes = forms.CharField(required=False)
	started_at = forms.DateTimeField(required=False)
	finished_at = forms.DateTimeField(required=False)
	
	def process(self):
		media_item:MediaItem = MediaItem()
		for f_name, field in self.declared_fields.items():
			f_val = self.cleaned_data.get(f_name) or None
			if f_val is not None:
				setattr(media_item, f_name, f_val)
		media_item.save()
		self.result = media_item
		return self
