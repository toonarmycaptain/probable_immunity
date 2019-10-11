import datetime

from typing import Union

current_year: int = datetime.date.today().year  # Returns 4 digit year.


def validate_birth_year(birth_year: int) -> Union[int, ValueError]:
    """
    Validate birth_year supplied to illness functions.

    Accepts a four digit positive integer (eg 1000+) up to the current year,
    inferring equivalent floats eg 1980.0 accepted as 1980.

    # Future possibility to also accept a datetime object, str and return valid
    integer for illness function consumption.

    :param birth_year: int
    :raises ValueError: Where supplied argument is not valid.
    :return: int
    """
    if not isinstance(birth_year, int) or not 999 < birth_year <= current_year:
        raise ValueError(f'Birth year must be a 4 digit integer less than {current_year}.')
    return birth_year
