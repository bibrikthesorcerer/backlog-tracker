import json

from service_objects.services import ServiceOutcome, ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import ValidationError
from viewflow.fsm import TransitionNotAllowed
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django import forms

from api.services.media_item.list import ListMediaItems, ListMediaItemsQueue
from api.serializers import ShowCurationSerializer
from models_app.models import MediaItem
from models_app.models.media_item.flows import MediaItemLifecycle


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
            if f_name == "media_item":
                continue
            f_val = self.cleaned_data.get(f_name) or None
            if f_val is not None:
                setattr(media_item, f_name, f_val)
                upd_names.append(f_name)
        media_item.save(update_fields=upd_names) # db optimization
        self.result = media_item
        return self


class HandleMediaItemLifecycle(ServiceWithResult):
    media_item = ModelField(MediaItem)
    ACTIONS = (
        ("start", ""),
        ("complete", ""),
        ("drop", ""),
    )
    action = forms.ChoiceField(choices=ACTIONS)
    
    def process(self):
        flow = MediaItemLifecycle(self.cleaned_data.get("media_item"))
        action_name = self.cleaned_data.get("action")
        transition_func = getattr(flow, action_name) # get bound method
        try:
            transition_func()
        except TransitionNotAllowed:
            self.add_error("action", ValidationError(message="This transition on this MediaItem is not allowed"))
            self.stop_process()
        return self


class SendCurationEMail(ServiceWithResult):
    user = ModelField(get_user_model()) 

    def process(self):
        # get items
        user = self.cleaned_data.get("user")
        queue = ServiceOutcome(
            ListMediaItemsQueue,
            {"user": user}
        ).result
        started = ServiceOutcome(
            ListMediaItems,
            {"user": user, "status": MediaItem.Status.IN_PROGRESS}
        ).result
        
        data = {"queue": queue, "started": started}

        serialized = ShowCurationSerializer(data).data
        text_content = json.dumps(serialized, indent=4, ensure_ascii=False)

        data.update({"username": user.username})
        html_content = render_to_string("api/curation.html", data)
        msg = EmailMultiAlternatives(
            subject="Your daily curation from Backlog",
            body=text_content,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        self.result = msg
        return self