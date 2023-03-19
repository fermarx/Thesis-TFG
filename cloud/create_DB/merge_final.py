import pandas as pd
import numpy as np
import re

pd.options.mode.chained_assignment = None  # # default='warn'
# With the objective of having the plant info and the sow month, we want to unify both files
# We read the 2 files we need
print("Reading files...")
plantInfo_clean = pd.read_csv("iniF/plantInfo-clean.csv")
merged_total = pd.read_csv("iniF/merged_total.csv")

# We unify the two files 
# Name,alternateName,sowInstructions,spaceInstructions,harvestInstructions,compatiblePlants,avoidInstructions,culinaryHints,culinaryPreservation,url
print("Unifying files...")
plantInfo_clean = plantInfo_clean.merge(merged_total, on="Name", how="left")
plantInfo_clean.drop(columns=["Unnamed: 0"],axis = 1, inplace=True) # Delete unused columns
plantInfo_clean.drop_duplicates(inplace=True) # Delete duplicates

print("Creating new columns...")
# Create new column to check if it is easy to grow ot not
# We search if in the instructions it says if its easy to grow and create a new table with that information
easy = plantInfo_clean.loc[plantInfo_clean["sowInstructions"].str.contains("Easy to grow", case=False)] 
# Delte repeated infomation
plantInfo_clean["sowInstructions"] = plantInfo_clean["sowInstructions"].map(lambda x: x.lstrip("Easy to grow. "))
# Create the new column in the "easy" table
easy["easyGrow"] = list([1]*len(easy))

# we drop all the coolumns that are not "Name" and "easygrow", as they are the only ones that are going to be useful
col = ["alternateName", "sowInstructions", "spaceInstructions","harvestInstructions","compatiblePlants","avoidInstructions","culinaryHints","culinaryPreservation","url", "sowMonthJan","sowMonthFeb","sowMonthMar","sowMonthApr","sowMonthMay","sowMonthJun","sowMonthJul","sowMonthAug","sowMonthSep","sowMonthOct","sowMonthNov","sowMonthDec"]
easy.drop(columns=col ,axis = 1, inplace=True)
# We merge and drop duplicates. If NaN, Not easy to grow. If 1, easy to grow
plantInfo_clean = plantInfo_clean.merge(easy, on="Name", how="left")
plantInfo_clean.drop_duplicates(inplace=True)

# Our interest is to have the temperature in its own column
minTinC = plantInfo_clean["sowInstructions"].str.extract(". Best planted at soil temperatures between (\w+)°C.")
maxTinC = plantInfo_clean["sowInstructions"].str.extract("C and (\w+).")
minTinF = plantInfo_clean["sowInstructions"].str.extract(". Best planted at soil temperatures between (\w+)°F.")
maxTinF = plantInfo_clean["sowInstructions"].str.extract("F and (\w+).")
farenheitMin = []
farenheitMax = []
for i in range(len(minTinC[0])):  
    if (minTinC[0][i] is not np.nan) and (maxTinC[0][i] is not np.nan):
        min = (float(minTinC[0][i])*1.8)+32
        max = (float(maxTinC[0][i])*1.8)+32
        farenheitMin.append(min)
        farenheitMax.append(max)
    else: 
        farenheitMin.append(minTinF[0][i])
        farenheitMax.append(maxTinF[0][i])
plantInfo_clean["minTinF"] = farenheitMin
plantInfo_clean["maxTinF"] = farenheitMax

# Delete the duplicated information
plantInfo_clean["sowInstructions"] = plantInfo_clean["sowInstructions"].map(lambda x: re.sub(r". Best planted at soil temperatures between \d+°\w and \d+°\w. \(Show °\w/\w+\)", ".", x))

print("Sorting rows...")
# We sort the list first by the sow month and then by name
plantInfo_clean.sort_values(["Name"], inplace=True)

print("Creating new file...")
# We store the final file
plantInfo_clean.to_csv("prueba.csv")
print("*********************New file created in ../DB/final.csv*********************")