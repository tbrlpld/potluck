import pytest

from potluck.picks import forms
from potluck.pots.tests import factories as pot_factories


class TestCreatePickSheet:
    def test_create_empty(self):
        with pytest.raises(TypeError):
            forms.CreatePickSheet()

    def test_create_without_data(self):
        pot = pot_factories.PotFactory.build()
        form = forms.CreatePickSheet(pot=pot)

        assert form.is_valid() is False

    def test_create_valid_form(self):
        pot = pot_factories.PotFactory.build()
        form = forms.CreatePickSheet(
            data={
                "picker": "Joe Shmoe",
                "tiebreaker_guess": 10,
            },
            pot=pot,
        )

        assert form.is_valid() is True
        pick_sheet = form.save(commit=False)
        assert pick_sheet.pot == pot


class TestCreatePick:
    def test_create_empty(self):
        with pytest.raises(ValueError):
            form = forms.CreatePick()

