# -*- coding: utf-8 -*-
from openfisca_core.model_api import *
from openfisca_collectivites_territoriales.entities import *


class dotation_solidarite_urbaine(Variable):
    value_type = float
    entity = Person
    definition_period = YEAR
