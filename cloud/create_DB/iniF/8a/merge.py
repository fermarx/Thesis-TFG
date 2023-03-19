import pandas as pd

# Create the dataframe we will use later
merged = pd.DataFrame()
# As there are 12 files in total, we create a loop
for file in range(1, 13):
    
    # Read the data from each file
    month_data = pd.read_csv(f"{file}.csv")

    # Get the name and delete the null rows
    name = list(month_data["Name"])
    name = [x for x in name if not(pd.isnull(x)) == True]
    
    # Get the month you have to sow each plant. Depends on the file it is in
    sowMonth = []
    sowMonth.extend([file]*len(name))

    # Create a dicitonary to append it to the file
    data = {"Name": name,
            "sowMonth": sowMonth}
    merged = merged.append(pd.DataFrame(data))

# Create file
merged.to_csv("merged_8a.csv")
