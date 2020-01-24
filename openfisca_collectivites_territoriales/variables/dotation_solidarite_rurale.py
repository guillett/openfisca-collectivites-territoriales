# -*- coding: utf-8 -*-
from openfisca_core.model_api import *
from openfisca_collectivites_territoriales.entities import *


class premiere_fraction_dotation_solidarite_rurale(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR


class second_fraction_dotation_solidarite_rurale_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR

    def formula(person, period, parameters):
      pf_hab = person('potentiel_financier_par_habitant', period)
      strate = person('strate_demographique', period)
      
      plafond = 2 * (
        + (strate == 1) * 657.114759
        + (strate == 2) * 722.315256
        + (strate == 3) * 785.439563
        + (strate == 4) * 862.218176
        + (strate == 5) * 940.663574
        + (strate == 6) * 1016.450575
        + (strate == 7) * 1073.239296
        + (strate > 7) * 0
        )

      return (pf_hab <= plafond)


class second_fraction_dotation_solidarite_rurale(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
