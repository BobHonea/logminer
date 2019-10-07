## Python Module
##
## General Utility Functions for Log Parser Engine
##

import mculog_parsetypes as pt
import time
import calendar

def smartMax(inputList : list):
    tempList = []


    for item in inputList:
        if type(item) in [int, float]:
            tempList.append(item)
            continue

        item = str(item)
        if item.isnumeric():
            if '.' in item:
                tempList.append(float(item))
            else:
                tempList.append(int(item))
        else:
            # drop strings
            pass
        continue

    if len(tempList) > 0:
        return max(tempList)

    return None


def listFromIndices(sourceRecord: list, indices: list):
    # return a list of sourceRecord items as located
    # by a given list of item indices

    data = []
    for index in indices:
        data.append(sourceRecord[index])

    return data


def simple_list_to_string(item):
    # return a string version of list with items of types: int,float,str,bool,list
    textLine = ""

    if item == None:
        textLine += """+"None"+"""
    elif type(item) in [int, float, str, bool]:
        textLine += """+str(item)+"""

    elif type(item) != list:
        raise NotImplementedError

    else:
        # processing list items
        textLine = textLine + "["
        subItemCount = len(item)
        for subitem in item:
            textLine = textLine + simple_list_to_string(subitem)
            subItemCount -= 1
            if subItemCount != 0:
                textLine += ","
        textLine = textLine + "]"

    return textLine


def str2int(strval):
    ## snip prefix and suffic punctuation
    ## beware, some punctuation is relevant
    ## to the int/hex input value

    strval = strval.rstrip(",:;-")
    strval = strval.lstrip(",:;")

    if str(strval).count('x') == 1:
        try:
            retval = int(strval, 0)
            return retval
        except:
            raise ValueError
    else:
        try:
            retval = int(strval)
            return retval
        except:
            raise ValueError


def str2float(strval):
    try:
        retval = float(strval)
        return retval
    except:
        raise ValueError

def uniqueNonemptyLexibleList(itemList):
    if len(itemList) == 0:
        #empty list
        return False

    for item in itemList:
        item_index = itemList.index(item)
        if item.isalnum():
            # each ID is nonnull and lexible

            for position in range(0,len(itemList)):
                if position == item_index:
                    #skip self-comparison
                    #compare to occupants of other positions
                    continue

                if item == itemList[position]:
                    # duplicate, fail.
                    return False

    # there are no duplicate items
    return True

class caseHdlr(object):
    # there is a meaningful order relationship for the following two
    # lists, do not disturb it without deep thought
    outputRules = [pt.TXTOUT_ANY, pt.TXTOUT_LCASE, pt.TXTOUT_UCASE]
    operandRules = [pt.TXTOPS_ANY, pt.TXTOPS_LCASE, pt.TXTOPS_UCASE]

    def caseRulesValid(self, caseRules):
        return (caseRules[0] in self.operandRules and caseRules[1] in self.outputRules)

    def __init__(self, operandRule, outputRule):
        if self.caseRulesValid([operandRule, outputRule]):
            self.operandRule = operandRule
            self.outputRule = outputRule
        else:
            raise ValueError

        return

    def operand(self, srcText, overrideRule=None):

        if overrideRule != None:
            if overrideRule not in self.operandRules:
                raise ValueError

            operandRule = overrideRule
        else:
            operandRule = self.operandRule

        if operandRule == pt.TXTOPS_ANY:
            return srcText

        if operandRule == pt.TXTOPS_LCASE:
            return str(srcText).lower()
        elif operandRule == pt.TXTOPS_UCASE:
            return str(srcText).upper()
        elif operandRule == pt.TXTOPS_ANY:
            return str(srcText)
        else:  # this is absurd, therefore error
            raise ValueError

    def output(self, opText, overrideRule=None):
        strOpText = str(opText)

        if overrideRule == None:
            outputRule = self.outputRule
        elif overrideRule not in self.outputRules:
            raise ValueError
        else:
            outputRule = overrideRule

        if outputRule == pt.TXTOUT_ANY:
            return strOpText

        if outputRule == pt.TXTOUT_LCASE:
            return strOpText.lower()
        else:
            return strOpText.upper()

    def lcase_operands(self):
        return pt.TXTOPS_LCASE == self.operandRule

    def lcase_output(self):
        return pt.TXTOUT_LCASE == self.operandRule

    def raw_operands(self):
        return pt.TXTOPS_ANY == self.operandRule

    def raw_output(self):
        return pt.TXTOUT_ANY == self.outputRule

    def ucase_operands(self):
        return pt.TXTOPS_UCASE == self.operandRule

    def ucase_output(self):
        return pt.TXTOUT_UCASE == self.outputRule

    def compare(self, textA, textB, overrideRule=pt.TXTOPS_ANY):
        strA = str(textA)
        strB = str(textB)

        if overrideRule != pt.TXTOPS_ANY:
            if overrideRule not in self.operandRules:
                raise ValueError

            operandRule = overrideRule
        else:
            operandRule = self.operandRule

        if operandRule == pt.TXTOPS_ANY:
            return strA == strB

        # if forced to compare in a single case
        # either case will do
        return (strA.lower() == strB.lower())

    def coercedOperandRule(self, outputRule):
        outputRuleIndex = self.outputRules.index(outputRule)
        if outputRuleIndex >= len(self.operandRules):
            raise ValueError

        return self.operandRules[outputRuleIndex]

    def coercedOutputRule(self, operandRule):
        operandRuleIndex = self.operandRules.index(operandRule)
        if operandRuleIndex >= len(self.outputRules):
            raise ValueError

        return self.outputRules[operandRuleIndex]


class wordInputStream(object):

    ## expecting a textline that is stripped of CR/LF
    ## whitespace will be stripped by the split() function
    ## words split from string can be obtained individually

    ## the case of operand text is governed by the passed in
    ## text case handler object. note that applications of
    ## this object can override the case handler's rules.

    def __init__(self, textline, textCaseHdlr: caseHdlr):
        self.m_textHandler = textCaseHdlr
        self.m_logLineWords = textline.split()
        self.m_lineWordsCount = len(self.m_logLineWords)
        self.m_endOfLineIndex = self.m_lineWordsCount
        self.m_lastWordIndex = self.m_endOfLineIndex - 1
        self.m_wordsIndex = 0
        return

    def lineWords(self):
        return self.m_textHandler.output(self.m_logLineWords)

    def wordsCount(self):
        return self.m_lineWordsCount

    def wordsIndex(self):
        return self.m_wordsIndex

    def nextWord(self, outputCaseRule=None):
        if self.m_wordsIndex < self.m_endOfLineIndex:
            textWord = self.m_logLineWords[self.m_wordsIndex]
            self.m_wordsIndex += 1
            return self.m_textHandler.output(textWord, outputCaseRule)
        return None

    def nextWords(self, wordCount, outputCaseRule=None):
        if self.m_wordsIndex <= self.m_endOfLineIndex - wordCount:
            phrase = " ".join(self.m_logLineWords[self.m_wordsIndex:self.m_wordsIndex + wordCount])
            return self.m_textHandler.output(phrase, outputCaseRule)

        return None

    def thisWord(self, outputCaseRule=None):
        textWord = self.m_logLineWords[self.m_wordsIndex]
        return self.m_textHandler.output(textWord, outputCaseRule)

    def endOfLine(self):
        return (self.m_wordsIndex == self.m_endOfLineIndex)

    def seekRelative(self, offset):
        newIndex = self.m_wordsIndex + offset
        if newIndex < 0:
            raise ValueError
        self.m_wordsIndex = newIndex
        return

    def seekAbsolute(self, newIndex):
        if newIndex >= 0 or newIndex <= self.m_endOfLineIndex:
            self.m_wordsIndex = newIndex
            return
        raise ValueError

    def seekFirstWord(self):
        self.m_wordsIndex = 0;

    def seekLastWord(self):
        self.m_wordsIndex = self.m_lastWordIndex

    def matchPhrase(self, phrase, operandCaseRule=pt.TXTOPS_ANY, postIncrement=False):
        phraseWords = str(phrase).split()
        phraseWordCount = len(phraseWords)
        cleanPhrase = " ".join(phraseWords)

        builtPhrase = " ".join(self.m_logLineWords[self.m_wordsIndex:self.m_wordsIndex + phraseWordCount])

        if self.m_textHandler.compare(cleanPhrase, builtPhrase, operandCaseRule):
            if postIncrement:
                self.m_wordsIndex += phraseWordCount
            return True
        else:
            return False

    def seekFwdToWordMatch(self, matchWord, operandCaseRule=pt.TXTOPS_ANY, postIncrement=True):
        while not self.endOfLine():
            # note that an 'operandCaseRule' is given to nextword which takes an
            # 'outputCaseRule'... since the output is immediately consumed as an
            # operand, then the operandRule is fitting.
            outputCaseRule = self.m_textHandler.coercedOutputRule(operandCaseRule)
            if self.m_textHandler.compare(self.nextWord(outputCaseRule), matchWord, operandCaseRule):
                if postIncrement == False:
                    self.seekRelative(-1)
                return True
        return False

    def seekFwdToPhraseMatch(self, phrase, operandCaseRule=pt.TXTOPS_ANY, postIncrement=False):
        startIndex = self.m_wordsIndex
        phraseWords = phrase.split()
        phraseWordCount = len(phraseWords)
        phraseEOLIndex = self.m_endOfLineIndex - phraseWordCount + 1
        phraseMatched = False

        while not phraseMatched and phraseEOLIndex > self.m_wordsIndex:
            if self.seekFwdToWordMatch(phraseWords[0], operandCaseRule, False) == True:
                ## first word match
                candidate = " ".join(self.m_logLineWords[self.m_wordsIndex:self.m_wordsIndex + phraseWordCount])
                if self.m_textHandler.compare(candidate, phrase, operandCaseRule):
                    phraseMatched = True
                    break

        if phraseMatched:
            if postIncrement:
                self.m_wordsIndex = self.m_wordsIndex + phraseWordCount
            return True

        else:
            ## word pointer does not move unless match found
            self.m_wordsIndex = startIndex
            return False

    def matchListedPhrase(self, phraseList, operandCaseRule=pt.TXTOPS_ANY, postIncrement=True):
        for thisPhrase in phraseList:
            if self.matchPhrase(thisPhrase, operandCaseRule, postIncrement):
                return self.m_textHandler.output(thisPhrase)

        return None


# prevent runaway skipping, limit skipping
MAX_SKIP_COUNT = 8


class keyedList(object):

    def __init__(self):
        self.m_keyedList = []
        return

    def addEntry(self, key, item):
        self.m_keyedList.append([key, item])
        return

    def removeEntry(self, key):
        del self.m_keyedList[key]
        return

    def getEntry(self, key):
        for entry in self.m_keyedList:
            if entry[0] == key:
                return entry[1]
        return None

    def entryExists(self, key):
        for entry in self.m_keyedList:
            if entry[0] == key:
                return True

        return False

    def purge(self):
        self.m_keyedList = []


class simpleParseRecord(object):

    def __init__(self):
        self.m_parseRecord = []
        return

    def addItem(self, datumName, datumValue):
        self.m_parseRecord.append([datumName, datumValue])
        return

    def getItemCount(self):
        return len(self.m_parseRecord)

    def getRecord(self):
        return self.m_parseRecord

    def purge(self):
        self.m_parseRecord = []



class applicationRegistry(object):

    def __init__(self):
        self.logLine_keyedList = keyedList()
        self.logLineKeyedSpecList = keyedList()
        self.idKeyedList = keyedList()
        self.logLineKeys = []
        self.idListKeys = []
        return


    def get_logLineKeyedSpecList(self):
        return self.logLineKeyedSpecList


    def get_idKeyedList(self):
        return self.idKeyedList

    def get_logLineKeys(self):
        return self.logLineKeys

    def get_idListKeys(self):
        return self.idListKeys

    def registerIdList(self, idTypeName, idList):
        # verify the list is nonempty
        # see no use, at present, for empty idList
        # verify the items are unique


        if type(idTypeName) == str:
            # ID type name is nonnull, lexible

            if idTypeName not in self.idListKeys:
                if uniqueNonemptyLexibleList(idList):
                    # id/keyword is useable by parser
                    self.idListKeys.append(idTypeName)
                    self.idKeyedList.addEntry(idTypeName, idList)
                    return True

        return False



    def registerRecord(self, recordTypeName, recordDefinition):
        return False

    def registerLogLineSpecification(self, logLineKey, logLineSpec):
        # logLineSpec is a single line of syntax
        # line id keywords must be recognized
        # logLineSpec is a list with:
        # initial item is list of keyword-seek command, and value
        # following list items are either:
        #   1. list [seek-constant-text-directive, text-constant]
        #   2. list [[datum-name-parse-cmd, datum-name-operand], [datum-value-parse-cmd, datum-value-operand]]
        #
        #  verify the list fits this syntax and all referred operands
        #  and resources are available

        if self.logLineSpecRegistered(logLineKey):
            raise ValueError

        lineIDParseCmd = logLineSpec[0][0]
        lineIDKey = logLineSpec[0][1]

        if lineIDParseCmd != pt.parseLineID:
            ## Only Single Value LineID supported atm
            print("Multivalue Line ID not implemented yet!!")
            raise ValueError

        if self.logLineSpecRegistered(lineIDKey):
            ## key collision
            print("Key Collision!!")
            raise ValueError

        #        if logLineSpec [0][0] == pt.parseLineIDfromList:
        #            if type(logLineSpec[0][1]) is not list:
        #                return False

        for parameterIndex in range(1, len(logLineSpec)):
            parseSpec = logLineSpec[parameterIndex]

            ## process parsing of each element of line
            ## an operant command is followed by an operand
            ## the operand is either a text constant or a
            ## selection list
            ## the parsed value must match a constant or text list item

            print(parseSpec)
            parseNameCmd = parseSpec[0][0]
            parseNameOperant = parseSpec[0][1]

            if parseNameCmd not in [pt.parseDatumName, pt.parseDatumNamefromList,
                                    pt.skipDatumName, pt.setDatumName, pt.skipTextWords]:
                return False

            # verify list processing resources are registered
            if parseNameCmd == pt.parseDatumNamefromList:
                listKey = parseNameOperant

                if not self.idListRegistered(listKey):
                    raise ValueError

                datumList = self.getRegisteredIdList(listKey)
                if len(datumList) == 0:
                    raise ValueError

            datumCmd = parseSpec[1][0]
            datumOperant = parseSpec[1][1]

            if datumCmd not in [pt.parseDatum, pt.parseDatumfromList, pt.skipTextWord, pt.skipText,
                                pt.skipTextWords, pt.skipUntilWordMatch, pt.skipIncludingWordMatch,
                                pt.setDatum]:
                raise ValueError

            if datumCmd == pt.parseDatum:
                if datumOperant not in [pt.parseInt, pt.parseTextWord, pt.parseFixedPoint]:
                    raise ValueError

            elif datumCmd == pt.parseDatumfromList:
                ## datum Operant is list key for parse from list
                if not self.idListRegistered(datumOperant):
                    raise ValueError

            elif datumCmd == pt.skipTextWord:
                if type(datumOperant) != str:
                    raise ValueError

            ## parse spec check for pt.parseDatumName, pt.parseDatumNameFromList
            ## is concluded
            continue

        self.logLineKeys.append(lineIDKey)
        self.logLineKeyedSpecList.addEntry(logLineKey, logLineSpec)

        return True

    def logLineSpecRegistered(self, logLine_key):
        return (logLine_key in self.logLineKeys)

    def idListRegistered(self, idList_key):
        return (idList_key in self.idListKeys)

    def getRegisteredIdList(self, key):
        thisList = self.idKeyedList.getEntry(key)
        return thisList
        ## exception raised on failure!!



