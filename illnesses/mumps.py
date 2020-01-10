from math import e
from typing import (Dict,
                    List,
                    Union)

from .common_helpers import (current_year,
                             validate_birth_year,
                             )

"""
"MMR vaccine is very safe and effective. The mumps component of the MMR vaccine
is about 88% (range: 31-95%) effective when a person gets two doses; one dose
is about 78% (range: 49%−92%) effective. Children may also get MMRV vaccine,
which protects against measles, mumps, rubella, and varicella (chickenpox)."

"During these outbreaks, people who previously had one or two doses of MMR
vaccine can get mumps too. Experts aren’t sure why vaccinated people still get
mumps; it could be that their immune system didn’t respond as well as it
should have to the vaccine. Or their immune system’s ability to fight the
infection decreased over time. Disease symptoms are milder and complications
are less frequent in vaccinated people. Also, high vaccination coverage helps
to limit the size, duration, and spread of mumps outbreaks. So it’s still
very important to be up to date on MMR vaccine."

"During a mumps outbreak, public health authorities might recommend an
additional dose of MMR vaccine for people who belong to groups at increased
risk for getting mumps. These groups are usually those who are likely to have
close contact, such as sharing sport equipment or drinks, kissing, or living
in close quarters, with a person who has mumps. Your local public health
authorities or institution will notify you if you are at increased risk and
should receive this dose. If you already have two doses of MMR, it is not
necessary to seek out vaccination unless the authorities tell you that
you are part of this group."
- https://www.cdc.gov/mumps/vaccination.html

Other sources:
https://stm.sciencemag.org/content/10/433/eaao5945
https://www.hsph.harvard.edu/news/press-releases/mumps-resurgence-waning-immunity/
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
https://stm.sciencemag.org/content/10/433/eaao5945.full
https://www.immunize.org/catg.d/p4211.pdf
"""

"""
regression_data_1_dose = {
    # Years after age 6: probability of immunity
    -4: .959,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    -0.5: .938,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    1.5: .903,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    3.5: .865,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    5.5: .659,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
}

regression_data_2_dose = {
    # Years after age 6: Probability of immunity
    0.5: 0.964,  # Immunity 6mo after immunisation https://stm.sciencemag.org/content/10/433/eaao5945.full
    27.4: 0.5,  # Avg loss of immunity: https://stm.sciencemag.org/content/10/433/eaao5945.full
    # Of those expected to acquire immunity (96.4%), loss of immunity expected after x years:
    7.9: 0.75 * .964,  # 75% of expected immune: https://stm.sciencemag.org/content/10/433/eaao5945.full
    19: 0.5 * .964,  # 50% of expected immune:  https://stm.sciencemag.org/content/10/433/eaao5945.full
    38: 0.25 * .964,  # 50% of expected immune:  https://stm.sciencemag.org/content/10/433/eaao5945.full
    # Median range estimated 7-8 years ~ 7.5 -6 = 1.5
    -0.5: .988,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    1.5: .958,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    3.5: .924,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
    5.5: .864,  # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2913658/
}

NB The current iterations of these algorithms have one-dose immunity greater
than two dose immunity for a birth year before 1942 (ie birth_year <= 1941),
but since persons this age are unlikely to have had shots, and this difference
is a small fraction of a percent, this is considered an acceptable inaccuracy.
"""
natural_immunity = 0.0  # Presumed, arbitrary value.

# Arbitrary value based on rarity of second infection eg https://www.immunize.org/catg.d/p4211.pdf
conferred_immunity = 0.99

# y = ae^bx
one_dose_init_immunity = 0.8953221919
one_dose_waning_imm_exp_coeff = -0.0309279447

two_dose_init_immunity = 0.9945023402
two_dose_waning_imm_exp_coeff = -0.03239090802


def one_dose_immunity(birth_year: int) -> float:
    """
    Returns a probability of immunity given one dose of mumps vaccine.

    :param birth_year: int
    :return:  float 0<=x<=1
    """
    years_after_age_six = (current_year - birth_year) - 6
    if years_after_age_six < 0:
        years_after_age_six = 0
    # http://www.xuru.org/rt/ExpR.asp
    return one_dose_init_immunity * (e ** (one_dose_waning_imm_exp_coeff * years_after_age_six))


def two_dose_immunity(birth_year: int) -> float:
    """
    Returns a probability of immunity given two doses of mumps vaccine.

    :param birth_year: int
    :return:  float 0<=x<=1
    """
    years_after_age_six = (current_year - birth_year) - 6
    if years_after_age_six < 0:
        years_after_age_six = 0
    # http://www.xuru.org/rt/ExpR.asp
    return two_dose_init_immunity * (e ** (two_dose_waning_imm_exp_coeff * years_after_age_six))


def immunity(birth_year: int,
             on_time_mumps_vaccinations: int = None,
             mumps_illness: bool = False) -> Dict[str, Union[float, List[str]]]:
    """
    Takes year of birth, number of shots before age 6, previous illness, and
    provides an estimated probability of being immune to mumps if exposed.

    Returns a float probability, and a list of content templates.

    birth_year accepts a four digit positive integer to compare to 1957.

    on_time_mumps_vaccinations not required -  not supplied or falsey value
        such as None, False, ''

    ValueError will be deliberately raised on improper data.

    templates:  'pre_1957_message': CDC explanation of assumed immunity due to
                    exposure before vaccines.
                    ref: https://www.cdc.gov/vaccines/vpd/mmr/public/index.html

                'has_immunisations': Correct immunisations.

                'greater_than_two_shots_before_age_six_message': Note about
                    data being unavailable for more than 2 shots before age 6,
                    but likely immune.

                'no_immunisations': Unlikely to have any immunity.

                'previous_illness': Documented previous illness, likely immune.

                'waning_warning': Note about efficacy decreasing over time,
                    differing takeup by immune system"),


    :param birth_year: int
    :param on_time_mumps_vaccinations: int or None
    :param mumps_illness: bool
    :raises: ValueError On improper valued data.
    :return: Dict {'probability_of_mumps_immunity': float, 'content_templates': List[str]}
    """
    # Set defaults:
    probability, templates = natural_immunity, ['no_immunisations']

    # Enforce integer 4 digit birth year up to current year.
    validate_birth_year(birth_year)

    if mumps_illness:
        probability, templates = conferred_immunity, ['previous_illness']

    elif birth_year < 1957:
        probability, templates = conferred_immunity, ['pre_1957_message',
                                                      ]
    elif on_time_mumps_vaccinations:
        if not (int(on_time_mumps_vaccinations) > 0  # Must be > 0
                # Must be integer.
                and (isinstance(on_time_mumps_vaccinations, int)
                     # Or float equiv to int eg 2.0 = 2
                     or int(on_time_mumps_vaccinations) == on_time_mumps_vaccinations)):
            raise ValueError('Mumps vaccinations must be a positive integer.')  # Or zero.

        if on_time_mumps_vaccinations == 1:
            probability, templates = one_dose_immunity(birth_year), ['has_immunisations',
                                                                     'waning_warning',
                                                                     ]
        if on_time_mumps_vaccinations == 2:
            probability, templates = two_dose_immunity(birth_year), ['has_immunisations',
                                                                     'waning_warning',
                                                                     ]
        if on_time_mumps_vaccinations > 2:
            probability, templates = two_dose_immunity(birth_year), ['has_immunisations',
                                                                     'waning_warning',
                                                                     'greater_than_two_shots_before_age_six_message',
                                                                     ]
    return {'probability_of_mumps_immunity': probability, 'content_templates': templates}

# need case where shots after age 6
