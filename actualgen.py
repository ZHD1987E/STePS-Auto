import json
import csv

# Please use this link: https://uvents.nus.edu.sg/api/event/28th-steps/vote
# This is the API endpoint for voting results.
# Copy and paste into results.json and run this script.

defaultCERTORDERRANKED = ["Best Project", "Second Prize", "Third Prize"]
defaultCERTORDERUNRANKED = "Honorable Mention"
undergradSIGN = "Prof. Kan Min Yen\nVice Dean, Undergraduate Studies\nVice Dean, Academic Affairs"
gradSIGN = "Prof. Chan Mun Choon\nVice Dean, Graduate Studies"

with open("results.json", "r", encoding="utf-8") as f_api, \
     open("awardData.dat", "r", encoding="utf-8") as f_master, \
     open("teamData.dat", "r", encoding="utf-8") as f_teams, \
     open("awardees.csv", "w", newline="", encoding="utf-8") as csvDATAFILE, \
     open("winningteams.md", "w", encoding="utf-8") as theWinningTeams:

    apiJSON = json.load(f_api)
    masterJSON = json.load(f_master)
    awardsJSON = json.load(f_teams)

    csvwriter = csv.writer(csvDATAFILE)
    csvwriter.writerow(["Course Names and Heads", "Project Name", "Winner Name", "Award", "Signature"])

    for course in apiJSON:
        courseCODE = course.get("module")
        courseELEMENTS = masterJSON.get(courseCODE)
        if not courseELEMENTS:
            continue

        courseAwarder = courseELEMENTS.get("AwardingTitle") or courseELEMENTS.get("Title") or courseCODE
        isGraduate = courseELEMENTS.get("IsGraduate", False)
        maxAwards = courseELEMENTS.get("PrizeCount", 0)
        hm_check = courseELEMENTS.get("HM", False)

        theWinningTeams.write(f"# {courseAwarder}\n")

        if hm_check:
            awards = [defaultCERTORDERUNRANKED]
            maxAwards = 1
        else:
            awards = defaultCERTORDERRANKED[:maxAwards]

        signer = gradSIGN if isGraduate else undergradSIGN

        courseRESULT = list(course.get("result", {}).items())
        courseRESULT.sort(key=lambda x: x[1], reverse=True)

        ranked = []
        current_group = []
        prev_score = None
        for item in courseRESULT:
            if item[1] != prev_score:
                if current_group:
                    ranked.append(current_group)
                current_group = [item]
                prev_score = item[1]
            else:
                current_group.append(item)
        if current_group:
            ranked.append(current_group)

        for e in range(maxAwards):
            if e >= len(ranked):
                break
            for winner in ranked[e]:
                projectKEY = f"{courseCODE}-{winner[0]}"
                projectNAME = awardsJSON.get(projectKEY, {}).get("name", "")
                theWinningTeams.write(f"**{awards[e]} ({projectKEY})** - {projectNAME}\n\n")
                for member in awardsJSON.get(projectKEY, {}).get("members", []):
                    csvwriter.writerow([courseAwarder, projectNAME, member, awards[e], signer])
