from typing import Optional, Type

from flask_wtf import FlaskForm
from wtforms import ValidationError


class Year(object):
    """
    Custom validator for year integer.
    ...

    Attributes:
    ----------
    min_year : int
        Minimum year.
    max_year : int
        Maximum year.
    digits : int
        Length of value required. eg 27 = 2, 20293 = 5. Default: 4
    message : str
        Error message on validation failure.


    """

    def __init__(self, min_year: Optional[int] = None,
                 max_year: Optional[int] = None,
                 digits: int = 4,
                 message=None,
                 ):
        """
        :param min_year: int, the minimum year
        :param max_year: int, the maximum year.
        :param digits: int, length of value required, defaults to 4.
        :param message: str, error message on validation failure.
        """
        self.min = min_year
        self.max = max_year
        self.num_digits = digits
        if not message:
            message = f'Field must be a {digits} digit year with a value between {min_year} and  {max_year}.'
        self.message = message


    def __call__(self, form: Type[FlaskForm], field):
        """
        :param form: Flask-WTF WTForm object
        :param field: The field to be validated.
        :return: None
        :raises: ValidationError
        """
        # Cast to int if value exists and is string, otherwise assign 0, which will fail num_digits !=0.
        value = field.data and int(field.data) or 0
        if ((self.min is not None and value < self.min)
                or (self.max is not None and value > self.max)
                or (self.num_digits is not None and self.num_digits != len(str(value)))
                or (not isinstance(value, int))):
            raise ValidationError(self.message)
