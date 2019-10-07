import collections as coll
var_INT = "_p_int"
var_HEXINT = "_p_xint"
var_BININT = "_p_bint"
var_OCTINT = "_p_octint"
var_DECINT = "_p_decint"
var_FIXEDPOINT = "_p_fixedpt"
var_FLOATPOINT = "_p_floatpt"
var_LIST = "_p_list"
var_STRING = "_p_string"
var_DICT = "_p_dict"
var_TUPLE = "_p_tuple"



var_SCALAR = [var_INT, var_HEXINT, var_BININT, var_OCTINT,
               var_DECINT, var_FIXEDPOINT, var_FLOATPOINT]

var_ITERABLE = [var_LIST, var_DICT, var_TUPLE]

var_TYPES = var_SCALAR + var_ITERABLE + [var_STRING]

## Log Parser Log-Line Keywords
## Verbs: 'parse', 'set', 'skip', 'noparse'
##
## 'parse'      : draw data from the log-line, processing it
## 'set'        : draw data from log-line spec, processing it
## 'skip'       : draw data from the log-line, discarding it
## 'noparse'    : do-nothing

parseLineID = "_p_LineID"

# unimplemented
# setLineIDOnCondition = _s_LineId@Condition
# a complex test of the line, if satisfied, confirms LineID

parseDatumName = "_p_DatumName"
parseDatum = "_p_Datum"

parseDatumfromList = "_p_Datum@List"
parseDatumNamefromList = "_p_DatumName@List"
parseLineIDfromList = "_p_LineID@List"

setDatumName = "_s_DatumName"
setDatumNamefromList = "_s_DatumName@List"
setDatumfromList = "_s_Datum@List"
setDatum = "_s_Datum"


## parse and confirm typed data
parseInt = "_p_I"
parseFixedPoint = "_p_FP"
parseTextWord = "_p_Txt"
skipText = "_s_Text"


skipTextWord = "_s_1Word"
skipTextWords = "_s_NWords"
skipUntilWordMatch = "_s_UntilMatch"
skipIncludingWordMatch = "_s_IncludeMatch"
skipDatumName = "_0_DatumName"

noparse = "_0_Datum"

error_ParseErrorReport = "_err_Report"

## Aggregation Phase Parse Specification
translateDatumfromList = "_x_Datum@List"


lineIDCommandSet = [ parseLineID, parseLineIDfromList ]

datumNameCommandSet = [ parseDatumName, parseDatumNamefromList, setDatumName]
datumNameOperantSet = [setDatumName, setDatumNamefromList, parseTextWord]

datumCommandSet= [ parseDatum, parseDatumfromList, setDatumfromList]
datumOperantSet = [ noparse, skipTextWord, skipTextWords, skipUntilWordMatch, setDatumfromList,
                  parseInt, parseFixedPoint, parseTextWord, skipText]

TXTOUT_ANY = 0x41
TXTOUT_UCASE = 0x42
TXTOUT_LCASE = 0x43
TXTOPS_ANY = 0x81
TXTOPS_UCASE = 0x82
TXTOPS_LCASE = 0x83
## NULL_ITEM is a formatting placement in an empty record
## None seemed OK, but causes problems in processing iterables
## so working with "None" string
#NULL_ITEM = 'x0x'
NULL_ITEM = None




