import glob

def sort_files(directory):
    sched_files = glob.glob("./exports/*SchedulingbyAssignment*.csv")
    if len(sched_files) != 1:
        print("Please check export directory")
        exit
    incidents_files = glob.glob("./exports/*IncidentsbyPersonnel*.csv")
    if len(incidents_files) != 1:
        print("Please check export directory")
        exit
    training_files = glob.glob("./exports/*TrainingHours*.csv")
    if len(training_files) != 1:
        print("Please check export directory")
        exit
    file_dict = {
        "Scheduling" : sched_files, "Incidents" : incidents_files,
        "Training" : training_files}
    return file_dict