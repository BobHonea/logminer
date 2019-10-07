import thermreg_main as tlp
import mculog_data_sequence as ds

## instance the following sequences
##
##
## 1. Max A0 Sensors Temperature
## 2. Max A2-A8 Temperature
## 3. Max System Temperature
## 4. A0 & A2-8 Fan Speed + PWM
## 5. Overtemp Alerts
## 6. Temperature Alert
## 7. Fan Stopped/Slowed


## The Data Sequences are instanced at the start of parsing
##
## They are populated as relevant data records are emitted
## from the parser.
##
## A "DataSink" is registered with the dataDispatcher, so data
## relevant to the Data Sequence is routed to the DataSink, which
## builds records, confirms their sequence Id/Time and appends them
## to the Data Sequence.
##
## Each record type produces data for none to many sequences
##
## A handler will send the data to the sequences
##
## A Sequence descriptor is required for the handler to do its work
##
##


## TemperatureSequence ( DataSequence)
## the sequence is an ordinal.
## the data is a record of all temperature sensors
## <a0-a8 (local, remote)> [epm1 max] [epm2 max]
##
## sources:
#  a raw record is emitted from the LogParser in this format:
#  [ logLineSpec_key, [<datumName>, <datumValue>], .... }
#
#  1. fpgaTempSensorLogSpec  (per log line: local/remote A(n) temps)
#  2. maxEPMTempLogSpec      (per log line: Max Temp EPM(n)
#
#
#  datumValue(linerecord, datumName):
#
#  if logLineKey == fpgaTempSensorLogSpec_key and datumValue("fansocket") in list("fansocket_key")
#   if datum("fansocket") == "A0":
#       flush_pending_record
#       begin_new_record
#
#   then store list-start [ datum("fansocket"), datum("local temperature), datum("remote temperature") ]
#
# When the record is filled with expected data, it is closed, and
# a new instance is formed.
# When data arrives of a type already stored, the record is closed
# and the most recent data is used for whatever may be missing


## datumLocator class
#
## provides the location information for data in log records
## to the data sequence generators at "Registration Time"
## prior to log parsing, each sequence generator will have
## the set of records, and locations within each record of thier
## vital data located. With this information, extraction can
## proceed effectively.



class datumDispatch(object):
    ## push individual datum from log line records into
    ## Data Sequence Collectors registered for that data

    def __init__(self):
        pass


    def registerDatumSink(self, dataList ):
        return

    def registerDatumSource(self, dataList ):
        return




class datumLocator(object):

    def __init__(self):
        pass


    def registerDatumMap(self, record_key, item_index, datumName_subindex, datum_subindex):
        return

    def registerDatumMap1(self, record_key, item_index, datum_name, datum_subindex):
        return

    def registerDatumMap2(self, record_key, item_index, datum_name, datum_value):
        return




class TemperatureSequence (ds.sequencedData):

    def self.simpleDemandList = [ [ tlp.fpgaTempSensorLogSpec_key, [ tlp.fpgaFanSocket_key, tlp.fpgaFanSocket ]],\
                                  [ tlp.epm1MaxTempLogSpec_key, [ tlp.epm1MaxTemp ]],\
                                  [ tlp.epm1MaxTempLogSpec_key, [ tlp.epm2MaxTemp ]] ]


    self.tempDemandList = [ [tlp.fpgaTempSensorLogSpec_key, [ \
                                    ["A0", "local temperature"], ["A0","remote temperature"], \
                                    ["A2", "local temperature"], ["A2","remote temperature"], \
                                    ["A4", "local temperature"], ["A4","remote temperature"], \
                                    ["A6", "local temperature"], ["A6","remote temperature"], \
                                    ["A8", "local temperature"], ["A8","remote temperature"]]], \
                                [tlp.epm1MaxTempLogSpec_key, ["max epm1 temperature"]], \
                                [tlp.epm2MaxTempLogSpec_key, ["max epm2 temperature"]]]


    def dataFilter(self, logLine_key, datumName, datum):
#        logLineKey in
        return


    def __init__(self):
        self.source_records = [tlp.fpgaTempSensorLogSpec_key, tlp.maxEPMTempLogSpec_key]
        self.dataCollection =   [tlp.fpgaTempSensorLogSpec_key, tlp.fpgaFanSocket + tlp. ]
        self.sourceLogLineKeys = [[tlp.fpgaTempSensorLogSpec_key, tlp.fpgaFanSocket, ]]

        ##self.new_trigger = tlp.fpgaFanSocket[0]
        ##self.close_trigger = [tlp.maxEPMTempLogSpec_key, tlp.epmIdList[-1]]
        self.history = []
        return


    def set_data_locations(self):
        ## determine the location of the data inside their
        ## source data records. save for each record_key/datum:
        #   [record_key, item_index, label_subindex, datum subindex]
        #
        ## RETHINK:
        ## listing the uniquely defined data/keys, in order, in a format list
        ## defines the record.
        ## the record's data map will be the data name, and an enmeration of the data key
        ## a list of logLine keys will be used, and the index of each key is the enumeration
        ##
        for datum in self.data_types:
            pass
        return

    ### TO-BE_DONE
    ### ----------
    ### This class will inherit a DataSink Class
    ### the DataSink.processRecord() method will
    ### receive the parsed data from parser by way
    ### of the dispatchData class.


    ## the collector receives data records from the dispatch
    ## handler. the record is checked for a key match.
    ## on key match, data is moved from the reocord into the
    ## temp sequence record. The data may be a trigger to
    ## store+re-instance a record

    def collector(self,logLineKey, data_record):
        if logLineKey in self.source_records:
            if logLineKey == tlp.fpgaTempSensorLogSpec_key:
                pass

        return

