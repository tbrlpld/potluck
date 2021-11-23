from potluck.pots import forms as pots_forms
from potluck.pots.tests import factories as pots_factories


class TestSetTiebreakerScoreForm:
    def test_is_valid(self):
        form = pots_forms.SetTiebreakerScoreForm({"tiebreaker_score": 1})

        result = form.is_valid()

        assert result is True

    def test_set_value_on_instance(self):
        pot = pots_factories.PotFactory.build()
        form = pots_forms.SetTiebreakerScoreForm({"tiebreaker_score": 1}, instance=pot)
        form.is_valid()

        result = pot.tiebreaker_score

        assert result == 1
