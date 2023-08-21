from typing import (Optional, Dict,
                    List,
                    Union)

from .common_helpers import validate_birth_year

"""
CDC Presumptive evidence of immunity: https://www.cdc.gov/vaccines/pubs/surv-manual/chpt07-measles.html


"Birth before 1957 provides only presumptive evidence for measles, mumps, and
rubella. Before vaccines were available, nearly everyone was infected with
measles, mumps, and rubella viruses during childhood. The majority of people
born before 1957 are likely to have been infected naturally and therefore are
presumed to be protected against measles, mumps, and rubella. Healthcare
personnel born before 1957 without laboratory evidence of immunity or disease
should consider getting two doses of MMR vaccine." - https://www.cdc.gov/vaccines/vpd/mmr/public/index.html


"Measles is a highly contagious virus that lives in the nose and throat mucus
of an infected person. It can spread to others through coughing and sneezing.
Also, measles virus can live for up to two hours in an airspace where the
infected person coughed or sneezed.

If other people breathe the contaminated air or touch the infected surface,
then touch their eyes, noses, or mouths, they can become infected. Measles is
so contagious that if one person has it, up to 90% of the people close to
that person who are not immune will also become infected.

Infected people can spread measles to others from four days before through
four days after the rash appears."
https://www.cdc.gov/measles/transmission.html


"Before a vaccine was available, infection with measles virus was nearly
universal during childhood, and more than 90% of persons were immune by age 15
years. Measles is still a common and often fatal disease in developing
countries. The World Health Organization estimates there were 145,700 deaths
globally from measles in 2013."

"Measles is highly communicable, with greater than 90% secondary attack rates
among susceptible persons. Measles may be transmitted from 4 days before to 4
days after rash onset. Maximum communicability occurs from onset of prodrome
through the first 3–4 days of rash."

"Although the titer of vaccine-induced antibodies is lower than that following
natural disease, both serologic and epidemiologic evidence indicate that
vaccine-induced immunity appears to be long-term and probably lifelong in
most persons. Most vaccinated persons who appear to lose antibody show an
anamnestic immune response upon revaccination, indicating that they are
probably still immune. Although revaccination can increase antibody titer in
some persons, available data indicate that the increased titer may not be
sustained. Some studies indicate that secondary vaccine failure
(waning immunity) may occur after successful vaccination, but this appears to 
occur rarely and to play only a minor role in measles transmission and
outbreaks." -> Vaccine does not wane.
https://www.cdc.gov/vaccines/pubs/pinkbook/meas.html


*Use conferred immunity as immunity for reinfection, since pre-1957 immunity
is based on previous infection/exposure.*

"Does past infection to measles make a person immune?
Yes. Persons who have had measles in the past have lifelong immunity. Since
measles can be confused with other infections that cause fever and a rash, a
person needs a special blood test to be sure they are immune. "
https://www.bphc.org/whatwedo/infectious-diseases/Infectious-Diseases-A-to-Z/Pages/Measles.aspx

"CDC considers you protected from measles if you have written documentation
(records) showing at least one of the following:

You received two doses of measles-containing vaccine, and you are a(n) —
school-aged child (grades K-12)
adult who will be in a setting that poses a high risk for measles transmission,
including students at post-high school education institutions, healthcare
personnel, and international travelers.
You received one dose of measles-containing vaccine, and you are a(n) —
preschool-aged child
adult who will not be in a high-risk setting for measles transmission.
A laboratory confirmed that you had measles at some point in your life.
A laboratory confirmed that you are immune to measles."
cdc.gov/measles/about/faqs.html


"""

conferred_immunity = 0.90
natural_immunity = 0.10
# shots before 6 years
shots_under_6_immunity = {
    0: natural_immunity,
    1: 0.93,
    2: 0.97,
}


def immunity(birth_year: int,
             on_time_measles_vaccinations: Optional[int] = None,
             measles_illness: bool = False) -> Dict[str, Union[float, List[str]]]:
    """
    Takes year of birth, number of shots before age 6, previous illness and
    provides an estimated probability of being immune to measles if exposed.

    Returns a float probability, and a list of content templates.

    birth_year accepts a four digit positive integer to compare to 1957.

    on_time_measles_vaccinations not required -  not supplied or falsey value
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


    :param birth_year: int
    :param on_time_measles_vaccinations: int or None
    :param measles_illness: bool
    :raises: ValueError On improper valued data.
    :return: Dict {'probability_of_measles_immunity': float, 'content_templates': List(str)}
    """
    # Set defaults:
    probability, templates = shots_under_6_immunity[0], ['no_immunisations']

    # Enforce integer 4 digit birth year up to current year.
    validate_birth_year(birth_year)

    if measles_illness:
        # Presume immunity from infection similar to pre-1957 immunity,
        # since pre-1957 immunity is presumed based on exposure/infection.
        probability, templates = conferred_immunity, ['previous_illness']

    elif birth_year < 1957:
        probability, templates = conferred_immunity, ['pre_1957_message']

    elif on_time_measles_vaccinations:
        if not (int(on_time_measles_vaccinations) > 0  # Must be > 0
                # Must be integer.
                and (isinstance(on_time_measles_vaccinations, int)
                     # Or float equiv to int eg 2.0 = 2
                     or int(on_time_measles_vaccinations) == on_time_measles_vaccinations)):
            raise ValueError('Measles vaccinations must be a positive integer.')  # Or zero.

        if on_time_measles_vaccinations <= 2:
            probability, templates = shots_under_6_immunity[on_time_measles_vaccinations], ['has_immunisations']
        if on_time_measles_vaccinations > 2:
            probability, templates = shots_under_6_immunity[2], ['has_immunisations',
                                                                 'greater_than_two_shots_before_age_six_message']

    return {'probability_of_measles_immunity': probability, 'content_templates': templates}

# need case where shots after age 6
