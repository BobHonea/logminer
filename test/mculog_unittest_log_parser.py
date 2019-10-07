# !/usr/bin/python
#
#  python class module
import mculog_logparser as lp
import mculog_parsetypes as pt
import mculog_utility as util

processed_logs = []

Menu_key = "menu"
MenuItems = ["Americano", "Cappuchino"]

textConstantLog = "textConstant ConstantText"
textConstantLogLineID = "textConstant"
textConstantLogSpec = [[pt.parseLineID, textConstantLogLineID],
                       [[pt.skipDatumName, pt.noparse],
                        [pt.skipTextWord, "ConstantText"]]]

singleIntLog = "Coffee Order Americano 1"
singleIntLogLineID = "Coffee Order"
singleIntLogSpec = [[pt.parseLineID, singleIntLogLineID],
                    [[pt.parseDatumNamefromList, Menu_key],
                     [pt.parseDatum, pt.parseInt]]]

fixedPointLog = "Imprecise Coffee Order Americano 1.0015"
fixedPointLogLineID = "Imprecise Coffee Order"
fixedPointLogSpec = [[pt.parseLineID, fixedPointLogLineID],
                     [[pt.parseDatumName, "Americano"],
                      [pt.parseDatum, pt.parseFixedPoint]]]

textVariableLog = "Uncertain Coffee Order Cappuchino likemaybeone"
textVariableLogLineID = "Uncertain Coffee Order"
textVariableLogSpec = [[pt.parseLineID, textVariableLogLineID],
                       [[pt.parseDatumName, pt.parseTextWord],
                        [pt.parseDatum, pt.parseTextWord]]]

logLineIDList_key = "logLineIDLists"
logLineIDList = [textConstantLogLineID, singleIntLogLineID, fixedPointLogLineID, textVariableLogLineID]


def unittest_caseHandler():
    # this class is used to regularize the case of operand text within
    # a set of operations, as well as to specify the case of text to be
    # output from the operation sequence it serves.

    lCaseString = "not much to say"
    uCaseString = "NOT MUCH TO SAY"
    mixedCaseString = "Not Much To Say"

    # P2(u,r,l) = [ uu, rr, ll, ur, ul, rl, ru, lu, lr ]

    uuHandler = util.caseHdlr(pt.TXTOPS_UCASE, pt.TXTOUT_UCASE)

    llHandler = util.caseHdlr(pt.TXTOPS_LCASE, pt.TXTOUT_LCASE)

    rrHandler = util.caseHdlr(pt.TXTOPS_ANY, pt.TXTOUT_ANY)

    urHandler = util.caseHdlr(pt.TXTOPS_UCASE, pt.TXTOUT_ANY)

    ulHandler = util.caseHdlr(pt.TXTOPS_UCASE, pt.TXTOUT_LCASE)

    rlHandler = util.caseHdlr(pt.TXTOPS_ANY, pt.TXTOUT_LCASE)

    ruHandler = util.caseHdlr(pt.TXTOPS_ANY, pt.TXTOUT_UCASE)

    luHandler = util.caseHdlr(pt.TXTOPS_LCASE, pt.TXTOUT_UCASE)

    lrHandler = util.caseHdlr(pt.TXTOPS_LCASE, pt.TXTOUT_ANY)

    # operand, output, compare methods

    assert (llHandler.output(lCaseString) == lCaseString)
    assert (llHandler.output(uCaseString) == lCaseString)
    assert (llHandler.output(mixedCaseString) == lCaseString)
    assert (llHandler.operand(lCaseString) == lCaseString)
    assert (llHandler.operand(uCaseString) == lCaseString)
    assert (llHandler.operand(mixedCaseString) == lCaseString)
    assert (llHandler.compare(lCaseString, uCaseString))
    assert (llHandler.compare(lCaseString, mixedCaseString))
    assert (llHandler.compare(uCaseString, mixedCaseString))

    assert (uuHandler.output(lCaseString) == uCaseString)
    assert (uuHandler.output(uCaseString) == uCaseString)
    assert (uuHandler.output(mixedCaseString) == uCaseString)
    assert (uuHandler.operand(uCaseString) == uCaseString)
    assert (uuHandler.operand(uCaseString) == uCaseString)
    assert (uuHandler.operand(mixedCaseString) == uCaseString)
    assert (uuHandler.compare(lCaseString, uCaseString))
    assert (uuHandler.compare(lCaseString, mixedCaseString))
    assert (uuHandler.compare(uCaseString, mixedCaseString))

    assert (rrHandler.output(lCaseString) == lCaseString)
    assert (rrHandler.output(uCaseString) == uCaseString)
    assert (rrHandler.output(mixedCaseString) == mixedCaseString)
    assert (rrHandler.operand(lCaseString) == lCaseString)
    assert (rrHandler.operand(uCaseString) == uCaseString)
    assert (rrHandler.operand(mixedCaseString) == mixedCaseString)
    assert (rrHandler.compare(lCaseString, uCaseString) == False)
    assert (rrHandler.compare(uCaseString, mixedCaseString) == False)
    assert (rrHandler.compare(mixedCaseString, lCaseString) == False)

    assert (urHandler.output(lCaseString) == lCaseString)
    assert (urHandler.output(uCaseString) == uCaseString)
    assert (urHandler.output(mixedCaseString) == mixedCaseString)
    assert (urHandler.operand(lCaseString) != lCaseString)
    assert (urHandler.operand(uCaseString) == uCaseString)
    assert (urHandler.operand(mixedCaseString) != mixedCaseString)
    assert (urHandler.compare(lCaseString, uCaseString))
    assert (urHandler.compare(uCaseString, mixedCaseString))
    assert (urHandler.compare(mixedCaseString, lCaseString))

    assert (lrHandler.output(lCaseString) == lCaseString)
    assert (lrHandler.output(uCaseString) == uCaseString)
    assert (lrHandler.output(mixedCaseString) == mixedCaseString)
    assert (lrHandler.operand(lCaseString) == lCaseString)
    assert (lrHandler.operand(uCaseString) != uCaseString)
    assert (lrHandler.operand(mixedCaseString) != mixedCaseString)
    assert (lrHandler.compare(lCaseString, uCaseString))
    assert (lrHandler.compare(uCaseString, mixedCaseString))
    assert (lrHandler.compare(mixedCaseString, lCaseString))

    assert (ruHandler.output(lCaseString) == uCaseString)
    assert (ruHandler.output(uCaseString) == uCaseString)
    assert (ruHandler.output(mixedCaseString) == uCaseString)
    assert (ruHandler.operand(lCaseString) == lCaseString)
    assert (ruHandler.operand(uCaseString) == uCaseString)
    assert (ruHandler.operand(mixedCaseString) == mixedCaseString)
    assert (ruHandler.compare(lCaseString, uCaseString) == False)
    assert (ruHandler.compare(uCaseString, mixedCaseString) == False)
    assert (ruHandler.compare(mixedCaseString, lCaseString) == False)

    assert (rlHandler.output(lCaseString) == lCaseString)
    assert (rlHandler.output(uCaseString) == lCaseString)
    assert (rlHandler.output(mixedCaseString) == lCaseString)
    assert (rlHandler.operand(lCaseString) == lCaseString)
    assert (rlHandler.operand(uCaseString) == uCaseString)
    assert (rlHandler.operand(mixedCaseString) == mixedCaseString)
    assert (rlHandler.compare(lCaseString, uCaseString) == False)
    assert (rlHandler.compare(uCaseString, mixedCaseString) == False)
    assert (rlHandler.compare(mixedCaseString, lCaseString) == False)

    assert (luHandler.output(lCaseString) == uCaseString)
    assert (luHandler.output(uCaseString) == uCaseString)
    assert (luHandler.output(mixedCaseString) == uCaseString)
    assert (luHandler.operand(lCaseString) == lCaseString)
    assert (luHandler.operand(uCaseString) != uCaseString)
    assert (luHandler.operand(mixedCaseString) != mixedCaseString)
    assert (luHandler.compare(lCaseString, uCaseString))
    assert (luHandler.compare(uCaseString, mixedCaseString))
    assert (luHandler.compare(mixedCaseString, lCaseString))

    assert (ulHandler.output(lCaseString) == lCaseString)
    assert (ulHandler.output(uCaseString) == lCaseString)
    assert (ulHandler.output(mixedCaseString) == lCaseString)
    assert (ulHandler.operand(lCaseString) != lCaseString)
    assert (ulHandler.operand(uCaseString) == uCaseString)
    assert (ulHandler.operand(mixedCaseString) != mixedCaseString)
    assert (ulHandler.compare(lCaseString, uCaseString))
    assert (ulHandler.compare(uCaseString, mixedCaseString))
    assert (ulHandler.compare(mixedCaseString, lCaseString))

    print("unittest_caseHandler success")
    return


def unittest_singleLineItemParse():
    ## encoding of data
    ## the parser will perform computations with lower-case
    ## renderings of text strings. the parser will output text
    ## verbatim, un-coerced to any case.

    caseHandler = util.caseHdlr(pt.TXTOPS_LCASE, pt.TXTOUT_ANY)

    logP = lp.logLineParser(caseHandler)

    ## register id/spec list keys

    ##assert(logP.registerIdList(logLineIDList_key, logLineIDList))

    assert (logP.registerIdList(Menu_key, MenuItems))

    ## register log line specs

    assert (logP.registerLogLineSpecification(singleIntLogLineID, singleIntLogSpec))

    assert (logP.registerLogLineSpecification(fixedPointLogLineID, fixedPointLogSpec))

    assert (logP.registerLogLineSpecification(textConstantLogLineID, textConstantLogSpec))

    assert (logP.registerLogLineSpecification(textVariableLogLineID, textVariableLogSpec))

    assert (logP.startLogSession())

    parsed_log = logP.parseLogLine(singleIntLog)
    assert (parsed_log[0])
    processed_logs.append(parsed_log)

    parsed_log = logP.parseLogLine(fixedPointLog)
    assert (parsed_log[0])
    processed_logs.append(parsed_log)

    parsed_log = logP.parseLogLine(textVariableLog)
    assert (parsed_log[0])
    processed_logs.append(parsed_log)

    parsed_log = logP.parseLogLine(textConstantLog)
    assert (parsed_log[0])
    processed_logs.append(parsed_log)

    for log in processed_logs:
        print("record: " + str(log[1]))

    print("unittest_singleLineItemParse success")
    return


def unittest_wordStreamParse():
    # The Wordstream defaults the following methods to lower case
    #
    # wordInputstream.thisWord(self, lcase=True)
    # wordInputStream.nextWords(self, wordCount, lcase=True)
    # wordInputStream.nextWord(self, lcase=True)
    # wordInputStream.matchListedPhrase(self, phrase, lcase=True, postIncrement=False)

    # define and pass a text operations handler to text processing objects
    # in this case, the wordstream

    # rawCaseHandler supports uncontrolled case of operand text, and text output
    rawCaseHandler = util.caseHdlr(pt.TXTOPS_ANY, pt.TXTOUT_ANY)
    # "lcaseOpsHandler" supports controlled lower-case operand text,
    # and uncontrolled text output
    lcaseOpsHandler = util.caseHdlr(pt.TXTOPS_LCASE, pt.TXTOUT_ANY)

    textline = "The Quick Red Fox Jumped Over The Lazy Brown Dog"
    lcase_textline = "the quick red fox jumped over the lazy brown dog"

    textline_wordlist = textline.split()
    wordCount = len(textline_wordlist)

    wordStream = util.wordInputStream(textline, rawCaseHandler)
    lcase_wordstream = util.wordInputStream(lcase_textline, lcaseOpsHandler)

    assert (wordStream.wordsCount() == wordCount)

    # Seek to, just past "Fox"
    while (wordStream.nextWord() != "Fox"):
        pass

    while (lcase_wordstream.nextWord() != "fox"):
        pass

    # back up, and compare 'foxes'

    wordStream.seekRelative(-1)
    lcase_wordstream.seekRelative(-1)
    assert (wordStream.thisWord() == "Fox")
    assert (lcase_wordstream.thisWord() == "fox")
    assert (wordStream.thisWord(pt.TXTOUT_LCASE) == "fox")

    lcase_wordstream.seekAbsolute(7)
    wordStream.seekAbsolute(7)
    assert (lcase_wordstream.thisWord() == "lazy")
    assert (wordStream.thisWord() == "Lazy")

    wordStream.seekFirstWord()
    assert (wordStream.thisWord(pt.TXTOUT_ANY) == "The")
    lcase_wordstream.seekLastWord()
    assert (lcase_wordstream.thisWord() == "dog")

    wordStream.seekFirstWord()
    assert (wordStream.seekFwdToWordMatch("over", pt.TXTOPS_LCASE, True) == True)
    wordStream.seekFirstWord()
    assert (wordStream.seekFwdToWordMatch("over", pt.TXTOPS_ANY, True) == False)
    lcase_wordstream.seekFirstWord()
    assert (lcase_wordstream.seekFwdToWordMatch("over", pt.TXTOPS_LCASE, True) == True)
    assert (lcase_wordstream.wordsIndex() == 6)

    wordStream.seekFirstWord()
    assert (wordStream.matchPhrase("The Quick Red Fox", pt.TXTOPS_ANY, True))
    assert (wordStream.matchPhrase("Jumped Over", pt.TXTOPS_ANY, True))
    assert (wordStream.matchPhrase("The Lazy Brown Dog", pt.TXTOPS_ANY))

    lcase_wordstream.seekFirstWord()
    assert (lcase_wordstream.seekFwdToPhraseMatch("red fox", pt.TXTOPS_ANY, True))
    assert (lcase_wordstream.wordsIndex() == 4)

    lcase_wordstream.seekFirstWord()
    assert (lcase_wordstream.matchPhrase("the quick", pt.TXTOPS_ANY, True))
    assert (not lcase_wordstream.seekFwdToWordMatch("red fox jumped over the lazy brown dog", pt.TXTOPS_ANY, False))
    lcase_wordstream.seekFirstWord()
    assert (lcase_wordstream.seekFwdToPhraseMatch("red fox jumped over the lazy brown dog", pt.TXTOPS_ANY, False))
    assert (lcase_wordstream.seekFwdToPhraseMatch("red fox jumped over the lazy brown dog", pt.TXTOPS_ANY, True))
    assert (lcase_wordstream.endOfLine())

    print("unittest_wordStreamParse success")
    return


test_list = [unittest_caseHandler, unittest_wordStreamParse, unittest_singleLineItemParse]


def main():
    for test in test_list:
        test()
    return


if __name__ == "__main__":
    main()
