import factory
from factory import fuzzy

from potluck.picks.models import Pick, PickSheet


class PickSheetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PickSheet

    picker = factory.Faker("first_name")
    tiebreaker_guess = fuzzy.FuzzyInteger(1, 100)


class PickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pick
