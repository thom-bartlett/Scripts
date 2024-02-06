#!/Library/ManagedFrameworks/Python/Python3.framework/Versions/Current/bin/python3
import requests
import os
import csv

token = os.environ.get("BEARER")
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {token}"
}

def getDirectReport(manager, CSV):
    directceoReports = []
    for row in CSV:
        if row[5] == manager:
            directceoReports.append({row[0]: [row[1],row[3],row[2],row[5]]})
    return directceoReports

def createConnector(start, end, startSnap, endSnap):
    url = "https://api.miro.com/v2/boards/uXjVMveFM10%3D/connectors"

    payload = {
        "startItem": { "id": start, 
                      "snapTo": startSnap, },
        "endItem": { "id": end, 
                    "snapTo": endSnap},
        "shape": "elbowed"
    }

    response = requests.post(url, json=payload, headers=headers)

    #print(response.text)

def createShape(name, x, y, type):
    url = "https://api.miro.com/v2/boards/uXjVMveFM10%3D/shapes"
    if type == "executive":
        shape = "rectangle"
        height = "250"
        width = "250"
        color = "#E6E6E6"
    elif type == "associate vp":
        shape = "round_rectangle"
        height = "200"
        width = "200"
        color = "#FFFFFF"
    elif type == "director":
        shape = "round_rectangle"
        height = "200"
        width = "200"
        color = "#FFFFFF"
    elif type == "nested":
        shape = "round_rectangle"
        height = "150"
        width = "150"
        color = "#FFFFFF"
    else:
        shape = "rectangle"
        height = "150"
        width = "150"
        color = "#FFFFFF"
    payload = {
        "data": { 
            "content": f"<p>{name}</p>", 
            "shape": shape},
        "position": {
            "x": x,
            "y": y
            },
        "style": {
            "fontSize": "25",
            "fillColor": color,
            "textAlignVertical": "middle",
            "textAlign": "center"
        },
    "geometry": {
        "height": height,
        "width": width
    }}
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    responseDict = response.json()
    shapeID = responseDict["id"]
    # connectorX = responseDict["position"]["x"]
    # connectorY = responseDict["position"]["y"]
    #print (f"shapeID = {shapeID}")
    return shapeID
    #return int(shapeID), positionX, positionY

def readCSV():
    with open("/Users/tbartlett/Airtable.csv") as csv_file:
        CSV = list(csv.reader(csv_file, delimiter=","))
        return CSV

def getDirectorWidth(CSV):
    # Top of org chart
    ceo = "pweilerstein@venturewell.org"
    # get executives
    ceoReports = getDirectReport(ceo, CSV)
    print (f"ceo reports = {ceoReports}\n")
    # create dictionary of directors - this is the widest level of chart
    directorWidth = 0
    for i in ceoReports:
        key = list(i.keys())[0]
        print (f"Key = {key}\n")
        reports = getDirectReport(key, CSV)
        print (f"Reports = {reports}")
        directorWidth+=len(reports)
        totalWidth = -abs((directorWidth * 250) / 2)
    return totalWidth, ceoReports

def iterator(ceoReports, CSV, x):
    for i in ceoReports:
        y = 200
        key = list(i.keys())[0]
        directors = getDirectReport(key, CSV)
        groupLength = len(directors)
        execLocation = ((groupLength * 200) / 2) + x - 100
        createShape(key, execLocation, y)
        # totalWidth, y= drawGroup(directors, key, totalWidth, 200, 250)
        # print people who report to a director
        print (f"directors: {directors}")
        for j in directors:
            y = 400
            key = list(j.keys())[0]
            level3 = getDirectReport(key, CSV)
            createShape(key, x, y)
            print (f"Level 3: {level3}")
            # print those that report to a sub-manager
            for k in level3:
                y += 200
                print (f"Y: {y}")
                key = list(k.keys())[0]
                createShape(key, x, y)
                level4 = getDirectReport(key, CSV)
                for l in level4:
                    if len(level4) > 0:
                        y+=200
                        key = list(l.keys())[0]
                        createShape(key, x+25, y)
                        
            x += 250

def recursion(reports, CSV, x, z=0, y=0, startID=0):
    # endID2 = 0
    for i in reports:
        if z == 0:
            y = 350
        elif z == 1:
            y = 700
        else:
            y +=200
        key = list(i.keys())[0]
        reports = getDirectReport(key, CSV)
        groupLength = len(reports)
        text = i[key][0] + " " + i[key][1]
        if i[key][3] == "vharris@venturewell.org":
            y+=200
        if z == 0:
            execLocation = ((groupLength * 250) / 2) + x - 125
            #print (f"execLocation = {execLocation}")
            endID = createShape(text, execLocation, y, "executive")
            createConnector(startID, endID, "bottom", "top")
        elif z == 1:
            if i[key][2] == "director":
                endID = createShape(text, x, y, "director")
            elif i[key][2] == "associate vp":
                y-=200
                endID = createShape(text, x, y-50, "director")
            else:
                y+=200
                endID = createShape(text, x, y, "staff")
            
            createConnector(startID, endID, "bottom", "top")
        elif z == 2:
            if i[key][2] == "director":
                endID = createShape(text, x, y, "director")
                createConnector(startID, endID, "bottom", "top")
            else:
                endID = createShape(text, x, y, "staff")
                createConnector(startID, endID, "left", "left")
        elif z == 3:
            endID = createShape(text, x+25, y, "nested")
            createConnector(startID, endID, "left", "left")
        else:
            endID = createShape(text, x+50, y, "nested")
            createConnector(startID, endID, "left", "left")
        # print (i)
        # print (f"Z: {z}")
        # print (f"Key = {key}")
        # print (f"startID = {startID}")
        # print (f"endID = {endID}")
        x, y = recursion(reports, CSV, x, z+1, y, endID)
        if z == 1:
            x += 250
        # if z >= 2:
        #     startID = endID
    return x, y

# switch to getting name and title
# make items prettier 

def main():
    # read in CSV
    CSV = readCSV()
    # Get list of execs and totalWidth of org chart
    x, ceoReports = getDirectorWidth(CSV)
    print (f"Main X and CEO Reports: {x}  {ceoReports}")
    #print (ceoReports)
    startID = createShape("pweilerstein@venturewell.org President & CEO", 0, 0, "executive")
    # Iterate through and draw executives
    #iterator(ceoReports, CSV, x)
    recursion(ceoReports, CSV, x, 0, 0, startID)       
main()