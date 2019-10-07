import thermreg_main as tlParse

#
#
#  This module holds the main() for reviewing the thermal test event/data
#   database(s) and testing for the following verification criteria
#
#   PASS-FAIL CRITERIA
#   ==================
#
#   Failure to meet **ANY** ofthese critera leads to TEST FAILURE
#
#    1. Alerts generated at Threshold and within Alert-Temp-Zone
#    2. Alerts withdrawn/not-reissued outside Alert-Temp-Zone
#    3. Fan speeds articulated according to:
#           Temperature Warning Criteria
#           Temperature Level Criteria
#           Fan Fault criteria
#
#   TESTER WARNING CRITERIA
#   =======================
#
#   1.  Sensor values are STATIC when other sensors are dynamic
#


# Test sketches
#
# FAN SPEED VERIFICATION
# ======================
# Review Temperature vs Sequence
# find Sequences bracketing FanSpeed change (increase/decrease) points
#
# ***CAUTION IN IMPLEMENTATION***
# The change points to increase and decrease are computed with hysteresis.
#
# verify that FanSpeed changes during or within a time-limit afterwards
#
#
# FAN ALERT VERIFICATION
# ======================
# Review Temperature vs Sequence
# find sequences bracketing Fan Alert, and Overtemperature Alert points (85C and 100C)
# Verify that Alerts are issued in brackets for each Alert
# Verify that Alerts are not issued, nor re-issued outside their brackets (lower temps)
#
# Review FanSpeed for each Fan
# Review Fan Speed vs PWM Setting for each Fan
# Verify that the Fan is turning at an appropriate speed
# Verify that a Fan Alert is issued of a Fan is static, or very slow
# Verify that the Fan Alert(s) withdraw(s) if contition is cured
#
#
# INTERBOARD COMMUNICATIONS
# =========================
# Review Interboard Comms Events
# Verify that Alerts and MaxTemp reports expected
# at FPGA board Log based on EPM board Logs do arrive
# and are accurately reported upon in time and content.
#


## Build Verification of Temperatures
## This test is for 'sanity check' of the temperature history
##
## DataSet needed:
##  all fpga and epm temperatures
##
## DataSink:  "tempCheck_sink"
##
## DataSink internal record:
##
##  trigger_startCollection on A0 temperature stats
##  trigger_endCollection on:
##          fullSystem:
##              all temperatures collected
##              next A8 temperature report
##                  which is both endCollection
##
##  collect data: fpgaTemperatureLogLine
##                  local/remote temps by fansocket
##                  epm1Max Temp
##                  epm2Max Temp
##
##  optional data: epm1Maxtemp, epm2MaxTemp depends
##                 on system configuration
##
##
tempSanityCheck_DataSink_key = "temperature sanity check"
tempSanityCheck_Demand = [ tlParse.fpgaTempSensorLogSpec_key,\
                           tlParse.epm1MaxTempLogSpec_key,\
                           tlParse.epm2MaxTempLogSpec_key]



class DataRecord(object):

    self.recordOnAllStored = "rec@allstored"
    self.recordOnRetrigger = "rec@retrigger"
    self.startRecordTrigger = "startTrigger@"
    self.startOnNamedValue = "start@Datum"
    self.setDataListItemCount = "setDListICount"
    self.storeRecordKey = "storeRecordKey"
    self.purgeOnError = "purge@Error"
    self.dataSetStart = "beginDataSet"
    self.dataSetEnd = "endDataSet"
    self.storeForEach = "storeListedData"
    self.storeDatum = "storeSingleDatum"
    self.postProcess = "beginPostProcess"
    self.postProcessEnd = "endPostProcess"
    self.selectMaxValue = "selectStore@Max"
    self.selectMinValue = "selectStore@Min"
    self.selectMaxListedValue = "selectStore@MaxListed"
    self.selectMinListedValue = "selectStore@MinListed"
    self.setDatumName = "setDatumName"



    def __init__(self):
        return

    def setRecordFormat(self, recordFormat):
        return

    def setLogLineList(self, logLines):
        return

    def processLogLineData(self, simpleRecord):
        return




# save all temperature values from all boards
# compute max and min temp values of record temps
# emit/initialize record on
#
tempSanityDataRecord = [ store_RecordKey, \
                         [[startRecord_trigger, startOnNamedValue, ["fansocket","a0"]],\
                         [retriggerOnRepeatValue],\
                         recordOnAllStored,\
                         recordOnRetrigger,\
                         purgeOnError,\
                         dataSetStart],\
                         [[storeForEach, tlParse.fpgaFanSocket],\
                         [storeValue, tlParse.epm1MaxTemp],\
                         [storeValue, tlParse.epm2MaxTemp],\
                         dataSetEnd,\
                         postProcess,\
                         [[setDataName, "MaxSystemTemp"],[store]],\
                         [[ setDataName, "MinSystemTemp"],[storeMinValue]]]]


