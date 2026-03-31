import factory
from factory import fuzzy, SubFactory

from models_app.factories import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Tag"
        
    title=fuzzy.FuzzyText(length=10)
    user=SubFactory(UserFactory)