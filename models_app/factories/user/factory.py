import factory
from django.utils import timezone
from factory import fuzzy
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    date_joined = fuzzy.FuzzyDateTime(start_dt=timezone.now())
    password = factory.PostGenerationMethodCall("set_password", "testpass123")

    class Params:
        admin = factory.Trait(
            is_staff=True, is_superuser=True
        )
        user = factory.Trait(
            is_staff=False, is_superuser=False
        )
