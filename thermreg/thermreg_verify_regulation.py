import mculog_utility as util
import thermreg_event_monitor as evtmon
import thermreg_registry as thregistry

#
# thermreg_verify_regulation.py
# Drive extraction of thermal sensor and control data
# from the Thermal Regulation logs for FPGA, EPM1, EPM2,
# and analyze data for adherence to system design constraints.
#

import argparse as argp
import ast

import mculog_aggregator as aggr
import mculog_parsetypes as pt
import thermreg_aggregation as ta
import collections as coll
import mculog_utility as mu
import thermreg_registry as thregistry

import csv

def getRecordFromParsedLogLine(line):
    bracketLevel = 0
    elementCount = 0
    recordString = str("")

    prevChar = None

    for char in line:
        if char == '[':
            bracketLevel += 1
            recordString += "["
            freshOpenBracket = True

        elif char == ']':
            bracketLevel -= 1
            if prevChar == ']':
                # do nothing
                pass
            else:
                # recordString+=
                # expressString()
                # expressCloseBracket()
                pass

        elif char == ',':
            # expressString()
            # expressComma()
            pass
        else:
            # expressChar()
            pass

        prevChar = char
        continue


def processVerification(verifier, parsedLogFile, outputFilename):
    for line in parsedLogFile:
        if '[' not in line:
            # discard junk lines
            continue
        lineRecord = ast.literal_eval(line)
        verifier.simpleRecordInput(lineRecord)
    return False


##
## Test the creation of a data sequence with temperatures
## for the fpga board, including epm max temps
## a log file is prepared with output parsed by the log parser
## read and drive the lines of parsed information through the
## ThermalVerifier class, and verify that the data sequence
## is formed and useable
FPGA_INDEX = 0
EPM1_INDEX = 1
EPM2_INDEX = 2
DEVKIT_INDEX = 3

parsedLogFileNames = []
parsedLogFiles = []
timestampedOutputFileNames = []
dataSetNames = []
dataSetFileNames = []
dataSetFiles = []

global definedAggregators
global definedLogMaps
global definedAggregationRecords
global unittest_argparser

definedLogMaps = []
definedAggregators = []
definedAggregationRecords = []
unittest_argparser = None

global fpgaTempAggregationMapList

global fpgaTempAggregateRecordMap

fanStatusAggregator = None
systemAlertAggregator = None
fpgaTempAggregator = None
epmBoardAggregator = None


def initGlobalData():
    global parsedLogFileNames
    global parsedLogFiles
    global dataSetNames
    global dataSetFileNames
    global dataSetFiles
    global definedAggregators
    global definedLogMaps
    global definedAggregationRecords

    parsedLogFileNames = 4 * [""]
    parsedLogFiles = 4 * [None]
    dataSetNames = 4 * [""]
    dataSetFileNames = 4 * [""]
    dataSetFiles = 4 * [None]
    #    definedAggregators = 4 * [None]
    definedLogMaps = 4 * [None]
    definedAggregationRecords = 4 * [None]
    return


def generateAggregatedDataSets():
    ## 0. This unittest must succeed the tests that
    ##      instantiate all aggregators and dependent
    ##      dataSequencers.
    ##
    ## 1. identify log files presented
    ## 2. open log files presented (verify files)
    ## 2.... each file comes from a specific target board
    ## 3. process log files through aggregation
    ## TODO 4. manage sequencing of various files (time synching)
    ##
    # start with clean globals for
    # files and data set names
    initGlobalData()

    # process / parse command line input
    unittest_argparser = argp.ArgumentParser(description="AVEPM UnitTest: ThermalVerifier")

    # EACH FILE IS OPTIONAL
    # COLLECTIVELY, HOWEVER: AT LEAST ONE FILE SPECIFICATION IS REQUIRED

    unittest_argparser.add_argument("--fpga_plog", dest="fpga_parsed_log", help="AVFPGA parsed log pathname",
                                    metavar="FILE")
    unittest_argparser.add_argument("--epm1_plog", dest="epm1_parsed_log",
                                    help="AVEPM Configuration 1 parsed log pathname", metavar="FILE")
    unittest_argparser.add_argument("--epm2_plog", dest="epm2_parsed_log",
                                    help="AVEPM Configuration 2 parsed log pathname", metavar="FILE")
    unittest_argparser.add_argument("--devkit_plog", dest="devkit_parsed_log", help="TC297-DEVKIT parsed log pathname",
                                    metavar="FILE")
    #    parser.add_argument("--unknown", dest="unknown_parsed_log", help="unknown target, ID is TBD", metavar="FILE")
    #   TODO a parsing tool that identifies the target board based on the log content
    #   could be fun *and* useful

    unittest_args = unittest_argparser.parse_args()

    boardSet = [FPGA_INDEX, EPM1_INDEX, EPM2_INDEX, DEVKIT_INDEX]
    boardNames = ["FPGA", "EPM1", "EPM2", "DEVKIT"]

    parsedLogFileNames[FPGA_INDEX] = unittest_args.fpga_parsed_log
    parsedLogFileNames[EPM1_INDEX] = unittest_args.epm2_parsed_log
    parsedLogFileNames[EPM2_INDEX] = unittest_args.epm2_parsed_log
    parsedLogFileNames[DEVKIT_INDEX] = unittest_args.devkit_parsed_log

    # fpga filename is mandatory, epm1 & 2 filenames optional
    # open defined files
    import time
    timeString = time.asctime(time.localtime(time.time()))
    sequenceID = timeString.replace(' ', '_')
    sequenceID = sequenceID.replace(':', '.')

    nullStringList = 4 * [""]
    noneTypeList = 4 * [None]

    # use list comprehension to find list of filenames specified
    definedParsedLogFiles = [item for item in parsedLogFileNames if item != ""]
    if len(definedParsedLogFiles) >= 1:
        # we have a defined log file
        pass
    else:
        # no log files are defined... Help!
        print("No parseable files specified\r\n")
        unittest_argparser.print_usage()
        unittest_argparser.print_help()
        return True

    for board in boardSet:
        if definedParsedLogFiles[board] == None:
            # nothing to do here
            continue

        message = boardNames[board] + " parsed log name is :" + definedParsedLogFiles[board]
        print(message)

        if len(parsedLogFileNames[board]) == 0:
            # log filename is mandatory - fail
            unittest_argparser.print_help()
            exit(-1)

        elif board == FPGA_INDEX:
            useFPGA = True
            pass
        elif board == EPM1_INDEX:
            useEPM1 = True
            pass
        elif board == EPM2_INDEX:
            useEPM2 = True
            pass
        elif board == DEVKIT_INDEX:
            useDEVKIT = True
            pass

        try:
            thisFile = open(parsedLogFileNames[board], 'r')

        except Exception as e:
            print(e)
            print("cannot open " + parsedLogFileNames[board])
            exit(-1)
            return False  # this line to prevent warning on next line

        parsedLogFiles[board] = thisFile

        ## process parsedLogfile of a single board
        ## through aggregation by each defined
        ## dataSequencer/aggregator

        for record in thisFile:
            if record[0][0] == pt.error_ParseErrorReport:
                # do not process parser error reports
                continue

            if record in ['\n', 'None\n']:
                # do not process empty lines
                continue

            astRecord = ast.literal_eval(record)
            #            astString = util.simple_list_to_string(astRecord)
            # print("-:" + record)

            global definedAggregators

            aggregator: aggr.dataAggregator
            for aggregator in definedAggregators:
                # record is to be parsed by each aggregator
                # TODO make multi-dataSequencer aggregation most efficient
                aggregator.processParsedLogLine(astRecord)
                # TODO ! Consider whether to ignore result of
                # TODO ..each record's aggregation attempts
                continue
            continue

        return True

    return (False)






def warningRecord_Aggregate():
    ### this one is not mapped to an aggregator
    ### TODO, differentiate between identical messages
    ### originating on EPM1 and EPM2
    ### use the 'info' command to grap the EPM identity
    ### and **somehow** imprint the identity on the data
    ### to support differentiation


    global systemAlertAggregator

    fpgaRegistry = thregistry.thermregRegistryKeyedList.getEntry(thregistry.fpgaRegistry_key)

    systemAlertAggregator = aggr.dataAggregator(ta.systemAlertAggregatedRecord,
                                                ta.systemAlertStorageControl,
                                                ta.systemAlertAggregationMapList,
                                                ta.systemAlertAggregator_key,
                                                fpgaRegistry)

    assert (systemAlertAggregator.configurationValid() == True)
    definedAggregators.append(systemAlertAggregator)
    definedLogMaps.append(ta.systemAlertAggregationMapList)
    definedAggregationRecords.append(ta.systemAlertAggregatedRecord)
    return True


def fanSpeedRecord_Aggregate():
    global definedAggregators
    global fanStatsAggregator

    fpgaRegistry = thregistry.thermregRegistryKeyedList.getEntry(thregistry.fpgaRegistry_key)

    fanStatsAggregator = aggr.dataAggregator(ta.fanStatsAggregatedRecordMap,
                                             ta.fanStatsStorageControl,
                                             ta.fanStatsAggregationMapList,
                                             ta.fanStatsAggregator_key,
                                             fpgaRegistry)

    assert (fanStatsAggregator.configurationValid() == True)
    definedAggregators.append(fanStatsAggregator)
    return True


def epmBoardRecord_Aggregate():
    global definedAggregators
    global epmBoardAggregator

    epmRegistry = thregistry.thermregRegistryKeyedList.getEntry(thregistry.epmRegistry_key)

    epmBoardAggregator = aggr.dataAggregator(ta.epmBoardAggregationRecord,
                                             ta.epmBoardStorageControl,
                                             ta.epmBoardAggregationMapList,
                                             ta.epmBoardAggregator_key,
                                             epmRegistry)

    assert (epmBoardAggregator.configurationValid() == True)
    definedAggregators.append(epmBoardAggregator)
    return True


## Build Source Maps for a aggregated temperature record
##


## Build Source Maps for a aggregated temperature record
##


def tempRecord_Aggregate():
    global definedAggregators

    global fpgaTempAggregateRecordMap

    global thermregRegistryKeyedList

    fpgaRegistry = thregistry.thermregRegistryKeyedList.getEntry(thregistry.fpgaRegistry_key)

    fpgaTempAggregator = aggr.dataAggregator(ta.fpgaTempAggregateRecordMap,
                                             ta.fpgaTempStorageControl,
                                             ta.tempAggregationMapList,
                                             ta.tempAggregator_key,
                                             fpgaRegistry)

    assert (fpgaTempAggregator.configurationValid() == True)
    definedAggregators.append(fpgaTempAggregator)
    return True



import mculog_data_sequence as ds


def isAggregator(x) -> aggr.dataAggregator:
    return x


def isSequencedData(x) -> ds.sequencedData:
    return x



def setupRegistries():
    return thregistry.buildRegistries()


def showDatabase():
    # display aggregated records from dataSequence objects
    result = False

    for index in enumerate(definedAggregators, 0):

        thisAggregator = isAggregator(index[1])
        if thisAggregator == fpgaTempAggregator:
            print("FPGA TEMPERATURE AGGREGATION")
            pass

        elif thisAggregator == fanStatusAggregator:
            print("FAN STATUS AGGREGATION")
            pass

        elif thisAggregator == systemAlertAggregator:
            print("SYSTEM ALERT AGGREGATOR")
            pass

        elif thisAggregator == epmBoardAggregator:
            print ("EPM BOARD AGGREGATOR")
            pass

        else:
            print("NO IDEA WHAT THIS IS")

        database = thisAggregator.getDatabase()
        #        database = isSequencedData(database)

        if database.getDatumCount() == 0:
            print("Skipping Empty Database")
            continue

        datum = database.getFirstDatum()
        # display record item labels
        # display all records in database
        recordLabelList = thisAggregator.getRecordLabelList()
        labelListString = repr(recordLabelList)
        print("\r\n\n\nAGGREGATED RECORD LABELS:\r\n" + labelListString)

        recordCount = database.getDatumCount()
        recordIndex = 0
        while recordIndex < recordCount:
            if recordIndex % 10 == 0:
                print(":::"+ labelListString)

            if recordIndex == 0:
                Record = database.getFirstDatum()
            else:
                Record = database.getNextDatum()

            valueString = repr(Record)
            print(str(recordIndex) + ": " + valueString)

            recordIndex += 1
            continue
        # if one database was nontrivial
        # then we have a success
        result = True

        continue

    return result




def NullItemPresent(thisList):
    ## Measure whether undefined data is in a record

    for item in thisList:
        if item == pt.NULL_ITEM:
            return True

    return False

def all_same( itemlist ):
    return all( map(lambda x: x == itemlist[0], itemlist))

def preProcessThermalData():
    ## create dataSequences with data records as follows
    ## [ MaxTemp(a2..a8), MaxTemp(a0), MaxTemp(epm1..epm2), fanspeed(a2..a6), fanspeed(a0)]
    ## [ alerts and warnings ] + [ synthetic events]
    ## synthetic events: fanspeedChange(a0), fanspeedChange(a2..a8)
    ## synthetic events: pwmChange(a0), pwmChange(a2..a8)

    tempAggregator = fanAggregator = systemAlertDatabaseAggregator = None
    tempRecordLabels = fanRecordLabels = systemAlertRecordLabels = None
    tempDatabase = fanDatabase = systemAlertDatabase = None

    for index in enumerate(definedAggregators, 0):

        thisAggregator = isAggregator(index[1])
        if thisAggregator.getKey() == ta.tempAggregator_key:
            tempAggregator = thisAggregator
            tempDatabase = tempAggregator.getDatabase()
            tempRecordLabels = thisAggregator.getRecordLabelList()

        elif thisAggregator.getKey() == ta.fanStatsAggregator_key:
            fanAggregator = thisAggregator
            fanDatabase = fanAggregator.getDatabase()
            fanRecordLabels = thisAggregator.getRecordLabelList()

        elif thisAggregator.getKey() == ta.systemAlertAggregator_key:
            systemAlertAggregator = thisAggregator
            systemAlertDatabase = systemAlertAggregator.getDatabase()
            systemAlertRecordLabels = thisAggregator.getRecordLabelList()



        if tempDatabase != None and fanDatabase != None and systemAlertDatabase != None:
            break

        continue

    ## Databases for temp status and fan status are in hand
    ## now build a history of system and heatsink max temps
    ## and system and heatsink fan stats

    ## databases with raw data
    tempRecordCount = tempDatabase.getDatumCount()
    fanStatsRecordCount = fanDatabase.getDatumCount()
    systemAlertRecordCount = systemAlertDatabase.getDatumCount()

    recordCounts = [ tempRecordCount, fanStatsRecordCount, systemAlertRecordCount ]

    ## database with refined data
    thermalRegulationHistory = ds.sequencedData(ds.compareNumber)

    if not all_same(recordCounts):
        print("Fan/Temp databases have different record counts")

    print("temp record count : "+ str(tempRecordCount))
    print("fanStats record count : " + str(fanStatsRecordCount))
    print("systemAlert record count : " + str(systemAlertRecordCount))




    a0LocalIndex =  tempRecordLabels.index("a0l")
    a0RemoteIndex = tempRecordLabels.index("a0r")
    a0TempIndices = [a0LocalIndex, a0RemoteIndex]

    epm1MaxTempIndex = tempRecordLabels.index("epm1Max")
    epm2MaxTempIndex = tempRecordLabels.index("epm2Max")
    epmMaxTempIndices = [epm1MaxTempIndex, epm2MaxTempIndex]

    a0FanPWMIndex = fanRecordLabels.index("a0pwm")

    a0FanTachIndex = fanRecordLabels.index("a0tach")

    a2468FanPWMIndices = [ fanRecordLabels.index("a2pwm"),
                           fanRecordLabels.index("a4pwm"),
                           fanRecordLabels.index("a6pwm"),
                           fanRecordLabels.index("a8pwm")]

    a2468FanTachIndices = [fanRecordLabels.index("a2tach"),
                           fanRecordLabels.index("a4tach"),
                           fanRecordLabels.index("a6tach"),
                           fanRecordLabels.index("a8tach")]


    evtmon.tempSystemHistory = ["a0MaxTemp", "sysMaxTemp", "epm1MaxTemp", "epm2MaxTemp"]
    evtmon.fanControlHistoryLabels = ["a0TachVal", "a0Pwm", "systemTach", "systemPwm"]

    ## Build pre-processed data lists

    ordinal = 0
    tempMaxOrdinal = tempDatabase.getDatumCount()  -  1
    fanMaxOrdinal = fanDatabase.getDatumCount() - 1
    systemAlertMaxOrdinal = systemAlertDatabase.getDatumCount() - 1

    maxOrdinal = min(tempMaxOrdinal, fanMaxOrdinal, systemAlertMaxOrdinal)

    Ordinal = 0

    while Ordinal <= maxOrdinal:

        # build a dataSequence or database of the derived key system
        # temperature and control variables

        tempRecord = tempDatabase.getDatumByOrdinal(ordinal)
        fanRecord = fanDatabase.getDatumByOrdinal(ordinal)
        alertRecord = systemAlertDatabase.getDatumByOrdinal(ordinal)

        if fanRecord == None or tempRecord == None or alertRecord == None:
            ## when one database is empty, we're done
            break

        fpgaTemps = util.listFromIndices(tempRecord, a0TempIndices)
        fpgaTach = fanRecord[a0FanTachIndex]
        fpgaPwm = fanRecord[a0FanPWMIndex]


        epmMaxTemps = util.listFromIndices(tempRecord, epmMaxTempIndices)
        a2468PwmSet = util.listFromIndices(fanRecord, a2468FanPWMIndices)
        a2468FanTachSet = util.listFromIndices(fanRecord, a2468FanTachIndices)

        #if NullItemPresent(a2468PwmSet):
        #    print("sparse 'a2468PwmSet' discarded")
        #    continue

        ## Named Tuples facilitate readable key variable access

        TempRegulationHistory = coll.namedtuple('TempRegulationHistory',
                    'a0MaxTemp,sysMaxTemp,epm1MaxTemp,epm2MaxTemp,a0Tach,a0Pwm,systemTach,systemPwm')

        tempRegHistory = TempRegulationHistory( a0MaxTemp = mu.smartMax(fpgaTemps),
                                                sysMaxTemp = mu.smartMax(tempRecord),
                                                epm1MaxTemp = str(epmMaxTemps[0]),
                                                epm2MaxTemp = str(epmMaxTemps[1]),
                                                a0Tach = str(fpgaTach),
                                                a0Pwm = str(fpgaPwm),
                                                systemTach=mu.smartMax(a2468FanTachSet),
                                                systemPwm=mu.smartMax(a2468PwmSet))

        thermalRegulationHistory.appendSequencedDatum(ordinal, tempRegHistory)

        if tempDatabase.getDatumIndex() + 1 == tempDatabase.getDatumCount():
            ## the last record has been taken
            break

        ordinal+=1
        continue

    ## parse through max temps and fan speed controls to determine compliance.
    ## find when system max temp rises or falls through a threshold

    ordinal = 0
    maxOrdinal = thermalRegulationHistory.getDatumCount()

    while ordinal < maxOrdinal:
        if ordinal == 0:
            tempRegHistory = thermalRegulationHistory.getFirstDatum()
        else:
            tempRegHistory = thermalRegulationHistory.getNextDatum()


        print ( repr(tempRegHistory))
        #print(  'a0MaxTemp %d  sysMaxTemp %d  epm1MaxTemp %s  epm2MaxTemp %s  a0Tach %s  a0Pwm %s  systemTach %d systemPwm %d' % tempRegHistory)

        ## Track changes in temperatures
        ## detect threshold crossing/leaving for events

        ## first event type to detect is epm1MaxTemp
        ## since an alert is in our test log file


        ordinal+=1

        if ordinal == maxOrdinal:
            break
        continue

    return True

task_list = [setupRegistries,
             tempRecord_Aggregate,
             fanSpeedRecord_Aggregate,
             warningRecord_Aggregate,
             epmBoardRecord_Aggregate,
             generateAggregatedDataSets,
             preProcessThermalData]
             #showDatabase



def main():
    for task in task_list:
        result = task()
        assert (result == True)
    return

if __name__ == "__main__":
        main()
