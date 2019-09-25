"""
Illness configuration

Register illnesses with application, encapsulate forms/functions associated
with each illness, and serve a nice API illnesses.illness.xyz.

"""
from probable_immunity_web_app.illnesses import (Measles,
                                                 )


class Illnesses:
    """
    Container for illness objects of configured illnesses.
    ...

    Allows for iterating over the illness objects, a list of names etc.

    To configure an illness, must:
        import illness object,
        add illness as an attribute in __init__:
            self.illness_name = Illness_name_object
        add illness attr to _illnesses_list:
            self._illnesses_list = [self.illness_name,]
    Adding or removing from _illnesses_list with activate/deactivate in app.

    """
    def __init__(self):
        # Add illness objects
        self.measles = Measles

        # Register illnesses
        self._illnesses_list = [self.measles,
                                ]

    def __iter__(self):
        return iter(self._illnesses_list)

    @property
    def names(self):
        return [illness.name for illness in self._illnesses_list]


illnesses = Illnesses()
