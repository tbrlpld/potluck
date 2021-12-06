from potluck.games import factories as games_factories
from potluck.pots import models as pots_models
from potluck.teams import models as teams_models


class TestGame:
    def test_build(self):
        games_factories.Game.build()

        assert True

    def test_build_with_teams_trait(self):
        game = games_factories.Game.build(with_teams=True)

        assert isinstance(game.home_team, teams_models.Team)
        assert isinstance(game.away_team, teams_models.Team)

    def test_build_with_pot_trait(self):
        game = games_factories.Game.build(with_pot=True)

        assert isinstance(game.pot, pots_models.Pot)
