# -*- coding: utf-8 -*-
from openfisca_core.model_api import *
from openfisca_collectivites_territoriales.entities import *


class potentiel_financier(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR


class potentiel_financier_par_habitant(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR

    def formula(person, period, parameters):
      return person('potentiel_financier', period) / person('population_dgf', period)
