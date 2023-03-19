from heapq import merge
from statistics import median_grouped
import pandas as pd
import numpy as np


# We create the united file with files 8a and 10a
merged = pd.DataFrame()
clean = pd.DataFrame()
files = ["8a/merged_8a", "10a/merged_10a"]

for file in files:
    month_data = pd.read_csv(f"{file}.csv")

    name = list(month_data["Name"])
    sowMonth = list(month_data["sowMonth"])

    data = {"Name": name,
            "sowMonth": sowMonth}
    
    DBname = {"Name": name}

    merged = merged.append(pd.DataFrame(data))
    clean = clean.append(pd.DataFrame(DBname))

merged = merged.drop_duplicates()
merged = merged.sort_values(["Name", "sowMonth"])

clean["sowMonthJan"] = [0]*len(clean["Name"])
clean["sowMonthFeb"] = [0]*len(clean["Name"])
clean["sowMonthMar"] = [0]*len(clean["Name"])
clean["sowMonthApr"] = [0]*len(clean["Name"])
clean["sowMonthMay"] = [0]*len(clean["Name"])
clean["sowMonthJun"] = [0]*len(clean["Name"])
clean["sowMonthJul"] = [0]*len(clean["Name"])
clean["sowMonthAug"] = [0]*len(clean["Name"])
clean["sowMonthSep"] = [0]*len(clean["Name"])
clean["sowMonthOct"] = [0]*len(clean["Name"])
clean["sowMonthNov"] = [0]*len(clean["Name"])
clean["sowMonthDec"] = [0]*len(clean["Name"])

idx = 0
for name in merged["Name"]:
    
    try: month = merged.loc[merged['Name'] == name, 'sowMonth'].iloc[0]
    except: pass
    
    merged = merged.drop( merged[(merged.Name == name) & (merged.sowMonth == month)].index, axis = 0)

    if month == 1:
        clean.loc[clean['Name'] == name, "sowMonthJan"] = 1
    elif month == 2:
        clean.loc[clean['Name'] == name, "sowMonthFeb"] = 1
    elif month == 3:
        clean.loc[clean['Name'] == name, "sowMonthMar"] = 1
    elif month == 4:
        clean.loc[clean['Name'] == name, "sowMonthApr"] = 1
    elif month == 5:
        clean.loc[clean['Name'] == name, "sowMonthMay"] = 1
    elif month == 6:
        clean.loc[clean['Name'] == name, "sowMonthJun"] = 1
    elif month == 7:
        clean.loc[clean['Name'] == name, "sowMonthJul"] = 1
    elif month == 8:
        clean.loc[clean['Name'] == name, "sowMonthAug"] = 1
    elif month == 9:
        clean.loc[clean['Name'] == name, "sowMonthSep"] = 1
    elif month == 10:
        clean.loc[clean['Name'] == name, "sowMonthOct"] = 1
    elif month == 11:
        clean.loc[clean['Name'] == name, "sowMonthNov"] = 1
    elif month == 12:
        clean.loc[clean['Name'] == name, "sowMonthDec"] = 1
    else:
        pass
    

clean = clean.drop_duplicates()
clean = clean.sort_values(["Name"])

clean.to_csv("merged_total.csv")