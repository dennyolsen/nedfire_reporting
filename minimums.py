import pandas as pd
from datetime import date, datetime
import os
import glob

directory =  os.path.join(".", "exports")

# This function finds files in the specified directory

def sort_files(directory):
    sched_files = glob.glob(os.path.join(directory, "*SchedulingbyAssignment*.csv"))
    if len(sched_files) != 1:
        print("Please check export directory")
        exit
    incidents_files = glob.glob(os.path.join(directory, "*IncidentsbyPersonnel*.csv"))
    if len(incidents_files) != 1:
        print("Please check export directory")
        exit
    # training_files = glob.glob("./exports/*TrainingHours*.csv")
    training_files = glob.glob(os.path.join(directory, "*TrainingHours*.csv"))
    if len(training_files) != 1:
        print("Please check export directory")
        exit
    file_dict = {
        "Scheduling" : sched_files, "Incidents" : incidents_files,
        "Training" : training_files}
    return file_dict


files = sort_files(directory)

training_csv = files["Training"][0]
print("Training hours file: " + training_csv)
standby_csv = files["Scheduling"][0]
print("Shift hours file: " + standby_csv)
incidents_csv = files["Incidents"][0]
print("Response totals file: " + incidents_csv)

# Restrict roster to volunteer FFs
drop_names = [
    "Total, Total", "Schmidtmann, Charlie", "Biscardi, Alec", "Joslin, Andrew",
    "Moran, Conor", "Wheelock, Glen", "Henrikson, Rik", "Faes, Nick",
    "(NULL), (NULL)", "Blumen, Jason", "Lucas, Eric", "Snyder, Sherry"]

# Input number of calls YTD and calculate minimum at 10% of that
calls = input("Calls YTD:")
minimum = int(calls) / 10

print("Call Credits Minimum: " + str(minimum))

# Date Math
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
today = date.today()
new_year = date(today.year, 1, 1)
delta = today - new_year
days_elapsed = delta.days
print("Days elapsed YTD: " + str(days_elapsed))

# Note that scores above 1 are passing
print("***Note that scores >1 indicate minimum fulfillment***")

# Training Hours Sum

# Open File
df_training = pd.read_csv(training_csv, sep = ",")
# Handle spaces in column names
df_training.columns = df_training.columns.str.replace(" ", "_")
# Rename column
df_training.columns = df_training.columns.str.replace("Total", "Training_Hours_Total")
# Drop Category column
df_training = df_training.drop('Category_Name', axis=1)
# Drop department total
df_training = df_training[df_training.Attendee_Name != "Total"]
# Pivot on training hours (sum)
df_training = df_training.groupby('Attendee_Name').sum()
df_training.index.name = 'Name'
# Handle Grace
df_training.rename(index={'Gude, Margaret Grace':'Gude, Margaret'},inplace=True)

# Standby Hours Sum

# Open file
df_standby = pd.read_csv(standby_csv, usecols=['Last, First','Response Credits for Stand-By Hours'])
# Rename columns
df_standby = df_standby.rename(columns={'Response Credits for Stand-By Hours': 'Shift_Credits', 'Last, First': 'Name'})
# Set index
df_standby = df_standby.set_index('Name')
# Drop department total
df_standby = df_standby.drop(index="Total", axis=0)

# Incidents Sum

# Open File
df_incidents = pd.read_csv(incidents_csv, usecols=['Personnel Name', "Total Responses"])
# Convert name to last, first
df_incidents['Name'] = df_incidents['Personnel Name'].str.split().apply(lambda x: f"{x[-1]}, {x[0]}")
# Set inxex
df_incidents = df_incidents.set_index('Name')
# Drop old name
df_incidents = df_incidents.drop('Personnel Name', axis=1)
# Fix column name
df_incidents = df_incidents.rename(columns={'Total Responses': 'Incidents'})

#Combine

# Combine various dataframes
df_combined = pd.merge(df_training, df_standby, on='Name', how='outer')
df_combined = pd.merge(df_combined, df_incidents, on='Name', how='outer')
# Convert null values to 0
df_combined = df_combined.fillna(0)
# Total response credits math
df_combined['Total_Response_Credits'] = df_combined['Shift_Credits'] + df_combined['Incidents']
# Response score math, based on YTD calls at beginning of execution
df_combined['Response_Score'] = round(df_combined['Total_Response_Credits'] / minimum, 2)
# Training score math, based on days elapsed YTD and 64 hour annual minimum
df_combined['Training_Score'] = round(df_combined['Training_Hours_Total'] / (64 * (days_elapsed / 365)), 2)
# Drop miscellaneous officers, chief PRNs, null values from reporting
for name in drop_names:
    df_combined = df_combined.drop(name)

# Print results
print(df_combined)

# Save to csv
df_combined.to_csv(os.path.join(".", "output", "NFPD_FF_Minimums_Report_" + timestamp + ".csv"))