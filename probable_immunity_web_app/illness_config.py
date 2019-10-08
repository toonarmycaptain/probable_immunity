"""
Illness configuration

Register illnesses with application, encapsulate forms/functions associated
with each illness, and serve a nice API illnesses.illness.xyz.

"""


class Illnesses:
    """
    Container for illness objects of configured illnesses.
    ...

    Allows for iterating over the illness objects, a list of names etc.

    Illness objects are passed as a list to constructor.
    This list is set in the loaded config file.

    """

    def __init__(self, illness_list):
        self._illnesses_list = []

        # Add illness objects
        for illness in illness_list:
            setattr(self, illness.name, illness)
            # Register illness
            self._illnesses_list.append(illness)

    def __iter__(self):
        return iter(self._illnesses_list)

    @property
    def names(self):
        return [illness.name for illness in self._illnesses_list]
