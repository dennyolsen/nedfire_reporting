import pandas as pd

training_csv = './exports/2025TrainingHoursperPersonnelbyCategoryYTD_20260324214142.csv'
standby_csv = './exports/2026SchedulingbyAssignment-PublicView_20260311191908.csv'
incidents_csv = './exports/2026IncidentsbyPersonnel_20260311191904.csv'
drop_names = ["Total, Total", "Schmidtmann, Charlie", "Biscardi, Alec", "Joslin, Andrew", "Moran, Conor", "Wheelock, Glen", "Henrikson, Rik"]
calls = input("Calls YTD:")
minimum = int(calls) / 10

print("Call Credits Minimum: " + str(minimum))

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

# Open File
df_standby = pd.read_csv(standby_csv, usecols=[0,4], header=None, index_col=0)
# Rename Columns
df_standby.index.name = 'Name'
df_standby = df_standby.rename(columns={4: 'Shift_Credits'})
# Drop department total
df_standby = df_standby.drop(index="Total", axis=0)

# Incidents Sum

# Open File
# This line ingests and sets index to name column
# df_incidents = pd.read_csv(incidents_csv, header=None, index_col=0)
df_incidents = pd.read_csv(incidents_csv, header=None)

# Rename Columns
# df_incidents.index.name = 'Name'
# df_incidents = df_incidents.rename(columns={1: 'Incidents'})
# Drop department total
# df_incidents = df_incidents.drop(index="Total", axis=0)

# print(df_incidents[0])
df_incidents['Name'] = df_incidents[0].str.split().apply(lambda x: f"{x[-1]}, {x[0]}")
df_incidents = df_incidents.set_index('Name')
df_incidents = df_incidents.drop(df_incidents.columns[0], axis=1)
df_incidents = df_incidents.rename(columns={1: 'Incidents'})

#Combine

df_combined = df_training.join(df_standby, how='right')
df_combined = df_combined.join(df_incidents, how='right')
df_combined = df_combined.fillna(0)
df_combined['Total_Response_Credits'] = df_combined['Shift_Credits'] + df_combined['Incidents']
for name in drop_names:
    df_combined = df_combined.drop(name)

print(df_combined)

df_combined.to_csv('exports/output.csv')