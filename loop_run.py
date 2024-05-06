import os
from openpyxl import load_workbook

Horizon = 2044
start_year = 2024
LeapYearsInvestment = 5
total_periods = int((Horizon - start_year)/LeapYearsInvestment)

bus_map = load_workbook('data_pypsa/bus_map30.xlsx').active
new_names = [cell.value for cell in bus_map['A'][1:]]
 
# Define the number of times to run the command
num_runs = 15

shedding_cost_increase = 1
 
# Loop to run the command multiple times
for _ in range(num_runs):
        
    # Run the command
    os.system("python run.py")