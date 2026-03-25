import pandas as pd

training_csv = './exports/2025TrainingHoursperPersonnelbyCategoryYTD_20260324214142.csv'
standby_csv = './exports/2026SchedulingbyAssignment-PublicView_20260311191908.csv'
incidents_csv = './exports/2026IncidentsbyPersonnel_20260311191904.csv'

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
df_incidents = pd.read_csv(incidents_csv, header=None, index_col=0)
# Rename Columns
df_incidents.index.name = 'Name'
df_incidents = df_incidents.rename(columns={1: 'Incidents'})
# Drop department total
df_incidents = df_incidents.drop(index="Total", axis=0)
for i in df_incidents.index:
    print("HELLO")

#Combine

df_combined = df_training.join(df_standby, how='right')
df_combined = df_combined.fillna(0)

print(df_incidents)
print(df_combined)

df_combined.to_csv('exports/output.csv')