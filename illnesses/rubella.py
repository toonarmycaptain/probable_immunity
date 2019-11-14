from typing import Dict, Union, List

from .common_helpers import validate_birth_year

"""
https://www.cdc.gov/rubella/vaccination.html

"Vaccine Effectiveness
One dose
1 dose of MMR vaccine is—
93% effective for measles (range: 39%–100%)
78% effective for mumps (range: 49%−92%)
97% effective for rubella (range: 94%–100%)"
-https://www.cdc.gov/vaccines/vpd/mmr/hcp/about.html

Presumptive immunity:
    - 1+ dose of vaccine
    - lab evidence of immunity/antibodies or illness
    - birth before 1957
https://www.cdc.gov/vaccines/pubs/surv-manual/chpt14-rubella.html
https://www.cdc.gov/rubella/hcp.html


"In the United States, rubella vaccine is available in combination with mumps
 and measles (MMR) vaccine or as a quadrivalent vaccine in combination with
 measles, mumps, and varicella (MMRV). One dose of the vaccine administered at
 12 or more months of age is immunogenic in more than 95% of recipients and
 confers lifelong immunity in more than 90% of vaccinees; the seroconversion
 rate is 99% after two doses of the MMR vaccine.
Reinfection after vaccination is rare."
-Principles and Practice of Pediatric Infectious Diseases (Fifth Edition) 2018,
 Sarah S. Long, Charles G. Prober and Marc Fischer
- chpt ref'd is by Yvonna A Maldonado, Avinash K. SHetty
-https://www.sciencedirect.com/topics/immunology-and-microbiology/rubella-virus

"A second dose of MMR is recommended to produce immunity to measles and mumps
 in those who failed to respond to the first dose. Data indicate that almost
 all persons who do not respond to the measles component of the first dose will
 respond to a second dose of MMR. Few data on the immune response to the
 rubella and mumps components of a second dose of MMR are available. However,
 most persons who do not respond to the rubella or mumps component of the
 first MMR dose would be expected to respond to the second dose. The second
 dose is not generally considered a booster dose because a primary immune
 response to the first dose provides long-term protection. Although a second
 dose of vaccine may increase antibody titers in some persons who responded
 to the first dose, available data indicate that these increased antibody
 titers are not sustained. The combined MMR vaccine is recommended for both
 doses to ensure immunity to all three viruses."
-https://www.cdc.gov/vaccines/pubs/pinkbook/rubella.html
-> second dose will give immunity for those who did not respond to first dose,
but will not confer better or increased likelihood of immunity in those who
already show some immunity.

"This recommendation is based on serologic studies which indicate that among
 hospital personnel born before 1957, 5% to 9% had no detectable measles
  antibody."
-https://www.cdc.gov/vaccines/pubs/pinkbook/rubella.html
-> ~ 7% non-immunity for Pre-1957
"""

conferred_immunity = 0.93
natural_immunity = 0.10

unvaccinated_immunity = natural_immunity
vaccinated_immunity = 0.97


def immunity(birth_year: int,
             rubella_vaccinations: int = None,
             rubella_illness: bool = False) -> Dict[str, Union[float, List[str]]]:
    """
    Takes year of birth, number of shots before age 6, and provides an
    estimated probability of being immune to rubella if exposed.

    Returns a float probability, and a list of content templates.

    birth_year accepts a four digit positive integer to compare to 1957.

    rubella_vaccinations not required -  not supplied or falsey value
        such as None, False, ''

    ValueError will be deliberately raised on improper data.


    templates:   'pre_1957_message': CDC explanation of assumed immunity due to
                    exposure before vaccines.
                    ref: https://www.cdc.gov/vaccines/vpd/mmr/public/index.html

                'has_immunisations': Correct immunisations.

                'no_immunisations': Unlikely to have any immunity.

    As compared to measles and mumps in the MMR combo, rubella immunity does
    not wane with time, and has good data available for late vaccination and
    vaccination in adulthood, so conditioning vaccinated immunity accuracy on
    shots being given on time/before age six is unnecessary.

    :param birth_year: int
    :param rubella_vaccinations: int or None
    :param rubella_illness: bool
    :raises: ValueError On improper valued data.
    :return: Dict {'probability_of_rubella_immunity': float, 'content_templates': List(str)}
    """
    # Set defaults:
    probability, templates = unvaccinated_immunity, ['no_immunisations']

    # Enforce integer 4 digit birth year up to current year.
    validate_birth_year(birth_year)

    if rubella_illness:
        probability, templates = conferred_immunity, ['previous_illness']

    elif birth_year < 1957:
        probability, templates = conferred_immunity, ['pre_1957_message']

    elif rubella_vaccinations:
        if not (int(rubella_vaccinations) > 0  # Must be > 0
                # Must be integer.
                and (isinstance(rubella_vaccinations, int)
                     # Or float equiv to int eg 2.0 = 2
                     or int(rubella_vaccinations) == rubella_vaccinations)):
            raise ValueError('rubella vaccinations must be a positive integer.')  # Or zero.

        # No increased likelihood of immunity for subsequent immunisations.
        probability, templates = vaccinated_immunity, ['has_immunisations']

    return {'probability_of_rubella_immunity': probability, 'content_templates': templates}
