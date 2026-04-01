import pandas as pd

data = pd.read_csv("MASTERDATACSV.csv")
data["AwardingTitle"] = data["Courses"] + " " + data["Title"] + " (Chair: " + data["Instructor"] + ")"
data.set_index("Courses", inplace=True)
data.to_json("28th-steps-awardData.dat", orient="index", indent=4)