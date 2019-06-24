import pytest

from illnesses.measles import (immunity,
                               messages,
                               )


class TestImmunity:
    @pytest.mark.parametrize('args, returned_tuple',
                             [  # pre 1957 birth year, no shots supplied
                                 ((1900,), (1.0, messages['pre_1957_message'])),
                                 ((1956,), (1.0, messages['pre_1957_message'])),
                                 ((1956, None), (1.0, messages['pre_1957_message'])),
                                 # pre-1957 birth year, number of shots 0 -> >2
                                 ((1900, 0), (1.0, messages['pre_1957_message'])),
                                 ((1956, 1), (1.0, messages['pre_1957_message'])),
                                 ((1900, 2), (1.0, messages['pre_1957_message'])),
                                 ((1956, 3), (1.0, messages['pre_1957_message'])),
                             ])
    def test_immunity_pre_1957(self, args, returned_tuple):
        assert immunity(*args) == returned_tuple

    @pytest.mark.parametrize('args, returned_tuple',
                             [  # 0 shots
                                 ((1957,), (0.0, messages['no_immunisations'])),
                                 ((1958,), (0.0, messages['no_immunisations'])),
                                 ((2011, None), (0.0, messages['no_immunisations'])),
                                 # 1 shot
                                 ((1957, 1), (0.93, messages['has_immunisations'])),
                                 ((1958, 1), (0.93, messages['has_immunisations'])),
                                 ((2011, 1), (0.93, messages['has_immunisations'])),
                                 # 2 shots
                                 ((1957, 2), (0.97, messages['has_immunisations'])),
                                 ((1958, 2), (0.97, messages['has_immunisations'])),
                                 ((2011, 2), (0.97, messages['has_immunisations'])),
                                 # >2 shots
                                 ((1957, 3), (0.97, messages['greater_than_two_shots_before_age_six_message'])),
                                 ((1958, 7), (0.97, messages['greater_than_two_shots_before_age_six_message'])),
                                 ((2011, 12), (0.97, messages['greater_than_two_shots_before_age_six_message'])),
                             ])
    def test_immunity_post_1957(self, args, returned_tuple):
        assert immunity(*args) == returned_tuple
