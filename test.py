import pandas
from openfisca_collectivites_territoriales import CountryTaxBenefitSystem


mapping_path = '/home/thomas/repos/openfisca-collectivites-territoriales/mapping.xlsx'
mapping_data = pandas.read_excel(mapping_path)
mapping = { row.OpenFisca: row.Base for row in mapping_data.itertuples() }

tax_benefit_system = CountryTaxBenefitSystem()

file_path_2019 = '/home/thomas/Documents/Beta.gouv.fr/Datafin/2019-communes-criteres-repartition.csv'
data_2019 = pandas.read_csv(file_path_2019, low_memory=False)
length = len(data_2019)

# file_path_2018 = '/home/thomas/Documents/Beta.gouv.fr/Datafin/2018-communes-criteres-repartition.csv'
# data_2018 = pandas.read_csv(file_path_2018, low_memory=False)

from openfisca_core.simulation_builder import SimulationBuilder
import numpy

simulation = SimulationBuilder().build_default_simulation(tax_benefit_system, length)

period = '2019'
inputs = ['population_insee', 'nb_residences_secondaires', 'nb_caravanes']
for i in inputs:
  simulation.set_input(i, period, numpy.array(data_2019[mapping[i]]))

period = '2018'
inputs = ['dotation_solidarite_urbaine', 'premiere_fraction_dotation_solidarite_rurale']
for i in inputs:
  simulation.set_input(i, period, numpy.array(data_2019[mapping[i]]))


period = '2019'
population_dgf = simulation.calculate('population_dgf', period)
result = (data_2019[mapping['population_dgf']] != population_dgf)

ko = sum(result)
print(ko)
print((length - ko)/ length)

# with pandas.ExcelWriter('error2.xlsx') as writer:
#   data_2019[result].to_excel(writer, sheet_name='error')
#   