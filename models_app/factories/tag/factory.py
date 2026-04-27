import factory
from factory import fuzzy, SubFactory

from models_app.factories.user import UserFactory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Tag"
        
    title=fuzzy.FuzzyText(length=10)
    user=SubFactory(UserFactory)
    

    @factory.post_generation
    def media_items(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for mi in extracted:
                obj.mediaitem_set.add(mi)