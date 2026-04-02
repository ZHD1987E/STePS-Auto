import pandas as pd

data = pd.read_csv("MASTERDATACSV.csv")
data["AwardingTitle"] = data["Courses"] + " " + data["Title"] + " (Chair: " + data["Instructor"] + ")"
data.set_index("Courses", inplace=True)
data.to_json("awardData.dat", orient="index", indent=4)