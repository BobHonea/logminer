#!/usr/bin/python
#
#  thermreg_main.py
#
#   reads log file names specified by board-type from command line
#   for each log file, registers parser-symbolic information
#   for each log file, drives log text lines through parser
#   output of log parser goes to a file, or to data record aggregation
#


import argparse as argp

import mculog_logparser as mcuparse
import mculog_parsetypes as mcuptype
import mculog_utility as mcutil
import thermreg_log_specification as tlspec
import thermreg_registry as thregistry






import mculog_utility as util


def processLog(logParse, logFile, parsedOutputFilePathname):
    logParse.startLogSession()
    processed_logs = []
    ordinal = 1
    try:
        parsedOutputFile = open(parsedOutputFilePathname, 'w')

    except FileExistsError as fe:
        print(fe)
        raise FileExistsError

    for lineNo, line in enumerate(logFile, 1):
        timestamp=None

        if line[0] == '[' and ']' :
            # time is of format <'['><number[seconds.milliseconds]><']'>
            # TODO: implement recognition of various time formats

            timeLen = 12
            if len(line) > timeLen and line[timeLen - 1] == ']':
                # line is nontrivial and has timestamp
                # capture timestamp then recast line to
                # begin after the timestamp
                logTime = line[1:timeLen - 1]
                line = line[timeLen+1:]

        ## DO NOTHING WITH TIMESTAMP FOR THE PRESENT
        ## TODO: imiplement time-stamping from raw log
        ## TODO:through LogParser through to Aggregation and
        ## TODO: the Aggregation Records themselves... with
        ## TODO: the record stamped for a single timestamp or
        ## TODO: a timestamp range.
        ## INTENTION: use a timestamp, if present
        ## INTENTION: if not, use an ordinal
        ## INTENTION: increment ordinal ONLY when a line parse succeeds
        ## INTENTION: ordinal of 'parsed' lines.


        ## time patterns
        ## HMS = [HH:MM:SS]
        ## GPS.MIL = [NNNNNN.MMM]

        if "[" in line and "]" in line:
            openIndex = line.index('[')
            closeIndex = line.index(']')
            if closeIndex > openIndex :
                timestamp = line[openIndex:closeIndex+1]
                line = line[closeIndex+2:]

        line = line.strip("\r\n")
        line1 = line.replace(":", "")
        line1 = line1.replace(",", "")
        line1 = ' '.join(line1.split())
        if len(line1.split()) == 0:
            ## skip empty lines
            continue

#        print(str(ordinal) + "!  : " + str(line))
        print(str(ordinal) + "<<<: " + str(line1))

        if "warning fan alert" in line1.lower():
            pass

        parsed_log = logParse.parseLogLine(line1, [ordinal,timestamp])
        if parsed_log[0] == False:
            print("lineParse fail.")
            for item in parsed_log:
                print(str(item) + ":")
        else:
            print(str(ordinal) + ">. : " + str(parsed_log[1]))
        parsedLine = parsed_log[1]
        processed_logs.append(parsedLine)
        #        logPrintLine = util.simple_list_to_string(parsed_log[1])+"\r\n"
        logPrintLine = repr(parsed_log[1]) + "\r\n"
        parsedOutputFile.writelines(logPrintLine)
        ordinal += 1

    parsedOutputFile.close()
    return


def driveThermalLogParsing():
    parser = argp.ArgumentParser(description="AVEPM Thermal Log Analyzer")

    sequencedParsedLogs = False

    parser.add_argument("-fpga", dest="fpgalog", help="fpga log pathname", metavar="FILE")
    parser.add_argument("-epm1", dest="epm1log", help="epm1 log pathname", metavar="FILE")
    parser.add_argument("-epm2", dest="epm2log", help="epm2 log pathname", metavar="FILE")

    args = parser.parse_args()

    ## DEFINE a caseHandler for the LogParser
    ## TEXT OPERATIONS: use lower case operands
    ## OUTPUT TEXT:     output ANY case
    fanlogCaseHandler = util.caseHdlr(mcuptype.TXTOPS_LCASE, mcuptype.TXTOUT_ANY)

 #   appRegistry = mcutil.applicationRegistry()
 #   logParse = mcuparse.logLineParser(fanlogCaseHandler, appRegistry)  # type: object

    if sequencedParsedLogs:
        # fpga filename is mandatory, epm1 & 2 filenames optional
        # open defined files
        import time
        timeString = time.asctime(time.localtime(time.time()))
        sequenceID = timeString.replace(' ', '_')
        sequenceID = sequenceID.replace(':', '.')
    else:
        sequenceID = ""


    if len(args.fpgalog) == 0:
        message = "fpgalog name is :" + args.fpgalog + ":"
        print(message)
        # fpga_log filename is mandatory - fail
        parser.print_help()
        exit(-1)

    else:
        useFPGA = True
        useEPM1 = useEPM2 = False
        try:
            fpgaLog = open(args.fpgalog, 'r')
            useFPGA = True
            outputLog = str(args.fpgalog)
            slashIndex = outputLog.rfind('\\')


            if slashIndex >= 0:
                outputLog = outputLog[slashIndex+1:]

            if sequencedParsedLogs:
                fpgaOutputFileName = str(outputLog + "_" + sequenceID + "_parsed.log")
            else:
                fpgaOutputFileName= str(outputLog+"_parsed.log")

            fpgaOutputFilePathname = "logfiles\\parsedLogs\\" + fpgaOutputFileName


        except Exception as e:
            print(e)
            print("cannot open " + args.fpgalog)
            exit(-1)

        finally:
            pass

        if args.epm1log != None:
            try:
                epm1Log = open(args.epm1log, 'r')
                useEPM1 = True
                outputLog = str(args.epm1log)
                slashindex = outputLog.rfind('\\')

                if slashindex >= 0:
                    outputLog = outputLog[slashIndex:]

                epm1OutputFileName = str(outputLog + "_" + sequenceID + ".parsed.log")
                epm1OutputFilePathname = "logfiles\\parsedLogs\\" + epm1OutputFileName

            except Exception as e:
                print(e)
                print("cannot open " + args.epm1log)
                exit(-1)

            finally:
                pass

        if args.epm2log != None:
            try:
                epm2Log = open(args.epm2log, 'r')
                useEPM2 = True
                outputLog = str(args.epm2log)
                slashindex = outputLog.rfind('\\')

                if slashindex >= 0:
                    outputLog = outputLog[slashIndex:]

                epm2OutputFileName = str(outputLog + "_" + sequenceID + ".parsed.log")
                epm2OutputFilePathname = "logfiles\\parsedLogs\\" + epm2OutputFileName

            except Exception as e:
                print(e)
                print("cannot open " + args.epm2log)
                exit(-1)
                pass

            finally:
                pass

        ## DEFINE a caseHandler for the LogParser
        ## TEXT OPERATIONS: use lower case operands
        ## OUTPUT TEXT:     output ANY case
        fanlogCaseHandler = util.caseHdlr(mcuptype.TXTOPS_LCASE, mcuptype.TXTOUT_ANY)

        ## full system logs available
        ## process full system log set

        # !!!!! FOR DEBUG EPM ONLY
        # useFPGA = False

        # useFPGA = useEPM2 = False
        if useFPGA or useEPM1 or useEPM2:
            thregistry.buildRegistries()
            registryKeyedList = thregistry.thermregRegistryKeyedList

            if useFPGA == True:
                fpgaRegistry = registryKeyedList.getEntry(thregistry.fpgaRegistry_key)
                fpgaParser = mcuparse.logLineParser(fanlogCaseHandler, fpgaRegistry)
                processLog(fpgaParser, fpgaLog, fpgaOutputFilePathname)

            if useEPM1 == True:
                epmRegistry = registryKeyedList.getEntry(thregistry.epmRegistry_key)
                epmParser = mcuparse.logLineParser(fanlogCaseHandler, epmRegistry)
                processLog(epmParser, epm1Log, epm1OutputFilePathname)

            if useEPM2 == True:
                epmRegistry = registryKeyedList.getEntry(thregistry.epmRegistry_key)
                epmParser = mcuparse.logLineParser(fanlogCaseHandler, epmRegistry)
                processLog(epmParser, epm2Log, epm2OutputFilePathname)

        return (0)

    return (-1)


if __name__ == "__main__":
    exit(driveThermalLogParsing())
