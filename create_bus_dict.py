import pandas as pd

# Read in the data
busmap = pd.read_excel('data_pypsa/bus_map30.xlsx')

# Create the dictionary
bus_dict = {}

# Iterate over each row in the dataframe
for index, row in busmap.iterrows():
    # Get the bus name
    bus_name = row['Buses']
    
    # Check if the bus name is not NaN
    if pd.notnull(bus_name):
        # Get the values for Name, Old_nodes, and Data_nodes
        name = row['Unnamed: 2']
        old_nodes = row['Gamle noder']
        data_nodes = [row[i] for i in range(2, 8) if pd.notnull(row[i])]
        
        # Create the inner dictionary
        inner_dict = {
            'Name': name,
            'Old_nodes': old_nodes,
            'Data_nodes': data_nodes
        }
        
        # Add the inner dictionary to the bus_dict
        bus_dict[bus_name] = inner_dict
        
print(bus_dict)

node_names = list(bus_dict[bus_name]['Name'] for bus_name in bus_dict)

print(node_names)
