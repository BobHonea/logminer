
import mculog_logparser as logP
import mculog_data_sequence as ds

## class DataSink(sequencedData)
##
## this implies that every DataSink extends from sequencedData object
## A sequencedData object is a searchable list of records, a database.
## Ultimately, a dataSink's input must route somewhere, and most likely,
## if not certainly, to sequencedData. However, there may be intermediate
## dataSinks which collect from other dataSources.
##
## DEFINITION: A DataSink is a the required interface for a receiver
## of information directly from a data dispatcher object.
##
## Since it is an interface, and inheritable, it may be a component of
## any data consuming object, such as an analyzer, database, trigger, etc.
##

##
class dataSink(ds.sequencedData):

    thisSink_key = None
    thisDemand_key = None
    thisRecord_key = None
    valid = False

    def __init__(self, dataSink_key, dataDemand_key, dataRecord_key):
        self.thisSink_key = dataSink_key
        self.thisDemand_key = dataDemand_key
        self.thisDataRecord_key = dataRecord_key
        self.logLines = logP.keyedList()

        if not self.verifyDemand():
            raise ValueError

        if not self.verifyRecord():
            raise ValueError

        self.valid = True
        return


    def isValid(self):
        return self.valid

    ##
    ## hold the data from the record
    ## process record_start, record_complete triggers
    ## fill out a sequencedData Record compiled from the dataRecord Set
    def processRecord(self, logLine_key, dataRecord):
        if not self.isValid():
            raise ValueError

        return




class dispatchData(object):
    ## datum dispatch will send data to a DataSequencer by way of
    ## .... TBD

    ## sink dispatch record: [ dataSequencer&, datumNamelist ]
    ##
    ##
    ## source dispatch record
    ## list of [logline_key, datumName
    ##
    ## list of sourced data
    ## list of demanded sourced data
    ## list of registered sink routes
    ##
    ## phase 0: test runner instantiates logLineParser, registers Log Lines
    ##          and datum names and types which populate the logLines.
    ##          at the end of this phase, the parser can parse and generate
    ##          datumName/datum records to a raw output source
    ##
    ## phase 1: test runner instantiates data manager
    ##          data manager instantiates dataSequencers (data collectors)
    ##          data manager operates dataSequencers to register as dataSinks
    ##          data manager operates dataSequencers to register their dataDemands
    ##          at the end of this phase, dataSinks are in place to receive
    ##          datumName/datum records and format them into temporary databases/lists
    ##
    ## phase 2: test runner instantiates validation manager
    ##          the rest is TBD.
    ##
    ## t0: log lines are registered, the list of sourceable data is built up.
    ## t2: all log lines have been registered
    ##      data sink registration is signalled
    ##      an invocation of the datasequencer startup is made,
    ##      triggering the sequencers to register demands with the dispatcher.
    ## t3:
    ## the sequencer will reserve data sources until
    ## the full set needed is reserved. Then the sequencer
    ## will commit the demand.
    ## if the full demand cannot be reserved, then the
    ## sequencer will withdraw the demand, and raise an
    ## exception.
    ##
    ## This rollback permits debugging/refactoring/testing
    ## with implementations-in-progress


    DATUM_AVAILABLE = 1
    DATUM_DEMANDED = 2
    DATUM_CONTRACTED = 3
    DATAREQ_REGISTERED = 1
    DATAREQ_PART_AVAILABLE = 2
    DATAREQ_FULL_AVILABLE = 3


    DATAREQ_LOGKEY_INDEX = 0
    DATAREQ_DATUMNAME_INDEX = 1

    DISPATCHSTATE_NONE = 0
    DISPATCHSTATE_LOGPARSER_INSTANCED = 1
    DISPATCHSTATE_DATASINKS_INSTANCED = 2
    DISPATCHSTATE_DATASOURCE_REGISTRATION = 3
    DISPATCHSTATE_DATASINK_REGISTRATION = 4
    DISPATCHSTATE_ROUTING_DISPATCH = 5
    DISPATCHSTATE_ROUTING_ENABLED = 6
    DISPATCHSTATE_ROUTING_DISABLED = 7


    dlp = logP.logLineParser()

    def __init__(self, LogParser : logP.logLineParser):
        self.dataSource = logP.keyedList()
        self.dataSink = logP.keyedList()
        self.dataDemandBlocks = logP.keyedList()
        self.logParser = LogParser
        self.dispatchState = self.DISPATCHSTATE_NONE
        return


    def signalLogParserInstanced(self, logParser):
        if self.dispatchState == self.DISPATCHSTATE_NONE:
            self.dispatchState = self.DISPATCHSTATE_LOGPARSER_INSTANCED
        else:
            raise RuntimeError
        return

    def signalBeginDataSinkRegistration(self):
        if self.dispatchState == self.DISPATCHSTATE_LOG:
            self.dispatchState = self.DISPATCHSTATE_DATASINK_REGISTRATION
        else:
            raise RuntimeError


    def signalBeginDataSourceRegistration(self):
        if self.dispatchState == self.DISPATCHSTATE_DATASINK_REGISTRATION:
            self.dispatchState = self.DISPATCHSTATE_DATASOURCE_REGISTRATION

        return

    def signalEndDataSourceRegistration(self):
        return



    def signalendDataSinkRegistration(self):
        return

    def SignalBeginDataDemandRegistration(self):
        return

    def signalEndDataDemandRegistration(self):
        return


    def registerDataSource(self, logLine_key, datumName):
        #####################################################
        ## register logline keys in a list as sources      ##
        #####################################################

        if self.dispatchState != self.DISPATCHSTATE_DATASOURCE_REGISTRATION:
            raise RuntimeError

        if self.dataSink.getEntry(logLine_key):
            raise ValueError

        return self.dataSink.addEntry(logLine_key)


    def registerSinkDemand(self, dataSink_key, dataDemandList):
        ######################################################
        ## a Demand Block: a list of LogLine Records Req'd. ##
        ######################################################
        ## each request lists the logLine_Keys, identifying
        ## the log line type sourcing the data
        #
        #
        # Thoroughly check each Data Sink Demand for consistency
        # before registering the Demand
        ########################################################

        if self.dispatchState != self.DISPATCHSTATE_DATASINK_REGISTRATION:
            raise RuntimeError

        if not self.dataSink.entryExists(dataSink_key):
            ##invalid dataSink
            raise ValueError


        for DemandIndex in range (0, len(dataDemandList)):
            ## verify Demand Block is properly formed
            ## referring to existing entities
            thisLogLineKey = dataDemandList[DemandIndex]
            if not self.dataSource.entryExists(thisLogLineKey):
                raise ValueError

        ## No Collision testing..
        self.dataSink.addEntry(dataSink_key, dataDemandList)
        return

    def dataSinkRegistered(self, dataSink_Key):
        return (self.dataSink.getEntry(dataSink_Key) is not None)


    def registerDataSink(self, dataSink_key, ):
        return

    def dispatchDatum(self, datumName, datumValue):
        return

    def recordReady(self):
        # drive dispatch state machine
        # each time a record is ready call is made here
        # verify the proper state for dispatch


        if self.dispatchState == self.DISPATCHSTATE_NONE:
            raise ValueError
        elif self.dispatchState == self.DISPATCHSTATE_LOGPARSER_INSTANCED:
            # begin registration of ....
            return

        elif self.dispatchState == self.DISPATCHSTATE_DATASOURCE_REGISTRATION:
            return

        elif self.dispatchState == self.DISPATCHSTATE_DATASINK_REGISTRATION:
            return

        elif self.dispatchState == self.DISPATCHSTATE_ROUTING_ENABLED:
            return

    def dispatchRecord(self, simpleRecord):
        # Simple Record has this format:
        #
        # 1. LineID item:       [ lineID type key, lineID ]
        # 2..N Datum(n) :       [ datumName, datum ]
        #
        # drive the dispatch state machine while dispatching
        # simple records (the heartbeat) input to this dispatch object
        #




        return