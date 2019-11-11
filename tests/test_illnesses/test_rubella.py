import pytest

from illnesses.rubella import (conferred_immunity,
                               immunity,
                               vaccinated_immunity,
                               unvaccinated_immunity,
                               )


class TestImmunity:
    @pytest.mark.parametrize('args, kwargs, returned_dict',
                             [  # Pre-1957 birth year, no shots supplied
                                 ((1900,), {'rubella_illness': False},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 ((1956,), {'rubella_illness': False},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 ((1956, None, False), {}, {'probability_of_rubella_immunity': conferred_immunity,
                                                            'content_templates': ['pre_1957_message']}),
                                 # Pre-1957 birth year, number of shots 0 -> >2
                                 ((1900, 0, False), {}, {'probability_of_rubella_immunity': conferred_immunity,
                                                         'content_templates': ['pre_1957_message']}),
                                 ((1956, 1, False), {}, {'probability_of_rubella_immunity': conferred_immunity,
                                                         'content_templates': ['pre_1957_message']}),
                                 ((1900, 2, False), {}, {'probability_of_rubella_immunity': conferred_immunity,
                                                         'content_templates': ['pre_1957_message']}),
                                 ((1956, 3, False), {}, {'probability_of_rubella_immunity': conferred_immunity,
                                                         'content_templates': ['pre_1957_message']}),
                                 pytest.param((1980, 0, False), {},
                                              {'probability_of_rubella_immunity': conferred_immunity,
                                               'content_templates': ['pre_1957_message']},
                                              marks=pytest.mark.xfail),
                                 # All kwargs
                                 # Pre-1957 birth year, no shots supplied
                                 ({}, {'birth_year': 1900, }, {'probability_of_rubella_immunity': conferred_immunity,
                                                               'content_templates': ['pre_1957_message']}),
                                 ({}, {'birth_year': 1956, }, {'probability_of_rubella_immunity': conferred_immunity,
                                                               'content_templates': ['pre_1957_message']}),
                                 ({}, {'birth_year': 1956,
                                       'on_time_rubella_vaccinations': None, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 # Pre-1957 birth year, number of shots 0 -> >2
                                 ({}, {'birth_year': 1900,
                                       'on_time_rubella_vaccinations': 0, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 ({}, {'birth_year': 1956,
                                       'on_time_rubella_vaccinations': 1, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 ({}, {'birth_year': 1900,
                                       'on_time_rubella_vaccinations': 2, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 ({}, {'birth_year': 1956,
                                       'on_time_rubella_vaccinations': 3, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['pre_1957_message']}),
                                 # Pre-1957 birth year, no shots supplied, previous illness rubella
                                 ({}, {'birth_year': 1900,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ({}, {'birth_year': 1956,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ({}, {'birth_year': 1900,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ({}, {'birth_year': 1956,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # Pre-1957 birth year, number of shots 0 -> >2, previous illness rubella
                                 ({}, {'birth_year': 1900,
                                       'on_time_rubella_vaccinations': 0,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ({}, {'birth_year': 1956,
                                       'on_time_rubella_vaccinations': 1,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ({}, {'birth_year': 1900,
                                       'on_time_rubella_vaccinations': 2,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ({}, {'birth_year': 1956,
                                       'on_time_rubella_vaccinations': 3,
                                       'rubella_illness': True, },
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),

                             ])
    def test_immunity_pre_1957(self, args, kwargs, returned_dict):
        assert immunity(*args, **kwargs) == returned_dict

    @pytest.mark.parametrize('args, kwargs, returned_dict',
                             [  # Pre-1957 birth year, no shots supplied
                                 ((1900,), {'rubella_illness': True},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956,), {'rubella_illness': True},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956, None, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # Pre-1957 birth year, number of shots 0 -> >2
                                 ((1900, 0, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956, 1, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1900, 2, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956, 3, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # 0 shots
                                 ((1957,), {'rubella_illness': True},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958,), {'rubella_illness': True},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011,), {'rubella_illness': True},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1957, 0, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 0, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 0, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # 1 shot
                                 ((1957, 1, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 1, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 1, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # 2 shots
                                 ((1957, 2, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 2, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 2, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # >2 shots
                                 ((1957, 3, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 7, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 12, True), {},
                                  {'probability_of_rubella_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                             ])
    def test_immunity_had_rubella(self, args, kwargs, returned_dict):
        assert immunity(*args, **kwargs) == returned_dict

    @pytest.mark.parametrize('args, returned_dict',
                             [  # 0 shots
                                 ((1957,),
                                  {'probability_of_rubella_immunity': unvaccinated_immunity,
                                   'content_templates': ['no_immunisations']}),
                                 ((1958,),
                                  {'probability_of_rubella_immunity': unvaccinated_immunity,
                                   'content_templates': ['no_immunisations']}),
                                 ((2011,),
                                  {'probability_of_rubella_immunity': unvaccinated_immunity,
                                   'content_templates': ['no_immunisations']}),
                                 ((1957, 0),
                                  {'probability_of_rubella_immunity': unvaccinated_immunity,
                                   'content_templates': ['no_immunisations']}),
                                 ((1958, 0),
                                  {'probability_of_rubella_immunity': unvaccinated_immunity,
                                   'content_templates': ['no_immunisations']}),
                                 ((2011, 0),
                                  {'probability_of_rubella_immunity': unvaccinated_immunity,
                                   'content_templates': ['no_immunisations']}),
                                 # 1 shot
                                 ((1957, 1), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 ((1958, 1), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 ((2011, 1), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 # 2 shots
                                 ((1957, 2), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 ((1958, 2), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 ((2011, 2), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 # >2 shots
                                 ((1957, 3), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 ((1958, 7), {'probability_of_rubella_immunity': vaccinated_immunity,
                                              'content_templates': ['has_immunisations']}),
                                 ((2011, 12), {'probability_of_rubella_immunity': vaccinated_immunity,
                                               'content_templates': ['has_immunisations']}),
                             ])
    def test_immunity_post_1957(self, args, returned_dict):
        assert immunity(*args) == returned_dict

    @pytest.mark.parametrize('args',
                             [  # No on_time_rubella_vaccinations arg
                                 {'birth_year': 'a', },  # String birth_year.
                                 {'birth_year': 1957.6, },  # String birth_year.
                                 {'birth_year': 'c', },  # String for all values.
                                 {'birth_year': -1989, },  # Negative birth year
                                 {'birth_year': 2232, },  # Too high birth year.
                                 {'birth_year': 19894, },  # Too long/high birth year.
                                 {'birth_year': 198, },  # Too low/short birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980}, marks=pytest.mark.xfail),
                                 # 0 shots
                                 {'birth_year': 'a', 'on_time_rubella_vaccinations': 0, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_rubella_vaccinations': 0, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_rubella_vaccinations': 0, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_rubella_vaccinations': 0, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_rubella_vaccinations': 0, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_rubella_vaccinations': 0, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_rubella_vaccinations': 0, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 0, },
                                              marks=pytest.mark.xfail),

                                 # 1 shot
                                 {'birth_year': 'a', 'on_time_rubella_vaccinations': 1, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_rubella_vaccinations': 1, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_rubella_vaccinations': 1, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_rubella_vaccinations': 1, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_rubella_vaccinations': 1, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_rubella_vaccinations': 1, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_rubella_vaccinations': 1, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 1, },
                                              marks=pytest.mark.xfail),
                                 # 2 shots
                                 {'birth_year': 'a', 'on_time_rubella_vaccinations': 2, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_rubella_vaccinations': 2, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_rubella_vaccinations': 2, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_rubella_vaccinations': 2, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_rubella_vaccinations': 2, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_rubella_vaccinations': 2, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_rubella_vaccinations': 2, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 2, },
                                              marks=pytest.mark.xfail),
                                 # > 2 shots
                                 {'birth_year': 'a', 'on_time_rubella_vaccinations': 3, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_rubella_vaccinations': 7, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_rubella_vaccinations': 12, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_rubella_vaccinations': 3, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_rubella_vaccinations': 7, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_rubella_vaccinations': 12, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_rubella_vaccinations': 3, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 3, },
                                              marks=pytest.mark.xfail),
                             ])
    def test_immunity_birth_year_raising_error(self, args):
        with pytest.raises(ValueError):
            immunity(**args)

    @pytest.mark.parametrize('args',
                             [
                                 # 0 shots
                                 {'birth_year': 1980, 'on_time_rubella_vaccinations': -1, },  # Negative shots.
                                 {'birth_year': 1980, 'on_time_rubella_vaccinations': 1.5, },  # Float shots.
                                 {'birth_year': 1980, 'on_time_rubella_vaccinations': 'two', },  # String shots.
                                 # Ensure good session data does not raise error.
                                 # Empty string
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': '', },
                                              marks=pytest.mark.xfail),
                                 # None
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': None, },
                                              marks=pytest.mark.xfail),
                                 # False
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': False, },
                                              marks=pytest.mark.xfail),
                                 # Ints
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 1, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 2, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 3, },
                                              marks=pytest.mark.xfail),  # Float > 2
                                 # Floats
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 0.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 1.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 2.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_rubella_vaccinations': 3.0, },
                                              marks=pytest.mark.xfail),  # Float > 2
                             ])
    def test_immunity_on_time_rubella_vaccinations_raising_value_error(self, args):
        with pytest.raises(ValueError):
            immunity(**args)
