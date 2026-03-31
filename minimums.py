import pandas as pd
from datetime import date, datetime

training_csv = './exports/2025TrainingHoursperPersonnelbyCategoryYTD_20260331194156.csv'
standby_csv = './exports/2026SchedulingbyAssignment-PublicView_20260331194151.csv' #New
incidents_csv = './exports/IncidentsbyPersonnel-PublicView_20260331194218.csv' #New
drop_names = ["Total, Total", "Schmidtmann, Charlie", "Biscardi, Alec", "Joslin, Andrew", "Moran, Conor", "Wheelock, Glen", "Henrikson, Rik", "Faes, Nick", "(NULL), (NULL)"]
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
print("Days elapsed: " + str(days_elapsed))

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
df_standby = pd.read_csv(standby_csv, usecols=['Last, First','Response Credits for Stand-By Hours'])

# Rename Columns

df_standby = df_standby.rename(columns={'Response Credits for Stand-By Hours': 'Shift_Credits', 'Last, First': 'Name'})
df_standby = df_standby.set_index('Name')
# Drop department total
df_standby = df_standby.drop(index="Total", axis=0)

# Incidents Sum

# Open File
# This line ingests and sets index to name column
# df_incidents = pd.read_csv(incidents_csv, header=None, index_col=0)
df_incidents = pd.read_csv(incidents_csv, usecols=['Personnel Name', "Total Responses"])



# Rename Columns
# df_incidents.index.name = 'Name'
# df_incidents = df_incidents.rename(columns={1: 'Incidents'})
# Drop department total
# df_incidents = df_incidents.drop(index="Total", axis=0)

# print(df_incidents[0])
df_incidents['Name'] = df_incidents['Personnel Name'].str.split().apply(lambda x: f"{x[-1]}, {x[0]}")
df_incidents = df_incidents.set_index('Name')
df_incidents = df_incidents.drop('Personnel Name', axis=1)
df_incidents = df_incidents.rename(columns={'Total Responses': 'Incidents'})

#Combine

df_combined = df_training.join(df_standby, how='right')
df_combined = df_combined.join(df_incidents, how='right')
df_combined = df_combined.fillna(0)
df_combined['Total_Response_Credits'] = df_combined['Shift_Credits'] + df_combined['Incidents']
df_combined['Response_Score'] = df_combined['Total_Response_Credits'] / minimum
df_combined['Training_Score'] = df_combined['Training_Hours_Total'] / (64 * (days_elapsed / 365))
for name in drop_names:
    df_combined = df_combined.drop(name)

print(df_combined)

df_combined.to_csv(f'output/output_{timestamp}.csv')