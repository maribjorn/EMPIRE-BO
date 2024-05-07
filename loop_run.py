import os
 
# Define the number of times to run the command
num_runs = 15

shedding_cost_increase = 1
 
# Loop to run the command multiple times
for _ in range(num_runs):
        
    # Run the command
    os.system("python run.py")