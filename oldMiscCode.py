def csvtoJson():
     with open("/Users/tbartlett/Downloads/orgchart.csv") as csv_file:
        directoryDict = {}
        CSV = list(csv.reader(csv_file, delimiter=","))
        ceo = "pweilerstein@venturewell.org"
        ceoReports = getDirectReport(ceo, CSV)
        directoryDict.update({ceo: ceoReports})
        # get first level of ceoReports (directors)
        for i in directoryDict[ceo]:
            # get the current key
            key = list(i.keys())[0]
            ceoReports = getDirectReport(key, CSV)
            # update master list
            i.update({key: ceoReports})
            # get second level (managers)
            for j in i[key]:
                key = list(j.keys())[0]
                ceoReports = getDirectReport(key, CSV)
                j.update({key: ceoReports})
                # get third level (individual staff)
                for k in j[key]:
                    key = list(k.keys())[0]
                    ceoReports = getDirectReport(key, CSV)
                    if len(ceoReports) > 0:
                        k.update({key: ceoReports})
        #print(json.dumps(directoryDict, indent=4))   
        return directoryDict

def drawGroup(reportList, manager, x, y, xSpace, ySpace=0):
        if type(reportList) is list:
            for i in reportList:
                key = list(i.keys())[0]
                createShape(key, x, y)
                #createConnector(shapeID[1], shapeID[0])
                x+= xSpace
                y+=ySpace
        else:
            createShape(reportList,x,y)
        return x, y

def getNext(shapeID, x, y, director=0,):
    lineCount = 0
    ceoReports = {}
    with open("/Users/tbartlett/Downloads/Miro_OrgChart_Template.csv") as csv_file:
        CSV = csv.reader(csv_file, delimiter=",")
        if director == 0:
            for row in CSV:
                if lineCount == 0:
                    print(f'Column names are {", ".join(row)}')
                    lineCount += 1
                else:
                    if row[2] == "President & CEO":
                        shapeID[1], positionX, positionY = createShape(row[0], row[2], row[1])
        else:
            for row in CSV:
                if row[7] == director:
                    ceoReports[row[0]] = row[2], row[5], row[1]
                    print(ceoReports)
            for key in ceoReports:
                print(shapeID)
                shapeID[0], positionX, positionY = createShape(key, ceoReports[key][0], ceoReports[key][1], x, y)
                createConnector(shapeID[1], shapeID[0])
                print(x)
                if x < 0:
                    x = abs(x)
                else:
                    x = -abs(x)
                    x+=-500
    return shapeID, ceoReports, x, y


def readDirectory(directory, x, y, z=0):
    global directorCount
    print (z)
    if z == 3:
            directorCount += 1
    for i in directory:
        # top level person
        
        if type(directory) is dict and len(directory) == 1:
            # print(json.dumps(directory, indent=4))
            #createShape(i, x, y)
            readDirectory(directory[i], 0, 200, z+1)
        else:
            key = list(i.keys())[0]
            # print(directory)
            print(key, x, y)
            # print(i)
            #createShape(key, x, y)
            #print(json.dumps(i, indent=4))
            readDirectory(i[key], x, y+200, z+1)
            x+=300