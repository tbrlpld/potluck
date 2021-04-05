from django.core import exceptions
import pytest

from potluck.games.models import Game
from potluck.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestGame:
    def test_full_clean_validation_error_one_team(self):
        team_1 = TeamFactory.create()
        game = Game()
        game.save()
        game.teams.add(team_1)

        with pytest.raises(exceptions.ValidationError):
            game.full_clean()
