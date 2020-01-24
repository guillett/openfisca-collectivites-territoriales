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
