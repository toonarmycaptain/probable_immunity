"""
CDC Presumptive evidence of immunity: https://www.cdc.gov/vaccines/pubs/surv-manual/chpt07-measles.html



"Birth before 1957 provides only presumptive evidence for measles, mumps, and
rubella. Before vaccines were available, nearly everyone was infected with
measles, mumps, and rubella viruses during childhood. The majority of people
born before 1957 are likely to have been infected naturally and therefore are
presumed to be protected against measles, mumps, and rubella. Healthcare
personnel born before 1957 without laboratory evidence of immunity or disease
should consider getting two doses of MMR vaccine." - https://www.cdc.gov/vaccines/vpd/mmr/public/index.html
"""
from typing import Dict

rec_shots_under_6 = 2

conferred_immunity = 1

messages = {'pre_1957_message': ("According to the CDC, you are likely immune to measles due to "
                                 "childhood exposure.\n\"Birth before 1957 provides only "
                                 "presumptive evidence for measles, mumps, and rubella. Before "
                                 "vaccines were available, nearly everyone was infected with "
                                 "measles, mumps, and rubella viruses during childhood. The "
                                 "majority of people born before 1957 are likely to have been "
                                 "infected naturally and therefore are presumed to be protected "
                                 "against measles, mumps, and rubella. Healthcare personnel born "
                                 "before 1957 without laboratory evidence of immunity or disease "
                                 "should consider getting two doses of MMR vaccine.\" "
                                 "- https://www.cdc.gov/vaccines/vpd/mmr/public/index.html"),
            'has_immunisations': ("This means you have a statistical probability of being immune "
                                  "to measles if you are exposed. The closer to 1.0, the more "
                                  "likely you are immune."),  # TODO make better message
            'greater_than_two_shots_before_age_six_message': ("Data not available for more than 2 "
                                                              "shots before age 6."),
            'no_immunisations': ("You are unlikely to have any immunity to measles, if you are "
                                 "exposed, you are very likely to be infected.")
            }

# shots before 6 years
shots_under_6_immunity = {
    1: 0.93,
    2: 0.97,
}


def immunity(birth_year=None, on_time_measles_vaccinations: int = None) -> Dict:
    """
    Takes year of birth, number of shots before age 6, and provides an
    estimated probability of being immune to measles if exposed.

    :param birth_year: int or None
    :param on_time_measles_vaccinations: int or None
    :return: Dict {'probability_of_measles_immunity': float, 'measles_message': str}
    """
    # Set defaults:
    probability, message = 0.0, messages['no_immunisations']
    if birth_year < 1957:
        probability, message = 1.0, messages['pre_1957_message']
    elif on_time_measles_vaccinations:
        if on_time_measles_vaccinations <= 2:
            probability, message = shots_under_6_immunity[on_time_measles_vaccinations], messages['has_immunisations']
        if on_time_measles_vaccinations > 2:
            probability, message = shots_under_6_immunity[2], messages['greater_than_two_shots_before_age_six_message']
    return {'probability_of_measles_immunity': probability, 'measles_message': message}

# need case where shots after age 6
