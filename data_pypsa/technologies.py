import pandas as pd

# Path to the data in pypsa
path = 'C:/Users/marih/OneDrive/Documents/pypsa-2802/pypsa-earth/data_EMPIRE'

# Read in the data
custom_powerplants = pd.read_excel(f'{path}/custom_powerplants_EMPIRE.xlsx')

powerplants_dict = {}

for index, row in custom_powerplants.iterrows():
    # Get the fuel type
    fueltype = row['Fueltype']
    
    if pd.notnull(fueltype):
        # Get the values for Fueltype and Technology
        technology = row['Technology']
        
        if fueltype in powerplants_dict:
            powerplants_dict[fueltype].append(technology)
        else:
            powerplants_dict[fueltype] = [technology]
        
        
print(powerplants_dict)