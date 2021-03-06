from math import isclose

import pytest

import illnesses

from illnesses.mumps import (current_year,
                             conferred_immunity,
                             immunity,
                             natural_immunity,
                             one_dose_immunity,
                             one_dose_init_immunity,
                             two_dose_immunity,
                             two_dose_init_immunity,
                             )


@pytest.mark.parametrize(
    'birth_year, probability_of_immunity',
    [  # 6 or under
        (current_year - 0, one_dose_init_immunity),
        (current_year - 5, one_dose_init_immunity),
        (current_year - 6, one_dose_init_immunity),
        # Over 6 years old
        (current_year - 7, 0.5),
        (2011, 0.5),
        (1985, 0.5),
        (1958, 0.5),
        (1957, 0.5),
        # Pre 1957
        (1956, 0.5),
        (1950, 0.5),

    ])
def test_one_dose_immunity(birth_year, probability_of_immunity):
    assert isclose(one_dose_immunity(birth_year), probability_of_immunity,
                   abs_tol=0.499)


@pytest.mark.parametrize('birth_year, probability_of_immunity',
                         [  # 6 or under
                             (current_year - 0, two_dose_init_immunity),
                             (current_year - 5, two_dose_init_immunity),
                             (current_year - 6, two_dose_init_immunity),
                             # Over 6 years old
                             (current_year - 7, 0.5),
                             (2011, 0.5),
                             (1985, 0.5),
                             (1958, 0.5),
                             (1957, 0.5),
                             # Pre 1957
                             (1956, 0.5),
                             (1950, 0.5),

                         ])
def test_two_dose_immunity(birth_year, probability_of_immunity):
    assert isclose(two_dose_immunity(birth_year), probability_of_immunity,
                   abs_tol=0.499)


class TestImmunity:
    @pytest.mark.parametrize(
        'args, kwargs, returned_dict',
        [  # Pre-1957 birth year, no shots supplied
            ((1900,), {'mumps_illness': False},
             {'probability_of_mumps_immunity': conferred_immunity,
              'content_templates': ['pre_1957_message']}),
            ((1956,), {'mumps_illness': False},
             {'probability_of_mumps_immunity': conferred_immunity,
              'content_templates': ['pre_1957_message']}),
            ((1956, None, False), {}, {'probability_of_mumps_immunity': conferred_immunity,
                                       'content_templates': ['pre_1957_message']}),
            # Pre-1957 birth year, number of shots 0 -> >2
            ((1900, 0, False), {}, {'probability_of_mumps_immunity': conferred_immunity,
                                    'content_templates': ['pre_1957_message']}),
            ((1956, 1, False), {}, {'probability_of_mumps_immunity': conferred_immunity,
                                    'content_templates': ['pre_1957_message']}),
            ((1900, 2, False), {}, {'probability_of_mumps_immunity': conferred_immunity,
                                    'content_templates': ['pre_1957_message']}),
            ((1956, 3, False), {}, {'probability_of_mumps_immunity': conferred_immunity,
                                    'content_templates': ['pre_1957_message']}),
            pytest.param((1980, 0, False), {},
                         {'probability_of_mumps_immunity': conferred_immunity,
                          'content_templates': ['pre_1957_message']},
                         marks=pytest.mark.xfail),
            # All kwargs
            # Pre-1957 birth year, no shots supplied
            ({}, {'birth_year': 1900, }, {'probability_of_mumps_immunity': conferred_immunity,
                                          'content_templates': ['pre_1957_message']}),
            ({}, {'birth_year': 1956, }, {'probability_of_mumps_immunity': conferred_immunity,
                                          'content_templates': ['pre_1957_message']}),
            ({}, {'birth_year': 1956,
                  'on_time_mumps_vaccinations': None, }, {'probability_of_mumps_immunity': conferred_immunity,
                                                          'content_templates': ['pre_1957_message']}),
            # Pre-1957 birth year, number of shots 0 -> >2
            ({}, {'birth_year': 1900,
                  'on_time_mumps_vaccinations': 0, }, {'probability_of_mumps_immunity': conferred_immunity,
                                                       'content_templates': ['pre_1957_message']}),
            ({}, {'birth_year': 1956,
                  'on_time_mumps_vaccinations': 1, }, {'probability_of_mumps_immunity': conferred_immunity,
                                                       'content_templates': ['pre_1957_message']}),
            ({}, {'birth_year': 1900,
                  'on_time_mumps_vaccinations': 2, }, {'probability_of_mumps_immunity': conferred_immunity,
                                                       'content_templates': ['pre_1957_message']}),
            ({}, {'birth_year': 1956,
                  'on_time_mumps_vaccinations': 3, }, {'probability_of_mumps_immunity': conferred_immunity,
                                                       'content_templates': ['pre_1957_message']}),
            # Pre-1957 birth year, no shots supplied, previous illness mumps
            ({}, {'birth_year': 1900,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            ({}, {'birth_year': 1956,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            ({}, {'birth_year': 1900,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            ({}, {'birth_year': 1956,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            # Pre-1957 birth year, number of shots 0 -> >2, previous illness mumps
            ({}, {'birth_year': 1900,
                  'on_time_mumps_vaccinations': 0,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            ({}, {'birth_year': 1956,
                  'on_time_mumps_vaccinations': 1,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            ({}, {'birth_year': 1900,
                  'on_time_mumps_vaccinations': 2,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),
            ({}, {'birth_year': 1956,
                  'on_time_mumps_vaccinations': 3,
                  'mumps_illness': True, }, {'probability_of_mumps_immunity': conferred_immunity,
                                             'content_templates': ['previous_illness']}),

        ])
    def test_immunity_pre_1957(self, args, kwargs, returned_dict):
        assert immunity(*args, **kwargs) == returned_dict

    @pytest.mark.parametrize('args, kwargs, returned_dict',
                             [  # Pre-1957 birth year, no shots supplied
                                 ((1900,), {'mumps_illness': True},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956,), {'mumps_illness': True},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956, None, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # Pre-1957 birth year, number of shots 0 -> >2
                                 ((1900, 0, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956, 1, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1900, 2, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1956, 3, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # 0 shots
                                 ((1957,), {'mumps_illness': True},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958,), {'mumps_illness': True},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011,), {'mumps_illness': True},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1957, 0, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 0, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 0, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # 1 shot
                                 ((1957, 1, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 1, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 1, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # 2 shots
                                 ((1957, 2, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 2, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 2, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 # >2 shots
                                 ((1957, 3, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((1958, 7, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                                 ((2011, 12, True), {},
                                  {'probability_of_mumps_immunity': conferred_immunity,
                                   'content_templates': ['previous_illness']}),
                             ])
    def test_immunity_had_mumps(self, args, kwargs, returned_dict):
        assert immunity(*args, **kwargs) == returned_dict

    @pytest.mark.parametrize(
        'args, kwargs, returned_dict',
        [  # 0 shots
            ((1957,), {}, {'probability_of_mumps_immunity': natural_immunity,
                           'content_templates': ['no_immunisations', ]}),
            ((1958,), {}, {'probability_of_mumps_immunity': natural_immunity,
                           'content_templates': ['no_immunisations', ]}),
            ((2011,), {}, {'probability_of_mumps_immunity': natural_immunity,
                           'content_templates': ['no_immunisations', ]}),
            ((1957, 0), {}, {'probability_of_mumps_immunity': natural_immunity,
                             'content_templates': ['no_immunisations', ]}),
            ((1958, 0), {}, {'probability_of_mumps_immunity': natural_immunity,
                             'content_templates': ['no_immunisations', ]}),
            ((2011, 0), {}, {'probability_of_mumps_immunity': natural_immunity,
                             'content_templates': ['no_immunisations', ]}),
            # 1 shot, 'waning_warning'
            ((1957, 1), {}, {'probability_of_mumps_immunity': 'one',
                             'content_templates': ['has_immunisations', 'waning_warning', ]}),
            ((1958, 1), {}, {'probability_of_mumps_immunity': 'one',
                             'content_templates': ['has_immunisations', 'waning_warning', ]}),
            ((2011, 1), {}, {'probability_of_mumps_immunity': 'one',
                             'content_templates': ['has_immunisations', 'waning_warning', ]}),
            # 2 shots, 'waning_warning'
            ((1957, 2), {}, {'probability_of_mumps_immunity': 'two',
                             'content_templates': ['has_immunisations', 'waning_warning', ]}),
            ((1958, 2), {}, {'probability_of_mumps_immunity': 'two',
                             'content_templates': ['has_immunisations', 'waning_warning', ]}),
            ((2011, 2), {}, {'probability_of_mumps_immunity': 'two',
                             'content_templates': ['has_immunisations', 'waning_warning', ]}),
            # >2 shots, 'waning_warning'
            ((1957, 3), {}, {'probability_of_mumps_immunity': 'two', 'content_templates': [
                'has_immunisations', 'waning_warning',
                'greater_than_two_shots_before_age_six_message', ]}),
            ((1958, 7), {}, {'probability_of_mumps_immunity': 'two', 'content_templates': [
                'has_immunisations', 'waning_warning',
                'greater_than_two_shots_before_age_six_message', ]}),
            ((2011, 12), {}, {'probability_of_mumps_immunity': 'two',
                              'content_templates': ['has_immunisations', 'waning_warning',
                                                    'greater_than_two_shots_before_age_six_message', ]}),
            # All kwargs
            ({}, {'birth_year': 1957, }, {'probability_of_mumps_immunity': natural_immunity,
                                          'content_templates': ['no_immunisations'],
                                          }),
            ({}, {'birth_year': 1958, }, {'probability_of_mumps_immunity': natural_immunity,
                                          'content_templates': ['no_immunisations'],
                                          }),
            ({}, {'birth_year': 2011, }, {'probability_of_mumps_immunity': natural_immunity,
                                          'content_templates': ['no_immunisations'],
                                          }),
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 0}, {'probability_of_mumps_immunity': natural_immunity,
                                                     'content_templates': ['no_immunisations'],
                                                     }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 0}, {'probability_of_mumps_immunity': natural_immunity,
                                                     'content_templates': ['no_immunisations'],
                                                     }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 0}, {'probability_of_mumps_immunity': natural_immunity,
                                                     'content_templates': ['no_immunisations'],
                                                     }),
            # 1 shot
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 1}, {'probability_of_mumps_immunity': 'one',
                                                     'content_templates': ['has_immunisations',
                                                                           'waning_warning'],
                                                     }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 1}, {'probability_of_mumps_immunity': 'one',
                                                     'content_templates': ['has_immunisations',
                                                                           'waning_warning'],
                                                     }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 1}, {'probability_of_mumps_immunity': 'one',
                                                     'content_templates': ['has_immunisations',
                                                                           'waning_warning'],
                                                     }),
            # 2 shots
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 2}, {'probability_of_mumps_immunity': 'two',
                                                     'content_templates': ['has_immunisations',
                                                                           'waning_warning'],
                                                     }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 2}, {'probability_of_mumps_immunity': 'two',
                                                     'content_templates': ['has_immunisations',
                                                                           'waning_warning'],
                                                     }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 2}, {'probability_of_mumps_immunity': 'two',
                                                     'content_templates': ['has_immunisations',
                                                                           'waning_warning'],
                                                     }),
            # >2 shots
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 3}, {'probability_of_mumps_immunity': 'two',
                                                     'content_templates': [
                                                         'has_immunisations',
                                                         'waning_warning',
                                                         'greater_than_two_shots_before_age_six_message'],
                                                     }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 7}, {'probability_of_mumps_immunity': 'two',
                                                     'content_templates': [
                                                         'has_immunisations',
                                                         'waning_warning',
                                                         'greater_than_two_shots_before_age_six_message'],
                                                     }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 12}, {'probability_of_mumps_immunity': 'two',
                                                      'content_templates': [
                                                          'has_immunisations',
                                                          'waning_warning',
                                                          'greater_than_two_shots_before_age_six_message'],
                                                      }),
            # Previous mumps illness
            # 0 shots
            ({}, {'birth_year': 1957,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 1958,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 2011,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 0,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 0,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 0,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            # 1 shot
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 1,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 1,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 1,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            # 2 shots
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 2,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 2,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 2,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            # >2 shots
            ({}, {'birth_year': 1957,
                  'on_time_mumps_vaccinations': 3,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 1958,
                  'on_time_mumps_vaccinations': 7,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
            ({}, {'birth_year': 2011,
                  'on_time_mumps_vaccinations': 12,
                  'mumps_illness': True}, {'probability_of_mumps_immunity': conferred_immunity,
                                           'content_templates': ['previous_illness'],
                                           }),
        ])
    def test_immunity_post_1957(self, args, kwargs, returned_dict,
                                monkeypatch):
        """
        Mock regression algorithm implementations.
        NB Implementation changes combined with long floats would make unnecessarily fragile test.
        """

        def mocked_one_dose_immunity(*ignored_args):
            return 'one'

        def mocked_two_dose_immunity(*ignored_args):
            return 'two'

        monkeypatch.setattr(illnesses.mumps, 'one_dose_immunity', mocked_one_dose_immunity)
        monkeypatch.setattr(illnesses.mumps, 'two_dose_immunity', mocked_two_dose_immunity)

        assert immunity(*args, **kwargs) == returned_dict

    @pytest.mark.parametrize('args',
                             [  # No on_time_mumps_vaccinations arg
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
                                 {'birth_year': 'a', 'on_time_mumps_vaccinations': 0, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_mumps_vaccinations': 0, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_mumps_vaccinations': 0, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_mumps_vaccinations': 0, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_mumps_vaccinations': 0, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_mumps_vaccinations': 0, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_mumps_vaccinations': 0, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 0, },
                                              marks=pytest.mark.xfail),

                                 # 1 shot
                                 {'birth_year': 'a', 'on_time_mumps_vaccinations': 1, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_mumps_vaccinations': 1, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_mumps_vaccinations': 1, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_mumps_vaccinations': 1, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_mumps_vaccinations': 1, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_mumps_vaccinations': 1, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_mumps_vaccinations': 1, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 1, },
                                              marks=pytest.mark.xfail),
                                 # 2 shots
                                 {'birth_year': 'a', 'on_time_mumps_vaccinations': 2, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_mumps_vaccinations': 2, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_mumps_vaccinations': 2, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_mumps_vaccinations': 2, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_mumps_vaccinations': 2, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_mumps_vaccinations': 2, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_mumps_vaccinations': 2, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 2, },
                                              marks=pytest.mark.xfail),
                                 # > 2 shots
                                 {'birth_year': 'a', 'on_time_mumps_vaccinations': 3, },  # String birth_year.
                                 {'birth_year': 1957.6, 'on_time_mumps_vaccinations': 7, },  # Float birth_year.
                                 {'birth_year': 'c', 'on_time_mumps_vaccinations': 12, },  # String for all values.
                                 {'birth_year': -1989, 'on_time_mumps_vaccinations': 3, },  # Negative birth year
                                 {'birth_year': 2232, 'on_time_mumps_vaccinations': 7, },  # Too high birth year.
                                 {'birth_year': 19894, 'on_time_mumps_vaccinations': 12, },  # Too long birth year.
                                 {'birth_year': 198, 'on_time_mumps_vaccinations': 3, },  # Too low birth year.
                                 # Ensure good session data does not raise error.
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 3, },
                                              marks=pytest.mark.xfail),
                             ])
    def test_immunity_birth_year_raising_error(self, args):
        with pytest.raises(ValueError):
            immunity(**args)

    @pytest.mark.parametrize('args',
                             [
                                 # 0 shots
                                 {'birth_year': 1980, 'on_time_mumps_vaccinations': -1, },  # Negative shots.
                                 {'birth_year': 1980, 'on_time_mumps_vaccinations': 1.5, },  # Float shots.
                                 {'birth_year': 1980, 'on_time_mumps_vaccinations': 'two', },  # String shots.
                                 # Ensure good session data does not raise error.
                                 # Empty string
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': '', },
                                              marks=pytest.mark.xfail),
                                 # None
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': None, },
                                              marks=pytest.mark.xfail),
                                 # False
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': False, },
                                              marks=pytest.mark.xfail),
                                 # Ints
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 1, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 2, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 3, },
                                              marks=pytest.mark.xfail),  # Float > 2
                                 # Floats
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 0.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 1.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 2.0, },
                                              marks=pytest.mark.xfail),
                                 pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 3.0, },
                                              marks=pytest.mark.xfail),  # Float > 2
                             ])
    def test_immunity_on_time_mumps_vaccinations_raising_value_error(self, args):
        with pytest.raises(ValueError):
            immunity(**args)
