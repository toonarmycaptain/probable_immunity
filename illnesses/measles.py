from typing import Dict

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
"""

rec_shots_under_6 = 2

conferred_immunity = 1

"""
messages:   'pre_1957_message': CDC explanation of assumed immunity due to exposure before vaccines.
                ref: https://www.cdc.gov/vaccines/vpd/mmr/public/index.html
                                
            'has_immunisations': Correct immunisations.  # TODO make better message
            
            'greater_than_two_shots_before_age_six_message': Note about data being unavailable for 
                more than 2 shots before age 6. # TODO add caveat about meeting minimum 
                requirements, likely immune. 
                
                                                             
            'no_immunisations': Unlikely to have any immunity.
"""
# shots before 6 years
shots_under_6_immunity = {
    1: 0.93,
    2: 0.97,
}


def immunity(birth_year=None, on_time_measles_vaccinations: int = None) -> Dict:
    """
    Takes year of birth, number of shots before age 6, and provides an
    estimated probability of being immune to measles if exposed.

    Returns a float probability, and a list of content templates.

    :param birth_year: int or None
    :param on_time_measles_vaccinations: int or None
    :return: Dict {'probability_of_measles_immunity': float, 'content_templates': List(str)}
    """
    # Set defaults:
    probability, messages = 0.0, ['no_immunisations']
    if birth_year < 1957:
        probability, messages = 1.0, ['pre_1957_message']
    elif on_time_measles_vaccinations:
        if on_time_measles_vaccinations <= 2:
            probability, messages = shots_under_6_immunity[on_time_measles_vaccinations], ['has_immunisations']
        if on_time_measles_vaccinations > 2:
            probability, messages = shots_under_6_immunity[2], ['greater_than_two_shots_before_age_six_message']
    return {'probability_of_measles_immunity': probability, 'content_templates': messages}

# need case where shots after age 6
