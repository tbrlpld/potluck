import factory

from potluck.picks.models import Pick, PickSheet


class PickSheetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PickSheet

    picker = factory.Faker("first_name")


class PickFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pick
