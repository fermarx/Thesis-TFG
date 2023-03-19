import pandas as pd
import numpy as np

# With the objective of having the plant info and the sow month, we want to unify both files
# We read the 2 files we need
print("Reading file...")
file = pd.read_csv("final.csv")

# From cm to inches
spaceBeforeG = file["spaceInstructions"].str.extract("Space plants: (\w+) - ")
spaceInIn = file["spaceInstructions"].str.extract("Space plants: (\w+) inches apart")
spaceInInBeforeG = file["spaceInstructions"].str.extract("- (\w+) inches apart")
spaceInCm = file["spaceInstructions"].str.extract("Space plants: (\w+) cm apart")
spaceInCmBeforeG = file["spaceInstructions"].str.extract("- (\w+) cm apart")
inches = []
for i in range(len(spaceBeforeG[0])):  
    if (spaceInCmBeforeG[0][i] is not np.nan) or (spaceInCm[0][i] is not np.nan): 
        if (spaceInCm[0][i] is not np.nan): inches.append(float(spaceInCm[0][i])/2.54)
        else:
            mean = (float(spaceBeforeG[0][i])+float(spaceInCmBeforeG[0][i]))/2
            inches.append(round((mean/2.54), 2))
    elif (spaceInInBeforeG[0][i] is not np.nan) or (spaceInIn[0][i] is not np.nan):
        if (spaceInIn[0][i] is not np.nan): inches.append(spaceInIn[0][i])
        else:
            mean = (float(spaceBeforeG[0][i])+float(spaceInInBeforeG[0][i]))/2
            inches.append(round(mean, 2))
    else: inches.append(np.nan)
file["spaceInstructions"] = inches

# Delete repeated infomation
file["spaceInstructions"] = file["spaceInstructions"].map(lambda x: str(x).lstrip("Space plants: "))
file["spaceInstructions"] = file["spaceInstructions"].map(lambda x: str(x).rstrip(" inches apart"))
file["spaceInstructions"] = file["spaceInstructions"].map(lambda x: str(x).rstrip(" cm apart"))
file.rename(columns={'spaceInstructions': 'spaceInstructionsInches'}, inplace=True)

file["harvestInstructions"] = file["harvestInstructions"].map(lambda x: str(x).lstrip("Harvest in "))
file["harvestInstructions"] = file["harvestInstructions"].map(lambda x: str(x).lstrip("pproximately "))

file["compatiblePlants"] = file["compatiblePlants"].map(lambda x: str(x).lstrip("Compatible with (can grow beside): "))

file.drop(columns=["Unnamed: 0"],axis = 1, inplace=True) # Delete unused columns

print("Creating new file...")
# We store the final file
file.to_csv("final_prueba.csv")
print("*********************New file created in ../DB/final_prueba.csv*********************")