from potluck.pots.forms import SetTiebreakerScoreForm
from potluck.pots.tests import factories as pots_factories


class TestSetTiebreakerScoreForm:
    def test_is_valid(self):
        form = SetTiebreakerScoreForm({"tiebreaker_score": 1})

        result = form.is_valid()

        assert result is True

    def test_set_value_on_instance(self):
        pot = pots_factories.PotFactory.build()
        form = SetTiebreakerScoreForm({"tiebreaker_score": 1}, instance=pot)
        form.is_valid()

        result = pot.tiebreaker_score

        assert result == 1
