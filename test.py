import datetime
import pandas
from openfisca_collectivites_territoriales import CountryTaxBenefitSystem


mapping_path = 'data/mapping.xlsx'
mapping_data = pandas.read_excel(mapping_path)
mapping = { row.OpenFisca: row.Base for row in mapping_data.itertuples() }

tax_benefit_system = CountryTaxBenefitSystem()

file_path_2019 = 'data/2019-communes-criteres-repartition.csv'
data_2019 = pandas.read_csv(file_path_2019, low_memory=False)
length = len(data_2019)

file_path_2018 = 'data/2018-communes-criteres-repartition.csv'
data_2018 = pandas.read_csv(file_path_2018, low_memory=False)

data = data_2019.set_index(mapping['depcom']).join(data_2018.set_index(mapping['depcom']), lsuffix='2019', rsuffix='2018')

# prefix = str(datetime.datetime.now()).replace(':', '-').replace(' ', '--')
# with pandas.ExcelWriter(prefix + 'head.xlsx') as writer:
#   data.head(n=100).to_excel(writer, sheet_name='error')

from openfisca_core.simulation_builder import SimulationBuilder
import numpy

simulation = SimulationBuilder().build_default_simulation(tax_benefit_system, length)

period = '2019'
inputs = ['population_insee', 'nb_residences_secondaires', 'nb_caravanes']
for i in inputs:
  simulation.set_input(i, period, numpy.array(data[mapping[i] + period]))

period = '2018'
inputs = ['dotation_solidarite_urbaine', 'premiere_fraction_dotation_solidarite_rurale']
for i in inputs:
  simulation.set_input(i, period, numpy.array(data[mapping[i] + period]))


period = '2019'
computation_variable = 'strate_demographique'
computation = simulation.calculate(computation_variable, period)
result = (data[mapping[computation_variable] + period] != computation)

ko = sum(result)
print(ko)
print((length - ko)/ length)

prefix = str(datetime.datetime.now()).replace(':', '-').replace(' ', '--')
with pandas.ExcelWriter(prefix + 'error.xlsx') as writer:
  data[result].to_excel(writer, sheet_name='error')
