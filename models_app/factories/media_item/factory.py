import factory
from django.utils import timezone
from factory import fuzzy, SubFactory

from models_app.factories.user import UserFactory
from models_app.models import MediaItem


class MediaItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.MediaItem"

    user = SubFactory(UserFactory)
    title = fuzzy.FuzzyText(length=32)
    status = fuzzy.FuzzyChoice(
        choices=[""]+list(MediaItem.Status),
    )
    rating = fuzzy.FuzzyChoice(
        choices=[""]+[x[0] for x in MediaItem.RATING_CHOICES],
    )
    media_type = fuzzy.FuzzyChoice(
        choices=MediaItem.MediaType,
    )
    priority = fuzzy.FuzzyChoice(
        choices=[""]+list(MediaItem.PriorityLevel),
    )
    notes = fuzzy.FuzzyText(length=64)

    class Params:
        want = factory.Trait(
            status=MediaItem.Status.WANT,
            started_at=None,
            finished_at=None
        )
        in_progress = factory.Trait(
            status=MediaItem.Status.IN_PROGRESS,
            started_at=fuzzy.FuzzyDateTime(start_dt=timezone.now() - timezone.timedelta(weeks=1)),
            finished_at=None
        )
        completed = factory.Trait(
            status=MediaItem.Status.COMPLETED,
            started_at=fuzzy.FuzzyDateTime(start_dt=timezone.now() - timezone.timedelta(weeks=1)),
            finished_at=timezone.now()
        )
        dropped = factory.Trait(
            status=MediaItem.Status.DROPPED,
            started_at=fuzzy.FuzzyDateTime(start_dt=timezone.now() - timezone.timedelta(weeks=1)),
            finished_at=timezone.now()
        )