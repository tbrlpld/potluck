from django import template

register = template.Library()


@register.filter
def insert(value, args):
    """
    Insert a string into the value.

    This filter inserts a given string into the value at a given index.

    The index and the string need to be passed as one string as comma separated
    arguments. E.g. to insert the string "example" at the second index (1) use like
    this:

    ```django+html
    {{ value|insert:'0, example' }}
    ```

    """
    index, insert_string = args.split(",")
    index = int(index)
    return value[:index] + insert_string + value[index:]
