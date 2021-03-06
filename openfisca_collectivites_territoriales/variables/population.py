# -*- coding: utf-8 -*-

from openfisca_core.model_api import *
from openfisca_collectivites_territoriales.entities import *


class population_insee(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR


class nb_residences_secondaires(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR


class nb_caravanes(Variable):
    value_type = int
    entity = Person
    definition_period = YEAR


class population_dgf(Variable):
    value_type = int
    entity = Person
    reference = [
        'Code général des collectivités territoriales - Article L2334-2',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000033878277&cidTexte=LEGITEXT000006070633'
        ]
    definition_period = YEAR

    def formula(person, period, parameters):
        insee = person('population_insee', period)
        nb_resid_second = person('nb_residences_secondaires', period)
        nb_caravanes = person('nb_caravanes', period)
        dsu_nm1 = person('dotation_solidarite_urbaine', period.last_year)
        pfrac_dsu_nm1 = person('premiere_fraction_dotation_solidarite_rurale', period.last_year)
 
        return (
            + insee
            + 1 * nb_resid_second
            + 1 * nb_caravanes
            + 1 * nb_caravanes * ((dsu_nm1 > 0) + (pfrac_dsu_nm1 > 0))
            )


class strate_demographique(Variable):
    value_type = int
    entity = Person
    reference = [
        'Code général des collectivités territoriales - Article L2334-3',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000033878299&cidTexte=LEGITEXT000006070633'
        ]
    definition_period = YEAR

    def formula(person, period, parameters):
        pop = person('population_dgf', period)

        return (
            + 1 * (pop <= 499)
            + 2 * (499 < pop) * (pop <= 999)
            + 3 * (999 < pop) * (pop <= 1999)
            + 4 * (1999 < pop) * (pop <= 3499)
            + 5 * (3499 < pop) * (pop <= 4999)
            + 6 * (4999 < pop) * (pop <= 7499)
            + 7 * (7499 < pop) * (pop <= 9999)
            + 8 * (9999 < pop) * (pop <= 14999)
            + 9 * (14999 < pop) * (pop <= 19999)
            + 10 * (19999 < pop) * (pop <= 34999)
            + 11 * (34999 < pop) * (pop <= 49999)
            + 12 * (49999 < pop) * (pop <= 74999)
            + 13 * (74999 < pop) * (pop <= 99999)
            + 14 * (99999 < pop) * (pop <= 199999)
            + 15 * (199999 < pop)
            )
