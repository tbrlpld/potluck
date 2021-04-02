from django.core.exceptions import ValidationError
from pytest import raises

from potluck.games.validators import validate_len


def test_validate_len_empty_list_error():
    with raises(ValidationError):
        validate_len([])


def test_validate_len_one_input_error():
    with raises(ValidationError):
        validate_len([1])


def test_validate_len_three_inputs_error():
    with raises(ValidationError):
        validate_len([1, 2, 3])


def test_validate_len_two_inputs_success():
    assert validate_len([1, 2]) is None
