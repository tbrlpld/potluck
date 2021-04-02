from django.core.exceptions import ValidationError
from pytest import raises

from potluck.games.validators import validate_len


def test_validate_len_one_input_error():
    with raises(ValidationError):
        validate_len([1])