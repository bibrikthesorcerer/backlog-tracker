from service_objects.services import ServiceWithResult
from django.contrib.auth import get_user_model
from django.forms import fields


class CreateUserService(ServiceWithResult):
    username = fields.CharField()
    password = fields.CharField()
    
    def process(self):
        self.result = get_user_model().objects.create_user(
            self.cleaned_data.get("username"),
            None,
            self.cleaned_data.get("password")
        )
        return self