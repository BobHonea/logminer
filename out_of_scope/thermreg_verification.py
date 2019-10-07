import mculog_data_sequence as ds
import thermreg_main as tlp
import thermreg_log_specification as tld

## review the data in the collections against the
## Verification constraints
##
## 1. Fan Speed Threshold Hysteresis
##      a) for fan A0 (fpga sensor driven)
##      b) for fans A2, A4, A6, A8  (system sensor driven)
##
## 2. Fan Speed vs Temp Transition
## 3. Temperature Alerts
##      a) fpga at/over 85C
##      b) fpga at/over 100C
##      c) EPM1/2 at/over 85C
##      d) EPM1/2 at/over 85C
##
## 4. fpga temperature sensors dynamic
##      a) temperature change follows system trends
##      b) temperature does change
##
## 5. In the absence of system Alerts: the fpga Heatsink
##    fanspeed is independent of the system fan's speed
##    i.e. fanspeed fan a0 dependent only on sensors
##    connected to fan-driver a0 (fpga Heatsink, Q3)
##


##
## data sets needed:
##  temp vs fanspeed -> Fanspeed Transition Temp Hysteresis
##      temp data set
##      fanspeed data set
##
##  events vs temp vs fanspeed -> Fanspeed Transitions on temp and event
##
##


## Data Stores for Temperatures, Events, and Fan Status
##


fanlogControlLogLines = [tld.fanCmdLogSpec_key, tld.fanlogStatusLogSpec_key]

eventLogLines = [tld.fpgaWarningLogSpec_key, tld.localEpmAlertLogSpec_key]

fanStatusLogLines = [tld.fanDutyCycleLogSpec_key, tld.fanSpeedLogSpec_key]
temperatureLogLines = [tld.epmTempSensorLogSpec_key, tld.epm1MaxTempLogSpec_key,
                       tld.epm2MaxTempLogSpec_key, tld.fpgaTempSensorLogSpec_key]

alertSequence = ds.sequencedData(ds.compareNumber)
fanStatusSequence = ds.sequencedData(ds.compareNumber)
eventSequence = ds.sequencedData(ds.compareNumber)
ignoredSequence = ds.sequencedData(ds.compareNumber)
fpgaTemperatureSequence = ds.sequencedData(ds.compareNumber)
epm1TemperatureSequence = ds.sequencedData(ds.compareNumber)
epm2TemperatureSequence = ds.sequencedData(ds.compareNumber)
avepmTemperatureData = ds.sequencedData(ds.compareNumber)
avepmMaxTempData = ds.sequencedData(ds.compareNumber)
avepmEventData = ds.sequencedData(ds.compareNumber)
fpgaBoardMaxTempData = ds.sequencedData(ds.compareNumber)
fpgaHeatsinkMaxTempData = ds.sequencedData(ds.compareNumber)
systemMaxTempData = ds.sequencedData(ds.compareNumber)


def simpleRecordInput(self, thisRecord):
    # replace lineID parse-code with sequence#
    self.thisRecord = thisRecord
    lineID = thisRecord[0][1]

    if lineID in temperatureLogLines:
        # keep lists of temp data
        # a0 - the Heatsink Fan Driver has a different
        # algorithm than [a2, a4, a6, a8]. Maintain seperate
        # max Temp values.
        # a0 Max, a2-8 Max, Epm1 Max, Epm2 Max, Set Max
        #
        if lineID == tld.epmTempSensorLogSpec_key:
            ## add to epm1 Temp Sequencer
            epm1TemperatureSequence.appendSequencedDatum(
                self.nextSequenceNumber(),
                [thisRecord[1][1],
                 thisRecord[2][1]])
        else:
            ## temperatures logged to fpga/system temperature
            ## database

            if lineID in [tld.epm1MaxTempLogSpec_key, tld.epm2MaxTempLogSpec_key]:
                self.addTempToaggregateRecord(lineID, thisRecord[1][0], thisRecord[1][1])
                pass

            elif lineID == tld.fpgaTempSensorLogSpec_key:
                ## FansocketID, localTemp, remoteTemp
                fansocket = thisRecord[1][1]
                localLabel = fansocket + "l"
                remoteLabel = fansocket + "r"
                localTemp = thisRecord[2][1]
                remoteTemp = thisRecord[3][1]
                self.addTempToaggregateRecord(lineID, localLabel, localTemp)
                self.addTempToaggregateRecord(lineID, remoteLabel, remoteTemp)
                pass


pass


class dataAggregator(object):

    tempRecord = None
    NULL_ITEM = None

    temperatureSequence_key = "tempSequence_key"
    fanSpeedSequence_key = "fanSpeedSequence_key"
    fanDriveSequence_key = "fanDriveSequence_key"

    fpgaTempSensorLogLineLabels = [tld.fpgaTempSensorLogSpec_key, "fansocket", "local_temperature",
                                   "remote_temperature"]
    epm1MaxTempLogLineLabels = [tld.epm2MaxTempLogSpec_key, "epm1MaxTemp"]
    epm2MaxTempLogLineLabels = [tld.epm2MaxTempLogSpec_key, "epm2MaxTemp"]

    aggregateRecordKeys = ["a0", "a2", "a4", "a6", "a8", "epm1MaxTemp", "epm2MaxTemp"]
    fpgaLocalTempSensorLabel = ["U42", "U93", "U109", "U46", "U7"]
    aggregateRecordIDs = ["a0l", "a2l", "a4l", "a6l", "a8l",
                          "a0r", "a2r", "a4r", "a6r", "a8r",
                          "epm1MaxTemp", "epm2MaxTemp"]
    fpgaRemoteTempSensorLabel = ["FPGA_HEATSINK", "U93", "U109", "U46", "U7"]
    aggregateRecordLabels = ["U42", "U93", "U109", "U46", "U7"
                                                          "FPGA HEATSINK", "Q46", "Q49", "Q26", "Q3",
                             "EPM1_MAX", "EPM2_MAX"]

    epmBus1TempSensorLabel = ["U60", "U61", "U62", "U63"]
    epmTempRecordKeys = ["0x90bus0", "0x90bus1", "0x94bus1", "0x94bus2"]

    # FPGA LOCAL Temp Info
    FPGABoard_MaxTemp = None
    FPGABoard_MaxTemp_Sensor = None

    # EPM REMOTE Temp Info
    EPM1_ReportedMaxTemp = None
    EPM2_ReportedMaxTemp = None
    # EPM LOCAL Temp Info
    EPM1_MaxTempSensor = None
    EPM1_MaxTemp = None

    sequenceNumber = None
    epmMaxTemp_detected = False
    fpgaTemp_detected = False
    maxSystemTemperature = None
    maxSystemTempSensor = None

    # epm reports may not occur, but come immediately before reports from
    # sensor a2, which otherwise would be the first report after a 10s gap
    # U42 is the remote (2nd reported) sensor for a0, which is the last
    # sensor temperature report during the 10s update.

    aggregateRecordStartTrigger = ["EPM1_MAX", "EPM2_MAX", "Q46"]
    aggregateRecordFlushTrigger = ["U42"]

    # scenarios:
    # 1. initial trigger lines are missing
    #   COMMON!
    #   can happen on any log where log is not
    #   started before log-streaming begins
    # 2. final data lines are missing
    #   COMMON!
    #   can happen at end of file, or when user
    #   stops/restarts log
    # 3. all datalines are present and in order
    #   COMMON!
    #   expected, but not guaranteed
    # 4. data lines are disordered:
    #   BEYOND RARE:
    #   nothing to do about this...not likely in natural
    #   execution

    def __init__(self):
        self.sequenceNumber = 0
        self.maxTemperature = None
        self.maxTempSensor = None
        self.maxTempRecordItems = len(self.aggregateRecordLabels)
        self.validRecordItems = 0
        # self.fanDriveSequence = ds.sequencedData(ds.compareNumber)
        # self.fpgaTempSequence = ds.sequencedData(ds.compareNumber)
        self.fanSpeedSequence = ds.sequencedData(ds.compareNumber)
        return

    def nextSequenceNumber(self):
        self.sequenceNumber += 1
        return self.sequenceNumber

    def recordIsFull(self, recordKey):
        return self.NULL_ITEM not in self.aggregateRecord or \
               self.aggregateRecordValidItems == self.maxTempRecordItems

        pass

    def getValueIndexByType(self, valueType, record_key):
        if record_key == tld.fpgaTempSensorLogSpec_key:
            pairIndex = self.fpgaTempSensorLogLineLabels.index(valueType)
            return pairIndex
        raise ValueError

    def getRecordValueByType(self, valueType):
        pairIndex = self.getValueIndexByType(valueType)
        return self.thisRecord[pairIndex, 1]

    def newaggregateRecord(self):
        # define list as full of None
        keyCount = len(self.aggregateRecordLabels)
        self.aggregateRecord = keyCount * self.NULL_ITEM
        self.aggregateRecordValidItems = 0
        self.aggregateRecordDirty = False
        return

    def emitaggregateRecord(self):
        # send a temp record to the temp data sequencer
        fpgaTemperatureSequence.appendSequencedDatum(self.sequenceNumber,
                                                     self.aggregateRecord)
        return

    def addTempToaggregateRecord(self, lineID, tempID, tempValue):

        ###############################################
        ## TODO: this is S...L...O...W, speedup later #
        ###############################################

        tempIndex = self.aggregateRecordIDs.index(tempID)

        if (self.validRecordItems == self.maxTempRecordItems) or \
                (self.aggregateRecord[tempIndex] != self.NULL_ITEM):
            # data collission: emit record
            # record filled: emit record
            self.emitaggregateRecord()
            self.newaggregateRecord()

        tempValue = self.aggregateRecordLabels[tempIndex]
        self.aggregateRecord[tempIndex] = [self.aggregateRecordLabels[tempIndex], tempValue]
        self.aggregateRecordDirty = True
        self.aggregateRecordValidItems += 1

        return

    def simpleRecordInput(self, thisRecord):

        # replace lineID parse-code with sequence#
        self.thisRecord = thisRecord
        lineID = thisRecord[0][1]

        if lineID in temperatureLogLines:
            # keep lists of temp data
            # a0 - the Heatsink Fan Driver has a different
            # algorithm than [a2, a4, a6, a8]. Maintain seperate
            # max Temp values.
            # a0 Max, a2-8 Max, Epm1 Max, Epm2 Max, Set Max
            #
            if lineID == tld.epmTempSensorLogSpec_key:
                ## add to epm1 Temp Sequencer
                epm1TemperatureSequence.appendSequencedDatum(
                    self.nextSequenceNumber(),
                    [thisRecord[1][1],
                     thisRecord[2][1]])
            else:
                ## temperatures logged to fpga/system temperature
                ## database

                if lineID in [tld.epm1MaxTempLogSpec_key, tld.epm2MaxTempLogSpec_key]:
                    self.addTempToaggregateRecord(lineID, thisRecord[1][0], thisRecord[1][1])
                    pass

                elif lineID == tld.fpgaTempSensorLogSpec_key:
                    ## FansocketID, localTemp, remoteTemp
                    fansocket = thisRecord[1][1]
                    localLabel = fansocket + "l"
                    remoteLabel = fansocket + "r"
                    localTemp = thisRecord[2][1]
                    remoteTemp = thisRecord[3][1]
                    self.addTempToaggregateRecord(lineID, localLabel, localTemp)
                    self.addTempToaggregateRecord(lineID, remoteLabel, remoteTemp)
                    pass

    pass
