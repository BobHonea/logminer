import mculog_data_sequence as ds
import mculog_debug as du
import mculog_parsetypes as pt
import mculog_utility as mcutil
import collections as coll


## the dataAggregator captures parsed log data and
## blends data from a single or multiple log line types
## into a single record for storage with a dataSequence
##
## the data can be looked up by an analyzer through the
## dataSequence
##


##
## at construction, the object receives defining information for the
## record to be produced, and the set of 'parsed log lines' from which
## the record data will be drawn.
##
## in the process of drawing data from the source 'parsed log lines',
## data labels of the log lines are used. However, in creating and
## referencing the product record (via the data sequencer), a different
## set of labels may be created/used... as more relevant to the task
## of the program/modules that analyze and present the aggregated data.
##

## aggregation is to draw things together
## and that may be from different sources, as well as only partial
## extracts from some of these sources.
## a design for extracting some values from selected log lines
## is necessary.
##
## a list of log lines sourced by the aggregator is needed
## a map/list of data values drawn from each selected log line
## is correspondingly needed.
##
## The sourcing map is a list with a first element being the
## logLine ID, and following elements being the labels of the
## values to be aggregated/drawn from the log line
## the sourcing map for a single aggregator may be several
## log line sourcing maps.
##
## The input for the aggregator is the output of the LogLineParser
## while the LogLineSpecification the parser uses to parse raw logs
## does not contain the explicit labels of the generated data,
## the parsed log line records/lists DO come as lists of [ 'label', value ] pairs.
####
#### THIS IS TRUE ( label-value pairs are definite, not variable definitions)
#### .... because Aggregation draws specific value-data pairs only
####
## 2 item lists. *** the PARSED LOG LINE SPECIFICATION *** is used
## when defining the input for aggregation, not the complex log line spec
## which is checked and used by the Log Line Parser.
##



## Aggregation Storage Control
##
## a collection of data that conditions when and if the aggregation record buffer
## is stored to the associated database/dataSequence
##
## define this tuple in your aggregation configuration section, once for each
## aggregator. Submit as an argument to instantiate.
##
## FirstDatum, if not None, nor '':
##      Trigger a storage the aggregation buffer prior to saving datum at this
##      label position.
##
## LastDatum, if not None nor '':
##      Trigger storage of the aggregation buffer subsequent to storing datum
##      at this label position.
##
## StoreOnCollision:
##      Trigger storage of ... when write of the current datum would
##      OVERWRITE datum already in the aggregation record buffer.
##
## StoreOnFull:
##      Trigger storage of aggregation buffer when all positions in the buffer
##      have been updated.
##
##
AggregationStorageControl = coll.namedtuple('AggregationStorageControl',
                                               'FirstDatum, LastDatum, StoreOnCollision, StoreOnFull, StoreIfEmpty')


class dataAggregator(object):
    class sourceMap(object):
        class valueMap(object):
            recordLabel = None
            logLabel = None
            variantFilter = None
            valueIndex = None
            translateFromList = None

            def __init__(self, record_label, log_label, variant_filter, value_index,
                                translateFromList=False):
                self.recordLabel = record_label
                self.logLabel = log_label
                self.translateFromList = translateFromList
                self.variantFilter = variant_filter
                self.valueIndex = value_index
                return

        pass

        parsedLogLineSpec = None
        logLine_key = None
        lineVariantMaps = None
        recordLabels = None
        valueMapList = None
        recordSize = None
        valueLabels = None
        mappedValueCount = None
        fetchIndex = None
        vmapFetchIndex = None
        valueLabelCount = None


        def __init__(self, recordLabelList, logLineAggregationMap, appRegistry:mcutil.applicationRegistry):
            ## for a single Log Line Type (logLineID)...
            ## produces compact data for mapping values between
            ## parsed log lines and aggregated records
            ## consumes per-log-line variable maps

            self.parsedLogLineSpec = list(logLineAggregationMap[0])
            #            self.logLine_key = self.parsedLogLineSpec[1]
            self.lineVariantMaps = logLineAggregationMap[1]
            self.recordLabels = recordLabelList

            self.appRegistry = appRegistry
            self.idListKeys = self.appRegistry.get_idListKeys()

            self.valueMapList = []
            self.recordSize = len(self.recordLabels)
            self.mappedValueCount = 0
            self.vmapMaxFetchIndex = None
            self.vmapFetchIndex = None
            self.valueLabelCount = len(self.recordLabels)
            self.mapValues()
            self.displayValueMapContents()
            return

        def getValueMapOK(self):
            if self.vmapFetchIndex == None or self.vmapMaxFetchIndex == None:
                return False


            return (self.vmapFetchIndex  <= self.vmapMaxFetchIndex)

        def getValueMap(self) -> valueMap:
            # return True if vmapFetchIndex locates a valid vMap
            if self.vmapFetchIndex <= self.vmapMaxFetchIndex:
                return self.valueMapList[self.vmapFetchIndex]

            du.showFaultInfo("index out of range")
            raise ValueError

        def getNextValueMapOK(self):
            # return True if getNextValueMap() will succeed
            return (self.vmapFetchIndex + 1 <= self.vmapMaxFetchIndex)

        def getNextValueMap(self) -> valueMap:
            if self.getNextValueMapOK():
                self.vmapFetchIndex += 1
                return self.getValueMap()
            raise ValueError

        def getFirstValueMap(self) -> valueMap:
            self.vmapFetchIndex = 0
            if self.getValueMapOK():
                return self.getValueMap()

            du.showFaultInfo("index out of range")
            raise ValueError

        def getMappedValueCount(self):
            return self.mappedValueCount

        def displayValueMapContents(self):
            self.vmapFetchIndex = 0

            if not self.getValueMapOK():
                print("No Value Maps To Print")
                return

            vmap = self.getFirstValueMap()

            while True:

                print("valueMap[" + str(self.vmapFetchIndex) + "]: " + vmap.recordLabel + "  index=" + str(
                    vmap.valueIndex) + \
                      "  " + repr(vmap.variantFilter))

                if self.getNextValueMapOK():
                    vmap = self.getNextValueMap()

                else:
                    break

                continue

            return

        # ParseSpec = coll.namedtuple('ParseSpec', 'lineIdSpec, DatumSpecs')

        # Build a map for each variant of a log line
        # The line variant set is an input
        # Each variant has the same lineID - line identifier
        # Each variant measures for a unique sensor, or reports a unique message
        # Specifically: the measure from each variant is reported in a different
        #               position in the aggregated record.
        #
        # task: for each variant - recognize which lineID is used, build a
        #       template for recognizing this variant on-the-fly during
        #       record aggregation. this template is a 'map'
        #

        def mapValues(self):
            LineVariant = coll.namedtuple('LineVariant', 'filter, rawlabels, recordlabels')
            #parseSpec = ParseSpec(lineIdSpec=self.parsedLogLineSpec[0], datumSpecs=self.parsedLogLineSpec[1])


            for lineVariant in self.lineVariantMaps:
                thisVariant = LineVariant(filter = lineVariant[0], rawlabels=lineVariant[1], recordlabels=lineVariant[2])

                for recordLabel in thisVariant.recordlabels:
                    # rawLabel is the label for a value from the log text
                    # variantFilter is typically the initial item pair in the log line
                    # the variant filter CAN be from a different position
                    # a "*" filter accepts every variant presented


                    labelIndex = thisVariant.recordlabels.index(recordLabel)
                    rawLabel = thisVariant.rawlabels[labelIndex]
                    variantFilter = thisVariant.filter


                    # find value location in parsed line spec
                    # original label is the first element of a label:value pair
                    # match the original label, use index info for map

                    ## in the case that a field has a 'variable label',
                    ## the list of legal labels is included in the DataPair's
                    ## 'label' position in the parse spec. process accordingly


                    # the first sub-list in the parsed line spec has the lineID info
                    # loop on the remaining sub-items in the line spec to identify
                    # data labels to assign to newly created value maps.
                    for datumSpecIndex, item in enumerate(self.parsedLogLineSpec[1:],1):

                        #test if item[0] is a list_key
                        #fetch labelList from appRegistry with key

                        if type(item[0]) == list:
                            if len(item) != 2:
                                raise ValueError

                            translateFromList = item[0][0] == pt.translateDatumfromList
                            if translateFromList:
                                idList_key = item[0][1]
                                labelList = self.appRegistry.idKeyedList.getEntry(idList_key)
                            else:
                                raise ValueError
                        else:
                            translateFromList = False

                            if item[0] in self.idListKeys:
                                idList_key = item[0]
                                labelList = self.appRegistry.idKeyedList.getEntry(idList_key)

                            else:
                                labelList = [item[0]]


                        for candidateLabel in labelList:
                            if candidateLabel == rawLabel:
                                # map ( destLabel, variant line filter, data pair index )
                                thisValueMap = self.valueMap(recordLabel, rawLabel,
                                                             variantFilter, datumSpecIndex,
                                                             translateFromList)

                                self.valueMapList.append(thisValueMap)
                                self.mappedValueCount += 1
                                break

                        datumSpecIndex += 1
                    pass
                pass

                if self.mappedValueCount > 0:
                    ## No further additions to vmap list
                    ## define the max index, and reset the index
                    self.vmapFetchIndex = 0
                    self.vmapMaxFetchIndex = self.mappedValueCount-1

            return

        pass

    # itemLabelList: list of labels each item has to identify
    #               the value within the aggregated record/database
    #
    # itemIDList:    list of labels used to identify parsed data
    #                to the aggregator, which then assigns 'labels'
    #                from corresponding label list when placing the
    #                value into the aggregating record
    #
    aggregationMapList = None
    recordLabelList = None
    recordSize = None
    sequenceNumber = None
    parsedLogLineList = None
    parsedLogLine_keyList = None
    sourceMapList = None
    validRecordItems = None
    sourceLabelCount = None
    database = None
    aggregateRecord = None
    aggregateRecordDirty = None
    aggregateRecordValidItems = None
    recordSequence = None
    aggregator_key = None
    startSyncLabel = None
    endSyncLabel = None

    def __init__(self, recordLabelList, aggStorageControl: AggregationStorageControl, aggregationMapList,
                        aggregator_key, appRegistry:mcutil.applicationRegistry):

        ## Debug settings
        self.showRecordStorage=False
        ## End Debug Settings

        self.aggregator_key = aggregator_key
        self.aggregationMapList = aggregationMapList
        self.recordLabelList = recordLabelList
        self.appRegistry = appRegistry
        self.startSyncLabel = aggStorageControl.FirstDatum
        self.endSyncLabel = aggStorageControl.LastDatum
        self.storeBeforeStartLabel = aggStorageControl.FirstDatum in recordLabelList
        self.storeAfterLastLabel = aggStorageControl.LastDatum in recordLabelList
        self.storeBeforeCollision = aggStorageControl.StoreOnCollision
        self.storeWhenFull = aggStorageControl.StoreOnFull
        self.storeIfEmpty = aggStorageControl.StoreIfEmpty
        self.recordSize = len(recordLabelList)
        self.aggregateRecord = []
        self.aggregateRecordDirty = False
        self.aggregateRecordValidItems = 0
        self.sequenceNumber = 0
        self.parsedLogLineList = []
        self.parsedLogLine_keyList = []
        self.sourceMapList = []
        self.validRecordItems = 0
        self.countUniqueSourceLabels()
        self.configureAggregation()
        self.database = ds.sequencedData(ds.compareNumber)
        self.aggregateRecordSequenceNumber = 0
        self.newAggregateRecord()
        return

    def configurationValid(self):
        if self.sourceLabelCount == None:
            self.countSourceLabels()


        result = self.recordSize > 0 and self.recordSize == len(self.recordLabelList) and \
                self.recordSize == self.sourceLabelCount

        return result

    def configureAggregation(self):
        self.sourceMapList = []

        for aggregationMap in self.aggregationMapList:
            ## Generate and store Source Maps for each Parsed Log Line Type
            ## Verify that values are mapped to the aggregate record
            ## BEFORE appending the source map

            thisSourceMap = self.sourceMap(self.recordLabelList, aggregationMap, self.appRegistry)


            if thisSourceMap.getMappedValueCount() > 0:
                self.sourceMapList.append(thisSourceMap)

                # accumulate list of PROVEN relevant parsedLogLines
                if thisSourceMap.parsedLogLineSpec not in self.parsedLogLineList:
                    self.parsedLogLineList.append(thisSourceMap.parsedLogLineSpec)
                    self.parsedLogLine_keyList.append(thisSourceMap.parsedLogLineSpec[0][1])
            pass

        return

    def getKey(self):
        return self.aggregator_key

    def getDatabase(self):
        if self.database != None:
            return self.database
        else:
            raise ValueError

    def getRecordLabelList(self) -> list:
        if len(self.recordLabelList) == self.recordSize \
                and self.recordSize > 0:
            return self.recordLabelList
        else:
            return None
        pass

    def countUniqueSourceLabels(self):

        self.sourceLabelCount = 0
        labelList = []
        
        for logMap in self.aggregationMapList:
            for logVariant in logMap[1]:
                for label in logVariant[2]:
                    if label not in labelList:
                        labelList.append(label)
                        self.sourceLabelCount+=1
                    pass
                pass
            pass

        return self.sourceLabelCount


    def nextAggregateRecordSequenceNumber(self):
        self.aggregateRecordSequenceNumber += 1
        return self.aggregateRecordSequenceNumber

    def aggregateRecordFull(self):
        if self.aggregateRecord.count(pt.NULL_ITEM) == 0:
            ## NULL_ITEM formatted fields have all been overwritten
            ## The Record is full
            return True
        return False

    def aggregateRecordEmpty(self):
        if self.aggregateRecord.count(pt.NULL_ITEM) == self.recordSize:
            ## all the NULL_ITEM formatted fields remain
            ## NO UPDATES have occurred
            return True
        return False


    def newAggregateRecord(self):
        # define list as full of NULL_ITEM
        self.aggregateRecord = self.recordSize * [pt.NULL_ITEM]
        self.aggregateRecordValidItems = 0
        self.aggregateRecordDirty = False
        return

    def storeAggregateRecord(self):
        if not self.storeIfEmpty:
            if self.aggregateRecordEmpty():
                return

        self.database.appendSequencedDatum(self.aggregateRecordSequenceNumber, self.aggregateRecord)
        self.nextAggregateRecordSequenceNumber()
        self.newAggregateRecord()
        return

    def emitaggregateRecord(self):
        # send a temp record to the temp data sequencer
        self.database.appendSequencedDatum(self.sequenceNumber,
                                           self.aggregateRecord)
        return

    def getListedSourceMap(self) -> sourceMap:
        if self.sourceMapIndex < len(self.sourceMapList):
            return self.sourceMapList[self.sourceMapIndex]
        raise ValueError

    def getNextListedSourceMap(self) -> sourceMap:
        self.sourceMapIndex += 1
        return self.getListedSourceMap()

    def getFirstListedSourceMap(self) -> sourceMap:
        self.sourceMapIndex = 0
        return self.getListedSourceMap()

    def processParsedLogLine(self, thisRecord):
        # filter parsed logs presented
        # process those relevant to aggregated record
        # identify this (presented) Record, a Parsed Line Log

        # self.thisRecord = thisRecord
        try:
            lineID = thisRecord[0][1]
            if lineID not in self.parsedLogLine_keyList:
                # this log line is not relevant to this Aggregated Record
                return
        except Exception as es:
            print("Exception: " + es)
            exit(-1)

        ## There is one SourceMap for each Parsed Log Line
        ## type in the Aggregation Map. Source Maps have
        ## lookup (valueMap) information for each of the
        ## variant forms of the Parsed Log Line matching
        ## the Log Line ID.

        srcMap = self.getFirstListedSourceMap()


        while srcMap != None:
            # Select the map that matches the lineID/logLine-Data
            # to be processed

            if srcMap.parsedLogLineSpec[0][1] != lineID:
                srcMap = self.getNextListedSourceMap()
            else:
                break

        ## since the parsed log line type *IS* listed
        ## execution *WILL* arrive here

        ## add values to the Aggregated Record
        valMap = srcMap.getFirstValueMap()



        while True:

            if valMap.variantFilter == ['*'] or valMap.variantFilter in thisRecord:
                ## This map **can** fit this record -BUT- WildCard filters mean
                ## they might not. We have to confirm the raw-label matches
                ## if it is a WildCard, or a label that appears more than once
                ## in the ValueMap set.

                ## Compare the value raw label to the raw label in the presented record


                #if valMap.logLabel == thisRecord[valMap.valueIndex][0]:
                ## sometimes the logLabel is the DatumName, sometimes DatumValue
                ## testing for 'in' is more liberal than testing an exact
                ## list element...
                if valMap.logLabel in thisRecord[valMap.valueIndex]:

                    ## confirm the logLabel matches the presented record
                    ## before confirming we have a match

                    ## process record publishing trigger
                    if self.storeBeforeStartLabel and valMap.recordLabel == self.startSyncLabel:
                        if self.showRecordStorage:
                            print("pre-FirstLabel Storage @:"+valMap.recordLabel)
                        self.storeAggregateRecord()

                    ## FILTER MATCH: add value to Aggregation Record
                    targetIndex = self.recordLabelList.index(valMap.recordLabel)

                    if self.storeBeforeCollision:
                        # emit record to prevent overwriting a valid value

                        collision = self.aggregateRecord[targetIndex] != pt.NULL_ITEM
                        if collision:
                            if self.showRecordStorage:
                                print("pre-Collision Storage @:"+valMap.recordLabel)
                            self.storeAggregateRecord()



                    if valMap.translateFromList:
                        #thisValue = valMap.recordLabel
                        self.aggregateRecord[targetIndex] = valMap.recordLabel
                    else:
                        self.aggregateRecord[targetIndex] = thisRecord[valMap.valueIndex][1]

                    if self.storeAfterLastLabel and valMap.recordLabel == self.endSyncLabel:
                        if self.showRecordStorage:
                            print("post-LastLabel Storage @:"+valMap.recordLabel)
                        self.storeAggregateRecord()

            if not srcMap.getNextValueMapOK():
                break

            valMap = srcMap.getNextValueMap()
            continue


        return
