import pytest

from illnesses.measles import (conferred_immunity,
                               immunity,
                               shots_under_6_immunity,
                               )


class TestImmunity:
    @pytest.mark.parametrize('args, returned_dict',
                             [  # pre 1957 birth year, no shots supplied
                                 ((1900,), {'probability_of_measles_immunity': conferred_immunity,
                                            'content_templates': ['pre_1957_message']}),
                                 ((1956,), {'probability_of_measles_immunity': conferred_immunity,
                                            'content_templates': ['pre_1957_message']}),
                                 ((1956, None), {'probability_of_measles_immunity': conferred_immunity,
                                                 'content_templates': ['pre_1957_message']}),
                                 # pre-1957 birth year, number of shots 0 -> >2
                                 ((1900, 0), {'probability_of_measles_immunity': conferred_immunity,
                                              'content_templates': ['pre_1957_message']}),
                                 ((1956, 1), {'probability_of_measles_immunity': conferred_immunity,
                                              'content_templates': ['pre_1957_message']}),
                                 ((1900, 2), {'probability_of_measles_immunity': conferred_immunity,
                                              'content_templates': ['pre_1957_message']}),
                                 ((1956, 3), {'probability_of_measles_immunity': conferred_immunity,
                                              'content_templates': ['pre_1957_message']}),
                             ])
    def test_immunity_pre_1957(self, args, returned_dict):
        assert immunity(*args) == returned_dict

    @pytest.mark.parametrize('args, returned_dict',
                             [  # 0 shots
                                 ((1957,),
                                  {'probability_of_measles_immunity': shots_under_6_immunity[0],
                                   'content_templates': ['no_immunisations']}),
                                 ((1958,),
                                  {'probability_of_measles_immunity': shots_under_6_immunity[0],
                                   'content_templates': ['no_immunisations']}),
                                 ((2011,),
                                  {'probability_of_measles_immunity': shots_under_6_immunity[0],
                                   'content_templates': ['no_immunisations']}),
                                 ((1957, 0),
                                  {'probability_of_measles_immunity': shots_under_6_immunity[0],
                                   'content_templates': ['no_immunisations']}),
                                 ((1958, 0),
                                  {'probability_of_measles_immunity': shots_under_6_immunity[0],
                                   'content_templates': ['no_immunisations']}),
                                 ((2011, 0),
                                  {'probability_of_measles_immunity': shots_under_6_immunity[0],
                                   'content_templates': ['no_immunisations']}),
                                 # 1 shot
                                 ((1957, 1), {'probability_of_measles_immunity': shots_under_6_immunity[1],
                                              'content_templates': ['has_immunisations']}),
                                 ((1958, 1), {'probability_of_measles_immunity': shots_under_6_immunity[1],
                                              'content_templates': ['has_immunisations']}),
                                 ((2011, 1), {'probability_of_measles_immunity': shots_under_6_immunity[1],
                                              'content_templates': ['has_immunisations']}),
                                 # 2 shots
                                 ((1957, 2), {'probability_of_measles_immunity': shots_under_6_immunity[2],
                                              'content_templates': ['has_immunisations']}),
                                 ((1958, 2), {'probability_of_measles_immunity': shots_under_6_immunity[2],
                                              'content_templates': ['has_immunisations']}),
                                 ((2011, 2), {'probability_of_measles_immunity': shots_under_6_immunity[2],
                                              'content_templates': ['has_immunisations']}),
                                 # >2 shots
                                 ((1957, 3), {'probability_of_measles_immunity': shots_under_6_immunity[2],
                                              'content_templates': ['has_immunisations',
                                                                    'greater_than_two_shots_before_age_six_message']}),
                                 ((1958, 7), {'probability_of_measles_immunity': shots_under_6_immunity[2],
                                              'content_templates': ['has_immunisations',
                                                                    'greater_than_two_shots_before_age_six_message']}),
                                 ((2011, 12), {'probability_of_measles_immunity': shots_under_6_immunity[2],
                                               'content_templates': ['has_immunisations',
                                                                     'greater_than_two_shots_before_age_six_message']}),
                             ])
    def test_immunity_post_1957(self, args, returned_dict):
        assert immunity(*args) == returned_dict

    @pytest.mark.parametrize('args',
                             [  # No on_time_measles_vaccinations arg
                                 {'birth_year': 'a', },  # String birth_year.
                                 {'birth_year': 1957.6, },  # String obirth_year.
                                 {'birth_year': 'c', },  # String for all values.
                                 {'birth_year': -1989, },  # Negative birth year
                                 {'birth_year': 2232, },  # Too high birth year.
                                 {'birth_year': 19894, },  # Too long/high birth year.
                                 {'birth_year': 198, },  # Too low/short birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980}, marks=pytest.mark.xfail),
                                 # 0 shots
                                 {'birth_year': 'a', 'on_time_measles_vaccinations': 0, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_measles_vaccinations': 0, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_measles_vaccinations': 0, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_measles_vaccinations': 0, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_measles_vaccinations': 0, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_measles_vaccinations': 0, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_measles_vaccinations': 0, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 0, },
                                              marks=pytest.mark.xfail),

                                 # 1 shot
                                 {'birth_year': 'a', 'on_time_measles_vaccinations': 1, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_measles_vaccinations': 1, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_measles_vaccinations': 1, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_measles_vaccinations': 1, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_measles_vaccinations': 1, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_measles_vaccinations': 1, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_measles_vaccinations': 1, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 1, },
                                              marks=pytest.mark.xfail),
                                 # 2 shots
                                 {'birth_year': 'a', 'on_time_measles_vaccinations': 2, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_measles_vaccinations': 2, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_measles_vaccinations': 2, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_measles_vaccinations': 2, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_measles_vaccinations': 2, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_measles_vaccinations': 2, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_measles_vaccinations': 2, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 2, },
                                              marks=pytest.mark.xfail),
                                 # > 2 shots
                                 {'birth_year': 'a', 'on_time_measles_vaccinations': 3, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_measles_vaccinations': 7, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_measles_vaccinations': 12, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_measles_vaccinations': 3, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_measles_vaccinations': 7, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_measles_vaccinations': 12, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_measles_vaccinations': 3, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 3, },
                                              marks=pytest.mark.xfail),
                             ])
    def test_immunity_birth_year_raising_error(self, args):
        with pytest.raises(ValueError):
            immunity(**args)

    @pytest.mark.parametrize('args',
                             [
                                 # 0 shots
                                 {'birth_year': 1980, 'on_time_measles_vaccinations': -1, },  # Negative shots.
                                 {'birth_year': 1980, 'on_time_measles_vaccinations': 1.5, },  # Float shots.
                                 {'birth_year': 1980, 'on_time_measles_vaccinations': 'two', },  # String shots.
                                 # Ensure good session data does not raise error.
                                 # Empty string
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': '', },
                                              marks=pytest.mark.xfail),
                                 # None
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': None, },
                                              marks=pytest.mark.xfail),
                                 # False
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': False, },
                                              marks=pytest.mark.xfail),
                                 # Ints
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 1, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 2, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 3, },
                                              marks=pytest.mark.xfail),  # Float > 2
                                 # Floats
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 0.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 1.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 2.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 3.0, },
                                              marks=pytest.mark.xfail),  # Float > 2
                             ])
    def test_immunity_on_time_measles_vaccinations_raising_value_error(self, args):
        with pytest.raises(ValueError):
            immunity(**args)
