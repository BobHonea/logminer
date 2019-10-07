import mculog_parsetypes as pt

## Log Data Definitions
## in order to make sense of the source logs, the strings that identify
## values are saved in compact lists, defined by a shared meaning or context
##
## These lists are stored and referenced by a key string, or 'key'.
## This pattern of defining identities and lists and referencing them by a
## 'key' is adopted throughout this design.
##
epmSensorAddress = ["device 0x90 via bus 0", "device 0x90 via bus 1",
                    "device 0x94 via bus 0", "device 0x94 via bus 1"]
epmSensorAddress_key = "epmSensorAddress_key"

fpgaWarning = ["fan alert reported",
               "fan overtemperature reported",
               "epm1 alert reported",
               "epm2 alert reported",
               "epm1 overtemperature reported",
               "epm2 overtemperature reported",
               "fan failure reported",
               "fan a0 failure reported",
               "fan a2 failure reported",
               "fan a4 failure reported",
               "fan a6 failure reported",
               "fan a8 failure reported"]

fpgaWarning_key = "fpgaWarning_key"

fpgaFanSocket = ["a0", "a2", "a4", "a6", "a8"]
fpgaFanSocket_key = "fpgaFanSocket_key"

fanTachID = ["tach1", "tach2"]
fanTachID_key = "fanTach_key"

fanTachCountID = ["tach1 count", "tach2 count"]
fanTachCountID_key = "fanTachCount_key"

systemFanID = ["a2", "a4", "a6", "a8"]
systemFanID_key = "systemFanID_key"

## single item here, treated differently as multiple item contexts
## ... is this OK ?
fpgaFanID = "A0"

fanLogStatus = ["enabled", "disabled", "on", "off"]
fanLogStatus_key = "fanLogStatus_key"

epmLocalAlerts = ["over temperature", "alert"]
epmLocalAlerts_key = "epmLocalAlerts_key"

epmIdList = ["epm1", "epm2"]
epmIdList_key = "epmIdList_key"

epm1MaxTemp = "epm1MaxTemp"
epm2MaxTemp = "epm2MaxTemp"

fpgaSensorInfo = \
    [["a0", "u42", "u42", "fpga heatsink"],
     ["a2", "u93", "u93", "q46"],
     ["a4", "u109", "u109", "q26"],
     ["a6", "u??", "u??", "q??"],
     ["a8", "u7", "u7", "q3"]]

## Keywords occur at/near the start of raw log lines that
## are used to identify that log line to the Log Parser.
## These keys need to be relatively unique
epmTempSensorLogSpec_key = "read temperature from"
localEpmAlertLogSpec_key = "epm reports"
fanlogStatusLogSpec_key = "fan logs"
fanSpeedLogSpec_key = "device"
fanSpeedLogSpec2_key = "No Tach"
fanCmdLogSpec_key = "fan log"
fpgaTempSensorLogSpec_key = "sensor"
epm1MaxTempLogSpec_key = "max epm1 temperature"
epm2MaxTempLogSpec_key = "max epm2 temperature"
fanDutyCycleLogSpec_key = "fan"
fpgaWarningLogSpec_key = "warning"

fpgaSensorLocation = ["local temperature", "remote temperature"]
fpgaSensorLocation_key = "sensorlocation"

## RAW LOG LINE SPECIFICATIONS
##
## there is one "LogSpec" for each type of Log Textline from the
## system under test.
##
## mculog_parsetypes.py holds the definitions of the special keywords
## for the LogSpec implementations. They interpretation (definition)
## of these keywords is manifest in the Log Parser module: mculog_logparser.py
##
## LogSpec Definition: the Key ART of implementing a parser for any
## type of system log: Unless the system log was consciously designed
## to simplify the task of parsing and post-processing, the creative
## involvement of the post-processing engineer is engaged to identify
## strategies for consistently and accurately extracting the reported
## values from the source log text.
##
## BY FAR, the most consuming task in this process is the definition of
## of each LogSpec, one for each unique type of system log string. However,
## once a suitable set of LogSpecs has been defined, success of the
## Log Parser is guaranteed.
##
##
##
## Each LogSpec, as well as each raw log line has:
## 1. 1 Line ID word/phrase
## 2. 1..N datumValues (datum: single unit of data)
##     2.1: Commonly, datumValues are always preceded by a portion of the
##          log string that can be adopted as a "datumName"
##     2.2: Some datumValues do not have an identifiable datumName in the
##          source log text, and one is assigned in the process of parsing.
##
##
##
## this is the encoding of the syntax of the RAW LOG LINES
## RAW LOG LINES: lines as they are emitted by the system under test
## these logs are defined by developers for their needs, and may change
## with some frequency...
##
## FLEXIBILITY OF DESIGN as a defense
## for this reason, this engine is defined to support rapid modification
## by editing data tables, and close checking of the data to root out
## sudden changes in the log stream, or its syntax encoding.


# ****************************
### BEGIN LOGSPEC DEFINITIONS
# ****************************

epmTempSensorLogSpec = \
    [[pt.parseLineID, epmTempSensorLogSpec_key],
     [[pt.parseDatumNamefromList, epmSensorAddress_key],
      [pt.parseDatum, pt.parseFixedPoint]]]

localEpmAlertLogSpec = \
    [[pt.parseLineID, localEpmAlertLogSpec_key],
     [[pt.setDatumName, 'epm reports'], [pt.parseDatumfromList, epmLocalAlerts_key]]]

fanCmdLogSpec = \
    [[pt.parseLineID, fanCmdLogSpec_key],
     [[pt.setDatumName, "fan log"], [pt.parseDatumfromList, fanLogStatus_key]]]

fanlogStatusLogSpec = \
    [[pt.parseLineID, fanlogStatusLogSpec_key],
     [[pt.setDatumName, "fan log status"], [pt.parseDatumfromList, fanLogStatus_key]]]

fanSpeedLogSpec = \
    [[pt.parseLineID, fanSpeedLogSpec_key],
     [[pt.setDatumName, "fansocket"], [pt.parseDatumfromList, fpgaFanSocket_key]],
     [[pt.parseDatumNamefromList, fanTachCountID_key], [pt.parseDatum, pt.parseInt]],
     [[pt.parseDatumName, "rpm"], [pt.parseDatum, pt.parseInt]]]

fanSpeedLogSpec2 = \
    [[pt.parseLineID, fanSpeedLogSpec2_key],
     [[pt.skipDatumName, pt.noparse], [pt.skipText, "value as device"]],
     [[pt.setDatumName, "fansocket"], [ pt.parseDatumfromList, fpgaFanSocket_key]],
     [[pt.setDatumName, "tach1"],[pt.setDatum, "0" ]],
     [[pt.setDatumName, "rpm"], [ pt.setDatum, "0"]]]



fpgaTempSensorLogSpec = \
    [[pt.parseLineID, fpgaTempSensorLogSpec_key],
     [[pt.setDatumName, "fansocket"], [pt.parseDatumfromList, fpgaFanSocket_key]],
     [[pt.parseDatumNamefromList, fpgaSensorLocation_key], [pt.parseDatum, pt.parseFixedPoint]],
     [[pt.skipDatumName, pt.noparse], [pt.skipText, "deg c"]],
     [[pt.parseDatumNamefromList, fpgaSensorLocation_key], [pt.parseDatum, pt.parseFixedPoint]]]

maxEPM1TempLogSpec = \
    [[pt.parseLineID, epm1MaxTempLogSpec_key],
     [[pt.setDatumName, epm1MaxTemp], [pt.parseDatum, pt.parseFixedPoint]]]

maxEPM2TempLogSpec = \
    [[pt.parseLineID, epm2MaxTempLogSpec_key],
     [[pt.setDatumName, epm2MaxTemp], [pt.parseDatum, pt.parseFixedPoint]]]

fanDutyCycleLogSpec = \
    [[pt.parseLineID, fanDutyCycleLogSpec_key],
     [[pt.setDatumName, "fansocket"], [pt.parseDatumfromList, fpgaFanSocket_key]],
     [[pt.parseDatumName, "duty cycle"], [pt.parseDatum, pt.parseInt]],
     [[pt.parseDatumName, "pwm"], [pt.parseDatum, pt.parseInt]]]

fpgaWarningLogSpec = \
    [[pt.parseLineID, fpgaWarningLogSpec_key],
     [[pt.setDatumName, "fpga warning"], [pt.parseDatumfromList, fpgaWarning_key]]]

epmLocalLogMessages = \
    [epmTempSensorLogSpec, fanlogStatusLogSpec, fanCmdLogSpec, localEpmAlertLogSpec]

fpgaLogMessages = \
    [fanSpeedLogSpec, fpgaTempSensorLogSpec, maxEPM1TempLogSpec,
     maxEPM2TempLogSpec, fanDutyCycleLogSpec, fanCmdLogSpec, fanlogStatusLogSpec,
     fpgaWarningLogSpec]

## END LOGSPEC DEFINITIONS

## PARSED LOG SPECIFICATIONS
## Hah! I lied!!
## After you define the Log Specs (see above) YOU ARE NOT DONE!!
## You have, also, to translate from the LogSpec format into an intermediate
## format named the 'ParseSpec'.
##
## It is FAR EASIER to draw up a ParseSpec from the LogSpec. In fact:
## TODO: automate the generation of ParseSpecs. It is doable.
##
## The ParseSpec is a description of the output of the LogParser
## this intermediate output form is consumed by the 'database' record
## aggregator, which samples data that is relevant to any specific analytic
## task into a single record, an aggregated record.
##
## The aggregator requires to know what is in the results of any string
## parsed by the LogParser, so it can sample from the labeled data what the
## end-use database needs. Bear in mind that the results of parsing might be
## a single database, or it might be a collection of purpose-defined databases.
##
## It is up to the consumer of the database to decide whether throwing everything
## into one database, or into a collection of databases suits their task(s).
##
##
################## BEGIN - PARSED LOG LINE SPEC TEMPLATES ##################


fanCmdParseSpec = \
    [[pt.parseLineID, fanCmdLogSpec_key],
     ["fan log", pt.var_STRING]]

fanlogStatusParseSpec = \
    [[pt.parseLineID, fanlogStatusLogSpec_key],
     ["fan log status", pt.var_STRING]]

fpgaTempSensorParseSpec = \
    [[pt.parseLineID, fpgaTempSensorLogSpec_key],
     ["fansocket", pt.var_STRING],
     ["local temperature", pt.var_FIXEDPOINT],
     ["remote temperature", pt.var_FIXEDPOINT]]

maxEPM1TempParseSpec = \
    [[pt.parseLineID, epm1MaxTempLogSpec_key],
     [epm1MaxTemp, pt.var_FIXEDPOINT]]

maxEPM2TempParseSpec = \
    [[pt.parseLineID, epm2MaxTempLogSpec_key],
     [epm2MaxTemp, pt.var_FIXEDPOINT]]

fanDutyCycleParseSpec = \
    [[pt.parseLineID, fanDutyCycleLogSpec_key],
     ["fansocket", fpgaFanSocket_key],
     ["duty cycle", pt.var_INT],
     ["pwm", pt.var_INT]]

##### PARSE SPECS TO MATCH AND RENAME AGAINST A LIST ####

localEpmAlertParseSpec = \
    [[pt.parseLineID, localEpmAlertLogSpec_key],
     [[pt.translateDatumfromList, epmLocalAlerts_key], pt.var_STRING]]

##### PARSE SPECS TO MATCH AGAINST A LIST #####

epmTempSensorParseSpec = \
    [[pt.parseLineID, epmTempSensorLogSpec_key],
     [epmSensorAddress_key, pt.var_STRING],
      [pt.parseDatum, pt.var_FIXEDPOINT]]

fpgaWarningParseSpec = \
    [[pt.parseLineID, fpgaWarningLogSpec_key],
     [fpgaWarning_key, pt.var_STRING]]

fanSpeedParseSpec = \
    [[pt.parseLineID, fanSpeedLogSpec_key],
     ["fansocket", pt.var_STRING],
     [fanTachCountID_key, pt.var_INT],
     ["rpm", pt.var_INT]]

fanSpeedParseSpec2 = \
    [[pt.parseLineID, fanSpeedLogSpec2_key],
     ["fansocket", pt.var_STRING],
     [fanTachCountID_key, pt.var_INT],
     ["rpm", pt.var_INT]]
################## END - PARSED LOG LINE SPEC TEMPLATES ##################
