from typing import Callable, Type

from flask_wtf import FlaskForm


class Illness:
    """
    Class to contain a class' data (ie student objects) and related methods.
    ...

    Attributes
    ----------
    name : str
        Illness' name

    form : FlaskForm
        Flask-WTF WTForm object, renders form in HTML and validates data.

    Methods
    -------
    immunity
        Wraps illness' immunity function.

    extract_data(form)
            Wraps function extracting data from form returning dict to store
            in session.

    """

    def __init__(self, name: str,
                 immunity: Callable,
                 wt_form: Type[FlaskForm],
                 form_data_extractor: Callable,
                 ):
        """
        :param name: str
        :param immunity: function
        :param wt_form: FlaskForm, Flask-WTF WTForm object
        :param form_data_extractor: function
        """
        self.name = name
        self.form = wt_form
        self._immunity = immunity
        self._form_data_extractor = form_data_extractor

    def immunity(self, *args, **kwargs) -> dict:
        """
        Wraps illness' immunity function, typically returning a dict with
        probability of being immune if exposed to illness, and data indicating
        templates/categories for front end to display.

        :param args:
        :param kwargs:
        :return:
        """
        return self._immunity(*args, **kwargs)

    def extract_data(self, form: FlaskForm) -> dict:
        """
        Wraps illness' extract_data function, taking data from form, turning
        into a dict for storing in session.

        :param form: FlaskForm, Flask-WTF WTForm object
        :return: dict
        """
        return self._form_data_extractor(form)
