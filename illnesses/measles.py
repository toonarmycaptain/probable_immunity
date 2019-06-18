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
from typing import Optional, Tuple

rec_shots_under_6 = 2

conferred_immunity = 1

pre_1957_message = ("Birth before 1957 provides only presumptive evidence for measles, mumps, and "
                    "rubella. Before vaccines were available, nearly everyone was infected with "
                    "measles, mumps, and rubella viruses during childhood. The majority of people "
                    "born before 1957 are likely to have been infected naturally and therefore are "
                    "presumed to be protected against measles, mumps, and rubella. Healthcare "
                    "personnel born before 1957 without laboratory evidence of immunity or disease "
                    "should consider getting two doses of MMR vaccine. - "
                    "https://www.cdc.gov/vaccines/vpd/mmr/public/index.html")

greater_than_two_shots_before_age_six_message = "Data not available for more than 2 shots before age 6."

# shots before 6 years
shots_under_6_immunity = {
    1: 0.93,
    2: 0.97,
}


def immunity(birth_year=None, shots_before_age_six: int = None) -> Tuple[float, Optional[str]]:
    if birth_year < 1957:
        return 1.0, pre_1957_message
    if shots_before_age_six:
        if shots_before_age_six <= 2:
            return shots_under_6_immunity[shots_before_age_six], None  # No message
        if shots_before_age_six > 2:
            return shots_under_6_immunity[2], greater_than_two_shots_before_age_six_message
    return 0.0, None

# need case where shots after age 6
