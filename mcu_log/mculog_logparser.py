import mculog_data_sequence as ds
import mculog_parsetypes as pt
import mculog_utility as mcutil

import thermreg_log_specification as tlspec

# LogParser is a general purpose Log Parser in support of the
# specific AVEPM Log Parser Set
#
# The LogParser is intended to collect data into single or multi-item records
# and sequence them in lists for post-processing
#
# The CHEAP throwaway database is intended to load data quickly, potentially
# in realtime as the log is being streamed.
#
# One timing use-case to aim for is to sequence the data with realtime ticks
#
#
# The client program must define its log stream using the format/syntax provided
#
#*******************************************************************************


#******************************************************************
#
# 1. read log text lines
# 2. identify log line type
# 3. for each log/event text line
#       a) extract and save log data
#       b) extract and save embedded line/event sequence information
#       c) optionally generate line/event sequence information
#       d) preserve correlation between data/events and sequence
#
# 4. present interface to database(s) created by log parsing
# 5. present interface for formatted-text and/or graphical presentation
#    of data
#
#***********************************************************************

# log lines can be recognized for their content by predefined keys
#     1. keyword(s) embedded in line
#     2. line order following a recognized "key line"
#     3. key syntax / numbering (nearly same as keywords)
#
# log lines have predefined data content
# predefined recognized log lines are processed by handler functions
#
#
# log lines can be corrupted
# corrupted lines are not passed to the handlers for interpretation
# syntax and consistency checking is part of the parser value/function


#<ignoreline_keyword>
# sequence_value:  < [numeric ordinal]|[ h:m:s[.nnn] time value] >
# ignoreline_keyword: a keyword leading an ignored log line text
# logline_keyword:   a keyword leading a unignored log line text
#  < [ nonkey text ] <datum key predecessor> <datum_type>  [ nonkey text] >
#


# when parsing a logline, specific data are either emitted to a record/datum sequence
# or discarded

# "sensor A8 local temperature 30.75 deg C remote temperature 29.37 deg C"
#  id_list: [idListname, [ id0, id1, ... ] ]
#  <logline_key datumkey:'sensor' > <datumtype: ID <idListname>> < datumkey: 'local temperature' > < datumtype: fixedpoint > < ignoretextkey: 'deg C'>
#  <ignoreline_key: 'Tach2' >
#      ignore a line with a keyword. in our implementation Tach2 is useless information
#
# Device A0 Tach2 count 1231, rpm 2437
# No TACH value as device A8 duty cycle is 0
# Device A8 Tach1 count 0, rpm 0
#
#
# <translatelinekey: 'No TACH value as'> < datumkey: 'device'> <datumtype: ID < 'fansocket_id' > < datumkey: 'duty cycle is' > < datumtype: number >
#
#
#

# Record Parsing
# a Record is a list with a fixed number of entries, an assigned data type for each entry location
# 
# a challenge is how to get a record created from data in multiple lines of a log
# 
# a record input specification is a list of line-keywords for each of the lines that contribute to its contents
#
#  the first keyword triggers its instantiation
# the last keyword bearing line finishing processing triggers the closure of the record
#
# an open record is closed whenever a fresh record of the same type is instantiated.
# the closure of the record must preceed the instantiation and processing to the following record (for sanity's sake)
#
# the record has a definition, where the id of each record occupies its position in the record definition list
# as lines of log are parsed, following the record instantiation pursuant to the incidince of the record's "line keyword"..
# the parsed entries matching the record's manifest, are entered into the fresh record instance
# 


## ******************************************************************
## ******************************************************************
##
##  Process for Parsing Logs
##
##  1. define log line formats/specs. One for each log line
##  1b.lines that vary only by a single parameter may be defined using
##     commands to pick an id or datum from a list
##
##  2. register each list and list-key with the parser
##      ..this will be needed if referring to a list in a line format
##un
##  3. register all line formats with the parser that will be used in
##     parsing sessions
##
##  4. register all output stream handlers that will manage data from
##     the log parsing session.
##
##  5.  open a log parsing session and invoke the parser once for each
##      log line
##
##  6.  review the results of the session in the products of the output
##      stream handlers. Enjoy!
##
## ********************************************************************
## ********************************************************************
##
##
##
##
##
##
##
##



## genParsedLogSpec(logSpec)
## generates the parsedLogLineSpecification
## for a given LogLineSpecification
##
## The ParsedLogSpec defines the format
## of the result of the logLineParser for a given
## log Line parsed by its logSpec
##


class genParsedLogSpec(object):

    def __init__(self, logSpec):
        self.logSpec = logSpec
        self.parseSpec = []
        return


    def translateLogLineSpec(self):
        ## translate the logLineID portion
        for item, ordinal in enumerate(self.logSpec, 0):
            if ordinal == 0:
                ## process logLineID item
                if item[0] == pt.parseLineID:
                    self.parseSpec.append(item)
                else:
                    raise ValueError

            else:
                ## process dataname/data item
                ## a 2 list dataname+data spec will parse to
                ## a single list two element spec
                if item[0][0] in [pt.parseDatumNamefromList]:
                    pass

                pass
            pass

        ## translate each data specification
        ## within the logLineSpec

        return


class logLineParser(object):
# maintains the line definition
# parses the line according to a fixed algorithm
# the algorithm constrains and defines the lined
# definition syntax

    appRegistry = None
    reg_idKeyedList = None
    reg_logLineKeyedSpecList = None
    logLineKeys = None
    reg_idListKeys = None

    def hardReset(self):

        self.reg_idListKeys = []

        if self.appRegistry != None:
            self.reg_idKeyedList = self.appRegistry.get_idKeyedList()
            self.reg_logLineKeyedSpecList = self.appRegistry.get_logLineKeyedSpecList()
            self.logLineKeys = self.appRegistry.get_logLineKeys()
            self.reg_idListKeys = self.appRegistry.get_idListKeys()

        else:
            self.reg_idKeyedList = mcutil.keyedList()
            self.reg_logLineKeyedSpecList = mcutil.keyedList()
            self.logLineKeys = []
            self.reg_idListKeys = []

        self.logLineSequence = 0

        return

    def __init__(self, caseHandler: mcutil.caseHdlr, appRegistry: mcutil.applicationRegistry = None):
        self.appRegistry = appRegistry
        self.caseHandler = caseHandler
        self.hardReset()
        return



    def getAppRegistry(self):
        return self.appRegistry

    def emitDataRecord(self):
        pass

    def registerAggregatedRecord(self, aggregateRecordSpec):
        pass


    def startLogSession(self):
        return True


    def parseLogLine(self, logLine, logLineSequenceID = None, logLineTime = None):
        ## parse log line using simple output method
        ## create a record of the Words parsed
        ## return the record on completion of line parse

        ## identify logLine type
        ## line must include a recognized logLineID
        ## parsed data is emitted -for the present-
        ## into a list, which is returned for inspection
        ##  -- this supports initial unit testing


        ## returns list with success code, and result record

        ## User provides sequence ID
        ## else an ordinal is assigned
        ## TODO: actually use the sequence ID
        ## TODO: presently, it is simply assigned, and nothing more
        if logLineSequenceID == None:
            logLineSquenceID = self.logLineSequence
            self.logLineSequence += 1


        try:
            logWords = mcutil.wordInputStream(logLine, self.caseHandler)

            logLineID_Detected = False

            # parse log line until logLineID is detected
            # discard if not detected, reparse otherwise

            logLineID_matched = False
            logLineKey = None

            ## some logLineKeys are a partial match for longer
            ## logLineKeys ( fan, fan log, fan logs )
            ## search must be from longest to shortest for
            ## partial matching subsets.
            ##

            keyMatch = []
            for testKey in self.logLineKeys:
                if logWords.matchPhrase(testKey, pt.TXTOPS_ANY):
                    keyMatch.append(testKey)
                    continue
            ## ALL Keys that match the start of the log line
            ## are identified in list keyMatch[]

            if len(keyMatch) == 0:
                ## zero matches, line is not recognized
                logLineID_matched = False
            elif len(keyMatch) == 1:
                ## one match, one is exactly recognized
                logLineKey = keyMatch[0]
                logLineID_matched = True
            else:
                ## multiple matches
                ## longest matching key identifies the line
                guessKey = keyMatch[0]
                for testKey in keyMatch[1:]:
                    if len(testKey) > len(guessKey):
                        guessKey = testKey
                logLineKey = guessKey
                logLineID_matched = True

            if logLineID_matched == False:
                ## Line unrecognized, no parse product
                return [False, None]

            ## syntax of identified log line
            lineSpec = self.reg_logLineKeyedSpecList.getEntry(logLineKey)
            if lineSpec == None:
                raise ValueError


            ## output record instance
            logRecord = mcutil.simpleParseRecord()


            ## reparse past line ID
            for itemIndex in range (0,len(lineSpec)):
                item = lineSpec[itemIndex]
                ## item 0 in line specification is a list with
                ## only two items.
                ## items 1..N are lists of two two-item lists
                ## command, operant are in the first/(only) sub-list

                if itemIndex == 0:
                    nameCommand = item[0]
                    nameOperant = item[1]
                else:
                    nameCommand = item[0][0]
                    nameOperant = item[0][1]

                if nameCommand == pt.parseLineID:
                    ## parse past LineID
                    ## emit into record ?
                    lineID = nameOperant
                    if not logWords.matchPhrase(nameOperant, pt.TXTOPS_LCASE, True):
                        raise ValueError

                    logRecord.addItem(nameCommand, lineID)
                    continue


                if nameCommand == pt.parseLineIDfromList:
                    if not self.appRegistry.idListRegistered(nameOperant):
                        raise ValueError

                    ## fetch line ID List
                    idList = self.reg_idKeyedList.getEntry(nameOperant)
                    idMatched = False

                    for thisID in idList:
                        if logWords.matchPhrase(thisID, True, False):
                            idMatched = True
                            logRecord.addItem([nameCommand, thisID])
                            break

                    if not idMatched:
                        raise ValueError

                    continue

                if nameCommand in [pt.parseDatumName, pt.parseDatumNamefromList, pt.setDatumName, pt.skipDatumName]:
                    if nameCommand == pt.parseDatumName:
                        if (nameOperant not in pt.datumNameOperantSet):
                            # Operant is of name, compare.
                            if logWords.matchPhrase(nameOperant, pt.TXTOPS_LCASE, True):
                                datumName = nameOperant
                            else:
                                raise ValueError

                        elif nameOperant == pt.parseTextWord:
                            datumName = logWords.nextWord()
                        else:
                            raise ValueError

    #                    if not logWords.matchPhrase(nameOperant, pt.TXTOPS_LCASE, True):
    #                        raise ValueError
                        #datumName = logWords.nextWord()

                    elif nameCommand == pt.parseDatumNamefromList:
                        datumListKey = nameOperant
                        datumList = self.reg_idKeyedList.getEntry(datumListKey)
                        datumName = logWords.matchListedPhrase(datumList, pt.TXTOPS_LCASE, True)

                        if datumName == None:
                            raise ValueError

                    elif nameCommand == pt.setDatumName:
                        ## no name to parse from log
                        ## set name directly
                        datumName = nameOperant

                    elif nameCommand == pt.skipDatumName:
                        datumName = ""

                datumCommand = item[1][0]
                datumOperant = item[1][1]

                if datumCommand == pt.parseDatum:
                    if datumOperant in [pt.parseInt, pt.parseTextWord, pt.parseFixedPoint]:
                        thisDatum = logWords.nextWord()

                        if datumOperant == pt.parseInt:
                            thisDatum = mcutil.str2int(thisDatum)

                        elif datumOperant == pt.parseFixedPoint:
                            thisDatum = mcutil.str2float(thisDatum)

                        elif datumOperant == pt.parseTextWord:
                            ## nothing to do, is a string
                            pass

                        logRecord.addItem(datumName, thisDatum)
                        continue

                    else:
                        raise NotImplementedError

                elif datumCommand == pt.parseDatumfromList:
                    lookupList = self.reg_idKeyedList.getEntry(datumOperant)
                    thisDatum = None
                    for datum in lookupList:
                        if logWords.matchPhrase(datum, pt.TXTOPS_LCASE, True):
                            thisDatum = datum
                            break

                    if thisDatum == None:
                        raise ValueError

                    logRecord.addItem(datumName, thisDatum)
                    continue

                elif datumCommand == pt.setDatum:
                    thisDatum = datumOperant
                    logRecord.addItem(datumName, thisDatum)
                    continue

                elif datumCommand in [pt.skipText, pt.skipTextWord, pt.skipTextWords, \
                                      pt.skipUntilWordMatch, pt.skipIncludingWordMatch]:
                    if datumCommand == pt.skipText:
                        logWords.matchPhrase(datumOperant, pt.TXTOPS_LCASE, True)

                    elif datumCommand == pt.skipTextWord:
                        logWords.nextWord()

                    elif datumCommand == pt.skipTextWords:
                        skipCount = mcutil.str2int(logWords.nextWord())
                        ## max of 8 words skipped
                        if skipCount <= 0 or skipCount > mcutil.MAX_SKIP_COUNT:
                            raise ValueError
                        while skipCount > 0:
                            logWords.nextWord()

                    elif datumCommand in [ pt.skipUntilWordMatch, pt.skipIncludingWordMatch ]:
                        while logWords.nextWord() != datumOperant:
                            pass
                        if datumCommand == pt.skipUntilWordMatch:
                            logWords.seekRelative(-1)

                    continue

                raise NotImplementedError

            return [True, logRecord.getRecord()]


        except Exception as e:
            if e == ValueError:
                exceptmsg = "Unexpected or Garbage data"
            else:
                exceptmsg = "Unknown error"

#        finally:
            errorRecord = [[pt.error_ParseErrorReport, exceptmsg], logLine],
            return [False, errorRecord]
