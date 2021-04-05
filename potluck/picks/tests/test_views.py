import http

from django import test
from django import urls
import pytest

from potluck.pots.tests.factories import PotFactory


@pytest.mark.django_db
class TestPickCreateView:
    def test_get_success(self):
        pot = PotFactory.create()
        url = urls.reverse("pick_create", kwargs={"pot_id": pot.id})
        client = test.Client()

        response = client.get(url)

        assert response.status_code == http.HTTPStatus.OK
