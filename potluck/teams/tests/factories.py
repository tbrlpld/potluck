import factory

from potluck.teams.models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: "Test Team {0}".format(n))
