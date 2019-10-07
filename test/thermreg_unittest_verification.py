# Python Script "thermreg_unittest_verification.py"


import argparse as argp
import ast

import mculog_aggregator as aggr
import mculog_parsetypes as pt
import thermreg_aggregation as ta


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


def unittest_generateAggregatedDataSets():
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

    # ALL FILES ARE OPTIONAL, individually taken, HOWEVER: AT LEAST ONE
    # FILE IS MANDATORY.

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
        if parsedLogFileNames[board] == "":
            # nothing to do here
            continue

        message = boardNames[board] + " parsed log name is :" + parsedLogFileNames[board]
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
            print("-:" + record)

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


## developing class definitions for data structures
## which can provide methods to help clarify/cleanup code

class aggregationSpecification(object):
    class logLineVariantMap(object):

        class mappedLogLineVariants(object):
            variantFilter = []
            valueLabels = []
            aggregationLabels = []

            def __init__(self, aggregationMapList):
                if type(aggregationMapList) == list:
                    if len(aggregationMapList) == 2 \
                            and len(aggregationMapList[0]) == 1 \
                            and type(aggregationMapList[1]) == list \
                            and len(aggregationMapList[1][0]) == 3:
                        return
                raise ValueError

            pass

        class mappedLogValueSet(object):
            parsedLineLogSpec = None
            parsedLogLineVariants = []

            def __init__(self, parsedLogSpec, parsedLineVariants):
                self.parsedLineLogSpec = parsedLogSpec
                if type(parsedLineVariants) == list \
                        and len(parsedLineVariants) > 0:
                    for variant in parsedLineVariants:
                        if len(variant) == 3:
                            self.parsedLogLineVariants.append(variant)

                return

            pass

        aggregatedRecordMap = []
        variantValueSets = []

        def __init__(self, aggregatedRecordMap, variantValueSets):
            self.variantValueSets = []
            self.aggregatedRecordMap = aggregatedRecordMap

            for set in variantValueSets:
                thisMappedValueSet = self.mappedLogValueSet(variantValueSets[0],
                                                            variantValueSets[1])
                self.variantValueSets.append(thisMappedValueSet)
            return

    pass


fpgaTempAggregationSpec = aggregationSpecification


def unittest_warningRecord_Aggregate():
    ### this one is not mapped to an aggregator
    ### TODO, differentiate between identical messages
    ### originating on EPM1 and EPM2
    ### use the 'info' command to grap the EPM identity
    ### and **somehow** imprint the identity on the data
    ### to support differentiation

    systemAlertAggregationMapList = [ta.mapped_fpgaWarningValues,
                                     ta.mapped_epmLocalAlertValues]

    global systemAlertAggregator


    systemAlertAggregator = aggr.dataAggregator(ta.systemAlertAggregatedRecord,
                                                ta.systemAlertSyncLabels,
                                                ta.systemAlertAggregationMapList,
                                                ta.systemAlertAggregator_key)

    assert (systemAlertAggregator.configurationValid() == True)
    definedAggregators.append(systemAlertAggregator)
    definedLogMaps.append(systemAlertAggregationMapList)
    definedAggregationRecords.append(ta.systemAlertAggregatedRecord)

    return True


def unittest_fanSpeedRecord_Aggregate():
    global definedAggregators
    global fanStatsAggregator

    fanStatsAggregator = aggr.dataAggregator(ta.fanStatsAggregatedRecordMap,
                                             ta.fanStatsSyncLabels,
                                             ta.fanStatsAggregationMapList,
                                             ta.fanStatsAggregator_key)

    assert (fanStatsAggregator.configurationValid() == True)
    definedAggregators.append(fanStatsAggregator)
    return True


## Build Source Maps for a aggregated temperature record
##


def unittest_tempRecord_Aggregate():
    global definedAggregators

    global fpgaTempAggregateRecordMap

    fpgaTempAggregator = aggr.dataAggregator(ta.fpgaTempAggregateRecordMap,
                                             ta.tempSyncLabels,
                                             ta.tempAggregationMapList,
                                             ta.tempAggregator_key)

    assert (fpgaTempAggregator.configurationValid() == True)
    definedAggregators.append(fpgaTempAggregator)

    ## DEBUGGING
    ## DEFERRING following work to another (later) unittest
    ## return without performing this work.
    return True

    parsedLogFilename = "fpga_putty_log_20190228-182812.groomed.log_Mon_Mar_11_15.11.15_2019.parsed.log"

    parsedLogFile = open(parsedLogFilename, "r")

    for line in parsedLogFile:
        if line in ['\n', "None\n"]:
            continue
        astline = ast.literal_eval(line)
        string_astline = str("::").join(astline)
        print(string_astline)
        tempAggregator.processParsedLogLine(astline)

    return True


import mculog_data_sequence as ds


def isAggregator(x) -> aggr.dataAggregator:
    return x


def isSequencedData(x) -> ds.sequencedData:
    return x


def unittest_showDatabase():
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


def unittest_generateFpgaDataSet():
    # generate a dataset for each of the record types
    # TODO generate a dataset drawing from all record types
    global tempAggregator

    parsedLogFilename = "fpga_putty_log_20190228-182812.groomed.log_Mon_Mar_11_15.11.15_2019.parsed.log"
    parsedLogFile = open(parsedLogFilename, "r")

    for line in parsedLogFile:
        if line in ['\n', "None\n"]:
            continue
        astline = ast.literal_eval(line)
        print("-:" + line)
        fpgaTempAggregator.processParsedLogLine(astline)

    return True


test_list = [unittest_tempRecord_Aggregate,
             unittest_fanSpeedRecord_Aggregate,
             unittest_warningRecord_Aggregate,
             unittest_generateAggregatedDataSets,
             unittest_showDatabase]


def main():
    for test in test_list:
        result = test()
        assert result == True
    return


if __name__ == "__main__":
    main()
