import factory


from potluck.pots.models import Pot


class PotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pot

    name = "Test Pot"
