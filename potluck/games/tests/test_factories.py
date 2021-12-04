from potluck.games import factories as games_factories
from potluck.teams import models as teams_models


class TestGame:
    def test_init(self):
        game = games_factories.Game.build()

        assert True

    def test_with_teams_trait(self):
        game = games_factories.Game.build(with_teams=True)

        assert isinstance(game.home_team, teams_models.Team)
        assert isinstance(game.away_team, teams_models.Team)
