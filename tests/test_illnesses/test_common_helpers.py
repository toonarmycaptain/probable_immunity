"""Test common helpers and validators."""
import pytest

from illnesses.common_helpers import (current_year,
                                      validate_birth_year,
                                      )


@pytest.mark.parametrize(
    'test_birth_year, validated_birth_year',
    [(1882, 1882),
     (1985, 1985),
     (current_year, current_year),
     # Ensure bad data does raises error.
     pytest.param('two thousand', 2000, marks=pytest.mark.xfail),
     ])
def test_validate_birth_year(test_birth_year, validated_birth_year):
    assert validate_birth_year(test_birth_year) == validated_birth_year


@pytest.mark.parametrize(
    'test_birth_year',
    ['a',  # String birth_year.
     1957.6,  # String on_time_measles_vaccinations.
     'c',  # String for all values.
     -1989,  # Negative birth year
     2232,  # Too high birth year.
     19894,  # Too long/high birth year.
     198,  # Too low/short birth year.
     current_year + 1,  # Ensure future/too high value raises error.
     # Ensure good data does not raise error.
     pytest.param(1980, marks=pytest.mark.xfail),
     ])
def test_validate_birth_year_raising_error(test_birth_year):
    with pytest.raises(ValueError):
        validate_birth_year(test_birth_year)
