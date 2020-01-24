# -*- coding: utf-8 -*-
from openfisca_core.model_api import *
from openfisca_collectivites_territoriales.entities import *


class premiere_fraction_dotation_solidarite_rurale(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
