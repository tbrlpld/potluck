import factory

from potluck.pots.models import Pot


class PotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pot

    name = factory.Sequence(lambda n: f"Test Pot {n}")

    games = factory.RelatedFactoryList(
        "potluck.games.tests.factories.GameFactory",
        factory_related_name="pot",
        size=2,
    )
