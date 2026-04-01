import json
import csv

theMASTERDATA = open("28th-steps-awardData.dat", "r", encoding = "utf-8")
theMASTERDATAJSON = json.load(theMASTERDATA)
csvDATAFILE = open("28th-steps-awardees.csv", "w", newline="", encoding = "utf-8")
csvwriter = csv.writer(csvDATAFILE)
defaultCERTORDERRANKED = ["Best Project", "Second Prize", "Third Prize"]
defaultCERTORDERUNRANKED = "Honorable Mention"
defaultCERTNUMBER = 3
undergradSIGN = "Prof. Kan Min Yen\nVice Dean, Undergraduate Studies\nVice Dean, Academic Affairs"
gradSIGN = "Prof. Chan Mun Choon\nVice Dean, Graduate Studies"
csvwriter.writerow(["Course Names and Heads", "Project Name", "Winner Name", "Award", "Signature"])
print(theMASTERDATAJSON)
for courseCODE, courseELEMENTS in theMASTERDATAJSON.items():
    signer = ""
    courseAwarder = courseELEMENTS["AwardingTitle"]
    isGraduate = courseELEMENTS["IsGraduate"]
    maxAwards = courseELEMENTS["PrizeCount"]
    hm_check = courseELEMENTS["HM"]
    if hm_check:
        awards = [defaultCERTORDERUNRANKED,]
        maxAwards = 1
    else:
        awards = defaultCERTORDERRANKED[:maxAwards]
    if isGraduate:
        signer = gradSIGN
    else:
        signer = undergradSIGN
    
    for order in range(maxAwards):
        position = awards[order]
        winnerNAME = f"{courseCODE} - {position}"
        csvwriter.writerow([courseAwarder, "", winnerNAME, position, signer])
csvDATAFILE.close()