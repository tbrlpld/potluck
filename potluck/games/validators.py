from django.core import exceptions


def validate_len(value):
    if len(value) != 2:
        raise exceptions.ValidationError("Only two values are allowed")
