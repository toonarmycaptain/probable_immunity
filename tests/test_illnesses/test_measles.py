import pytest

from illnesses.measles import (immunity,
                               messages,
                               )


class TestImmunity:
    @pytest.mark.parametrize('args, returned_dict',
                             [  # pre 1957 birth year, no shots supplied
                                 ((1900,), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                                 ((1956,), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                                 ((1956, None), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                                 # pre-1957 birth year, number of shots 0 -> >2
                                 ((1900, 0), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                                 ((1956, 1), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                                 ((1900, 2), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                                 ((1956, 3), {'probability_of_measles_immunity': 1.0, 'measles_message': messages['pre_1957_message']}),
                             ])
    def test_immunity_pre_1957(self, args, returned_dict):
        assert immunity(*args) == returned_dict


    @pytest.mark.parametrize('args, returned_dict',
                             [  # 0 shots
                                 ((1957,), {'probability_of_measles_immunity': 0.0, 'measles_message': messages['no_immunisations']}),
                                 ((1958,), {'probability_of_measles_immunity': 0.0, 'measles_message': messages['no_immunisations']}),
                                 ((2011,), {'probability_of_measles_immunity': 0.0, 'measles_message': messages['no_immunisations']}),
                                 ((1957, 0), {'probability_of_measles_immunity': 0.0, 'measles_message': messages['no_immunisations']}),
                                 ((1958, 0), {'probability_of_measles_immunity': 0.0, 'measles_message': messages['no_immunisations']}),
                                 ((2011, 0), {'probability_of_measles_immunity': 0.0, 'measles_message': messages['no_immunisations']}),
                                 # 1 shot
                                 ((1957, 1), {'probability_of_measles_immunity': 0.93, 'measles_message': messages['has_immunisations']}),
                                 ((1958, 1), {'probability_of_measles_immunity': 0.93, 'measles_message': messages['has_immunisations']}),
                                 ((2011, 1), {'probability_of_measles_immunity': 0.93, 'measles_message': messages['has_immunisations']}),
                                 # 2 shots
                                 ((1957, 2), {'probability_of_measles_immunity': 0.97, 'measles_message': messages['has_immunisations']}),
                                 ((1958, 2), {'probability_of_measles_immunity': 0.97, 'measles_message': messages['has_immunisations']}),
                                 ((2011, 2), {'probability_of_measles_immunity': 0.97, 'measles_message': messages['has_immunisations']}),
                                 # >2 shots
                                 ((1957, 3), {'probability_of_measles_immunity': 0.97, 'measles_message': messages['greater_than_two_shots_before_age_six_message']}),
                                 ((1958, 7), {'probability_of_measles_immunity': 0.97, 'measles_message': messages['greater_than_two_shots_before_age_six_message']}),
                                 ((2011, 12), {'probability_of_measles_immunity': 0.97, 'measles_message': messages['greater_than_two_shots_before_age_six_message']}),
                             ])
    def test_immunity_post_1957(self, args, returned_dict):
        assert immunity(*args) == returned_dict

