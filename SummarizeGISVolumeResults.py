import numpy


class SummarizeGISVolumeResults:
    '''
    Create a summary of GIS channel volume estimates
    '''
    feetToMeters = 0.3048
    cubicFeetToCubicMeters = 0.0283168

    def __init__(self):
        volumeFiles = [
            'dem_ccfb_south_delta_san_joaquin_rvr_2m_20180612_CutFillResults.csv',
            'dem_columbia_cut_2m_20120911_CutFillResults.csv',
            'dem_false_rvr_piper_sl_fisherman_cut_2m_20171109_CutFillResults.csv',
            'dem_montezuma_sl_2m_20180604_CutFillResults.csv',
            'dem_north_delta_2m_20171220_CutFillResults.csv',
            'dem_Sanjoaquin_bradfords_2m_20151204_clip_CutFillResults.csv',
            'dem_turner_cut_2m_20120907_CutFillResults.csv',
            'dem_yolo_merge3_mod_20161202_CutFillResults.csv',
            'dem_delta_10m_20180615_CutFillResults.csv'
        ]

        directory = 'D:/dsm2GisReference/gisChannelVolumes/GeoProOutput/all2mRastersVolumeResults/'

        networkSummaryPath = 'd:/dsm2GisReference/csdpFiles/final/networkSummary20190308.txt'


        gisCutfillSummaryPath = directory + "allGisVolumeResults.txt"
        gisCutfillSummaryStatisticsFilePath = directory + 'gisVolumeSummaryStatistics.txt'

        # volumeFiles = [
        #     'volumeResultsCCFBSouthDeltaSJR.csv',
        #     'volumeResultsColumbia.csv',
        #     'volumeResultsDelta10m.csv',
        #     'volumeResultsFalsePiperFisherman.csv',
        #     'volumeResultsMontezuma.csv',
        #     'volumeResultsNorthDelta.csv',
        #     'volumeResultsSanJoaquinBradfords.csv',
        #     'volumeResultsTurner.csv',
        #     'volumeResultsYolo.csv'
        # ]
        #
        # directory = 'D:/dsm2GisReference/gisChannelVolumes/GeoProOutput/all10mRastersVolumeResults/'

        # dsm2ChanList contains the dsm2 channel numbers, derived from the polygon names.
        # it is the key for the following dictionary objects
        dsm2ChanList = []
        # polygonDict = {}

        # read networkSummary, and map avgWidth and DSM2 volume to channel number.
        csdpAvgWidthFeetDict = {}
        dsm2ChanVolumeDict = {}
        networkSummaryFile = open(networkSummaryPath)
        for line in networkSummaryFile:
            parts = line.split('\t')
            try:
                chan = parts[0]
                int(chan)
                if chan not in dsm2ChanList:
                    dsm2ChanList.append(chan)
                avgWidth = parts[4]
                chanVol = parts[8]
                # test to make sure these are all numeric. if not, exception will be thrown, and line is
                # effectively ignored.
                float(chan)
                float(avgWidth)
                float(chanVol)
                csdpAvgWidthFeetDict.update({chan: avgWidth})
                dsm2ChanVolumeDict.update({chan: chanVol})
            except:
                print "ignoring line "+line

        # dicts of dicts: first key is 'volumeResults" filename.
        #  They Map to dict with key, value = chan, volume/area/demName
        gisVolumeDict = {}
        gisAreaDict = {}
        demDict = {}
        for volumeFile in volumeFiles:
            # polygonDict[volumeFile] = {}
            gisVolumeDict[volumeFile] = {}
            gisAreaDict[volumeFile] = {}
            demDict[volumeFile] = {}
            infile = open(directory+volumeFile)
            i = 0
            for line in infile:
                if i > 0:
                    lineParts = line.split(',')
                    shape = lineParts[0]
                    polygon = lineParts[1]
                    volume = lineParts[2]
                    area = lineParts[3]
                    # polygonArea was supposed to be one of the program outputs, but it's only zeros
                    polygonArea = None
                    dem = None
                    if len(lineParts) == 5:
                        dem = lineParts[4]
                    elif len(lineParts) == 6:
                        dem = lineParts[5]
                    # shape, polygon, volume, area, dem = line.split(',')
                    chan = polygon.replace('_chanpoly', '')
                    if chan not in dsm2ChanList:
                        dsm2ChanList.append(chan)
                    # polygonDict[volumeFile].update({chan: polygon})
                    gisVolumeDict[volumeFile].update({chan: volume})
                    gisAreaDict[volumeFile].update({chan: area})
                    demDict[volumeFile].update({chan: dem})
                i += 1
            infile.close()

        outfile = open(gisCutfillSummaryPath, 'w')
        outfile.write(',Summary,,,,CCFB,,Columbia,,FalsePiperFisherman,,Montezuma,,North Delta,,SanJoaquinBradfords,,Turner,,Yolo,,Delta10m\n')
        outfile.write('DSM2Chan,'
                'Max2mVolume, Stdev2mVolume, Max2mArea, num2mValues,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area,'
                'Volume,Area\n')

        # maps chan to value
        max2mDEMVolumeDict = {}
        stdev2mDEMVolumeDict = {}
        max2mDEMAreaDict = {}
        num2mDEMValuesDict = {}

        tenMDEMVolumeDict = {}
        tenMDEMAreaDict = {}
        for chan in dsm2ChanList:
            twoMVolumeValues = []
            twoMAreaValues = []
            num2mValues = 0
            # calculate average volume and stdev
            for volumeFile in volumeFiles:
                if '10m' not in volumeFile:
                    v = ''
                    a = ''
                    if chan in gisVolumeDict[volumeFile]:
                        v = gisVolumeDict[volumeFile][chan]
                        a = gisAreaDict[volumeFile][chan]
                        if len(v) > 0:
                            try:
                                vol = float(v)
                                area = float(a)
                                if vol > 0:
                                    twoMVolumeValues.append(vol)
                                    twoMAreaValues.append(area)
                                    num2mValues += 1
                            except ValueError:
                                pass
                else:
                    if chan in gisVolumeDict[volumeFile]:
                        v = gisVolumeDict[volumeFile][chan]
                        a = gisAreaDict[volumeFile][chan]
                        if len(v) > 0:
                            try:
                                vol = float(v)
                                area = float(a)
                                if vol > 0:
                                    tenMDEMVolumeDict.update({chan: v})
                                    tenMDEMAreaDict.update({chan: a})
                            except ValueError:
                                pass

            num2mDEMValuesDict.update({chan: num2mValues})

            max2mVolume = -999999
            stdev2mVolume = -999999
            max2mArea = -999999
            if len(twoMVolumeValues) > 0:
                max2mVolume = numpy.max(twoMVolumeValues)
                stdev2mVolume = numpy.std(twoMVolumeValues)
                max2mArea = numpy.max(twoMAreaValues)
            else:
                max2mVolume = ''
                stdev2mVolume = ''
                max2mArea = ''
            line = chan+','+str(max2mVolume)+','+str(stdev2mVolume)+','+str(max2mArea)+','+str(num2mValues)+","
            max2mDEMVolumeDict.update({chan: max2mVolume})
            stdev2mDEMVolumeDict.update({chan: stdev2mVolume})
            max2mDEMAreaDict.update({chan: max2mArea})

            # now add the values
            for volumeFile in volumeFiles:
                v = ''
                a = ''
                if chan in gisVolumeDict[volumeFile]:
                    v = gisVolumeDict[volumeFile][chan]
                if chan in gisAreaDict[volumeFile]:
                    a = gisAreaDict[volumeFile][chan]
                try:
                    if float(v) < 0:
                        v = ''
                    if float(a) < 0:
                        a = ''
                except:
                    v = ''
                    a = ''
                line += v+','+a+','
            outfile.write(line)
            outfile.write('\n')
        outfile.close()

        # now create summary file
        summaryFile = open(gisCutfillSummaryStatisticsFilePath, 'w')
        line = 'DSM2 Chan, 2m Max Vol(m3), 2m Stdev Vol(m3), 2m Max Area(m2), Num 2m Values, 10m Vol(m3), ' \
               'DSM2-2m Vol, DSM2-10m Vol, 2m Vol % diff, 10m Vol % diff, ' \
               '10m Area (m2)m, CSDP Avg Width(m), 2m Width Ratio, 10m Width Ratio, DSM2 Vol(m3)\n'
        summaryFile.write(line)
        for chan in dsm2ChanList:
            twoMWidthRatio = ''
            tenMWidthRatio = ''
            csdpAvgWidthMeters = ''
            if chan in csdpAvgWidthFeetDict:
                csdpAvgWidthMeters = SummarizeGISVolumeResults.feetToMeters * float(csdpAvgWidthFeetDict[chan])
                twoMWidthRatio = csdpAvgWidthMeters/2.0
                tenMWidthRatio = csdpAvgWidthMeters/10.0

            dsm2Volume = ''

            if chan in dsm2ChanVolumeDict:
                dsm2Volume = SummarizeGISVolumeResults.cubicFeetToCubicMeters * float(dsm2ChanVolumeDict[chan])

            else:
                # it's a multi-channel polygon
                # 281_282_295_296_297_301
                # 290-294
                # 438_443_444_450_570_571_574_575
                # 439_440_441_451_452_453_454
                # 448_449_572_573
                if "_" in chan:
                    chanList = chan.split("_")
                    dsm2Volume = 0.0
                    for c in chanList:
                        dsm2Volume += SummarizeGISVolumeResults.cubicFeetToCubicMeters * float(dsm2ChanVolumeDict[c])
                elif "-" in chan:
                    chanList = chan.split("-")
                    dsm2Volume = 0.0
                    i = 0
                    while i<len(chanList)-1:
                        chan1 = int(chanList[i])
                        chan2 = int(chanList[i+1])
                        for c1 in range(chan1, chan2+1):
                            dsm2Volume += SummarizeGISVolumeResults.cubicFeetToCubicMeters * float(dsm2ChanVolumeDict[str(c1)])
                        i += 1

            volDiff2m = ''
            volDiff10m = ''
            volPercentDiff2m = ''
            volPercentDiff10m = ''
            if type(dsm2Volume) == float:
                if chan in max2mDEMVolumeDict:
                    try:
                        volDiff2m = dsm2Volume - float(max2mDEMVolumeDict[chan])
                        volPercentDiff2m = 100.0 * volDiff2m / dsm2Volume
                    except:
                        volDiff2m = ''
                        volPercentDiff2m = ''
                if chan in tenMDEMVolumeDict:
                    try:
                        volDiff10m = dsm2Volume - float(tenMDEMVolumeDict[chan])
                        volPercentDiff10m = 100.0 * volDiff10m/dsm2Volume
                    except:
                        volDiff10m = ''
                        volPercentDiff10m = ''

            line = str(chan)+","+self.getStringValue(max2mDEMVolumeDict, chan)+","+\
                   self.getStringValue(stdev2mDEMVolumeDict, chan)+","+\
                   self.getStringValue(max2mDEMAreaDict, chan)+","
            line += self.getStringValue(num2mDEMValuesDict, chan)+","+self.getStringValue(tenMDEMVolumeDict, chan)+","\
                    +str(volDiff2m)+","+str(volDiff10m)+","+str(volPercentDiff2m)+","+str(volPercentDiff10m)+","+\
                    self.getStringValue(tenMDEMAreaDict, chan)
            line += ","+str(csdpAvgWidthMeters)+","+str(twoMWidthRatio)+","+str(tenMWidthRatio)
            line += ","+str(dsm2Volume)+"\n"
            summaryFile.write(line)

        summaryFile.close()

    def getStringValue(self, dict, key):
        if key in dict:
            return str(dict[key])
        else:
            return ''

SummarizeGISVolumeResults()