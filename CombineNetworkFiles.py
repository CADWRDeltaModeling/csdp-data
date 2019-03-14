class CombineNetworkFiles:
    def __init__(self):
        folder = "d:/dsm2GisReference/csdpFiles/final/"
        files = [
            "group1Channels_2019Calib.cdn",
            "group2Channels_2019Calib.cdn",
            "group3Channels_2019Calib.cdn",
            "group4Channels_2019Calib.cdn"
        ]
        outputFile = open(folder+"delta_2019Calib_navd88.cdn", 'w')

        totalNumElements=0
        dataLines = []
        for f in files:
            networkFile = open(folder+f)
            for line in networkFile:
                if line.startswith(";"):
                    if ";NumElements:" in line:
                        parts = line.split(":")
                        totalNumElements += int(parts[1])
                else:
                    dataLines.append(line)
            networkFile.close()

        outputFile.write(";HorizontalDatum:  UTMNAD83\n")
        outputFile.write(";HorizontalZone:   10\n")
        outputFile.write(";HorizontalUnits:  Meters\n")
        outputFile.write(";VerticalDatum:    NAVD88\n")
        outputFile.write(";VerticalUnits:    USSurveyFeet\n")
        outputFile.write(";Filetype:          network\n")
        outputFile.write(";NumElements:      "+str(totalNumElements)+"\n")
        for line in dataLines:
            outputFile.write(line)
        outputFile.close()

CombineNetworkFiles()