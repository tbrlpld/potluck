from django.test import Client
import pytest

from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPotDetailView:
    def test_title(self):
        pot = PotFactory.create()

        assert True