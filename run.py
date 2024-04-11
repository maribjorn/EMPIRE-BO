#!/usr/bin/env python
from reader import generate_tab_files
from Empire import run_empire
from scenario_random import generate_random_scenario
from datetime import datetime
from yaml import safe_load

__author__ = "Stian Backe"
__license__ = "MIT"
__maintainer__ = "Stian Backe"
__email__ = "stian.backe@ntnu.no"

UserRunTimeConfig = safe_load(open("config_run.yaml"))

USE_TEMP_DIR = UserRunTimeConfig["USE_TEMP_DIR"]
temp_dir = UserRunTimeConfig["temp_dir"]
version = UserRunTimeConfig["version"]
Horizon = UserRunTimeConfig["Horizon"]
NoOfScenarios = UserRunTimeConfig["NoOfScenarios"]
lengthRegSeason = UserRunTimeConfig["lengthRegSeason"]
discountrate = UserRunTimeConfig["discountrate"]
WACC = UserRunTimeConfig["WACC"]
solver = UserRunTimeConfig["solver"]
scenariogeneration = UserRunTimeConfig["scenariogeneration"]
fix_sample = UserRunTimeConfig["fix_sample"]
LOADCHANGEMODULE = UserRunTimeConfig["LOADCHANGEMODULE"]
filter_make = UserRunTimeConfig["filter_make"] 
filter_use = UserRunTimeConfig["filter_use"]
n_cluster = UserRunTimeConfig["n_cluster"]
moment_matching = UserRunTimeConfig["moment_matching"]
n_tree_compare = UserRunTimeConfig["n_tree_compare"]
EMISSION_CAP = UserRunTimeConfig["EMISSION_CAP"]
IAMC_PRINT = UserRunTimeConfig["IAMC_PRINT"]
WRITE_LP = UserRunTimeConfig["WRITE_LP"]
PICKLE_INSTANCE = UserRunTimeConfig["PICKLE_INSTANCE"] 


#############################
##Non configurable settings##
#############################

NoOfRegSeason = 4
regular_seasons = ["winter", "spring", "summer", "fall"]
NoOfPeakSeason = 2
lengthPeakSeason = 2
LeapYearsInvestment = 5
time_format = "%d/%m/%Y %H:%M"
if version in ["europe_v50"]:
    north_sea = False
else:
    north_sea = True

#######
##RUN##
#######

name = version + '_reg' + str(lengthRegSeason) + \
    '_peak' + str(lengthPeakSeason) + \
    '_sce' + str(NoOfScenarios)
if scenariogeneration and not fix_sample:
        name = name + "_randomSGR"
else:
	name = name + "_noSGR"
if filter_use:
    name = name + "_filter" + str(n_cluster)
if moment_matching:
    name = name + "_moment" + str(n_tree_compare)
name = name + str(datetime.now().strftime("_%Y%m%d%H%M"))
workbook_path = 'Data handler/' + version
tab_file_path = 'Data handler/' + version + '/Tab_Files_' + name
scenario_data_path = 'Data handler/' + version + '/ScenarioData'
result_file_path = 'Results/' + name
FirstHoursOfRegSeason = [lengthRegSeason*i + 1 for i in range(NoOfRegSeason)]
FirstHoursOfPeakSeason = [lengthRegSeason*NoOfRegSeason + lengthPeakSeason*i + 1 for i in range(NoOfPeakSeason)]
Period = [i + 1 for i in range(int((Horizon-2020)/LeapYearsInvestment))]
Scenario = ["scenario"+str(i + 1) for i in range(NoOfScenarios)]
peak_seasons = ['peak'+str(i + 1) for i in range(NoOfPeakSeason)]
Season = regular_seasons + peak_seasons
Operationalhour = [i + 1 for i in range(FirstHoursOfPeakSeason[-1] + lengthPeakSeason - 1)]
HoursOfRegSeason = [(s,h) for s in regular_seasons for h in Operationalhour \
                 if h in list(range(regular_seasons.index(s)*lengthRegSeason+1,
                               regular_seasons.index(s)*lengthRegSeason+lengthRegSeason+1))]
HoursOfPeakSeason = [(s,h) for s in peak_seasons for h in Operationalhour \
                     if h in list(range(lengthRegSeason*len(regular_seasons)+ \
                                        peak_seasons.index(s)*lengthPeakSeason+1,
                                        lengthRegSeason*len(regular_seasons)+ \
                                            peak_seasons.index(s)*lengthPeakSeason+ \
                                                lengthPeakSeason+1))]
HoursOfSeason = HoursOfRegSeason + HoursOfPeakSeason
dict_countries = {'BO0 0': 'BO0 0',
                   'BO0 1': 'BO0 1',
                    'BO0 2': 'BO0 2',
                    'BO0 3': 'BO0 3',
                    'BO0 4': 'BO0 4',
                    'BO0 5': 'BO0 5',
                    'BO0 6': 'BO0 6',
                    'BO0 7': 'BO0 7',
                    'BO0 8': 'BO0 8',
                    'BO0 9': 'BO0 9',
                    'BO0 10': 'BO0 10',
                    'BO0 11': 'BO0 11',
                    'BO0 12': 'BO0 12',
                    'BO0 13': 'BO0 13',
                    'BO0 14': 'BO0 14',
                    'BO0 15': 'BO0 15',
                    'BO0 16': 'BO0 16',
                    'BO0 17': 'BO0 17',
                    'BO0 18': 'BO0 18',
                    'BO0 19': 'BO0 19',
                    'BO0 20': 'BO0 20',
                    'BO0 21': 'BO0 21',
                    'BO0 22': 'BO0 22',
                    'BO0 23': 'BO0 23',
                    'BO0 24': 'BO0 24',
                    'BO0 25': 'BO0 25',
                    'BO0 26': 'BO0 26',
                    'BO0 27': 'BO0 27',
                    'BO0 28': 'BO0 28',
                    'BO0 29': 'BO0 29'}

# dict_countries = {"AT": "Austria", "BA": "BosniaH", "BE": "Belgium",
#                   "BG": "Bulgaria", "CH": "Switzerland", "CZ": "CzechR",
#                   "DE": "Germany", "DK": "Denmark", "EE": "Estonia",
#                   "ES": "Spain", "FI": "Finland", "FR": "France",
#                   "GB": "GreatBrit.", "GR": "Greece", "HR": "Croatia",
#                   "HU": "Hungary", "IE": "Ireland", "IT": "Italy",
#                   "LT": "Lithuania", "LU": "Luxemb.", "LV": "Latvia",
#                   "MK": "Macedonia", "NL": "Netherlands", "NO": "Norway",
#                   "PL": "Poland", "PT": "Portugal", "RO": "Romania",
#                   "RS": "Serbia", "SE": "Sweden", "SI": "Slovenia",
#                   "SK": "Slovakia", "MF": "MorayFirth", "FF": "FirthofForth",
#                   "DB": "DoggerBank", "HS": "Hornsea", "OD": "OuterDowsing",
#                   "NF": "Norfolk", "EA": "EastAnglia", "BS": "Borssele",
#                   "HK": "HollandseeKust", "HB": "HelgolanderBucht", "NS": "Nordsoen",
#                   "UN": "UtsiraNord", "SN1": "SorligeNordsjoI", "SN2": "SorligeNordsjoII"}

print('++++++++')
print('+EMPIRE+')
print('++++++++')
print('LOADCHANGEMODULE: ' + str(LOADCHANGEMODULE))
print('Solver: ' + solver)
print('Scenario Generation: ' + str(scenariogeneration))
print('++++++++')
print('ID: ' + name)
print('++++++++')

if scenariogeneration:
    generate_random_scenario(filepath = scenario_data_path,
                             tab_file_path = tab_file_path,
                             scenarios = NoOfScenarios,
                             seasons = regular_seasons,
                             Periods = len(Period),
                             regularSeasonHours = lengthRegSeason,
                             peakSeasonHours = lengthPeakSeason,
                             dict_countries = dict_countries,
                             time_format = time_format,
                             filter_make = filter_make,
                             filter_use = filter_use,
                             n_cluster = n_cluster,
                             moment_matching = moment_matching,
                             n_tree_compare = n_tree_compare,
                             fix_sample = fix_sample,
                             north_sea = north_sea,
                             LOADCHANGEMODULE = LOADCHANGEMODULE)

generate_tab_files(filepath = workbook_path, tab_file_path = tab_file_path)

run_empire(name = name, 
           tab_file_path = tab_file_path,
           result_file_path = result_file_path, 
           scenariogeneration = scenariogeneration,
           scenario_data_path = scenario_data_path,
           solver = solver,
           temp_dir = temp_dir, 
           FirstHoursOfRegSeason = FirstHoursOfRegSeason, 
           FirstHoursOfPeakSeason = FirstHoursOfPeakSeason, 
           lengthRegSeason = lengthRegSeason,
           lengthPeakSeason = lengthPeakSeason,
           Period = Period, 
           Operationalhour = Operationalhour,
           Scenario = Scenario,
           Season = Season,
           HoursOfSeason = HoursOfSeason,
           discountrate = discountrate, 
           WACC = WACC, 
           LeapYearsInvestment = LeapYearsInvestment,
           IAMC_PRINT = IAMC_PRINT, 
           WRITE_LP = WRITE_LP, 
           PICKLE_INSTANCE = PICKLE_INSTANCE, 
           EMISSION_CAP = EMISSION_CAP,
           USE_TEMP_DIR = USE_TEMP_DIR,
           LOADCHANGEMODULE = LOADCHANGEMODULE)
