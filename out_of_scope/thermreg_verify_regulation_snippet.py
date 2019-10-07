## developing class definitions for data structures
## which can provide methods to help clarify/cleanup code

class aggregationSpecification(object):
    class logLineVariantMap(object):

        class mappedLogLineVariants(object):
            variantFilter = []
            valueLabels = []
            aggregationLabels = []

            def __init__(self, aggregationMapList):
                if type(aggregationMapList) == list:
                    if len(aggregationMapList) == 2 \
                            and len(aggregationMapList[0]) == 1 \
                            and type(aggregationMapList[1]) == list \
                            and len(aggregationMapList[1][0]) == 3:
                        return
                raise ValueError

            pass

        class mappedLogValueSet(object):
            parsedLineLogSpec = None
            parsedLogLineVariants = []

            def __init__(self, parsedLogSpec, parsedLineVariants):
                self.parsedLineLogSpec = parsedLogSpec
                if type(parsedLineVariants) == list \
                        and len(parsedLineVariants) > 0:
                    for variant in parsedLineVariants:
                        if len(variant) == 3:
                            self.parsedLogLineVariants.append(variant)

                return

            pass

        aggregatedRecordMap = []
        variantValueSets = []

        def __init__(self, aggregatedRecordMap, variantValueSets):
            self.variantValueSets = []
            self.aggregatedRecordMap = aggregatedRecordMap

            for set in variantValueSets:
                thisMappedValueSet = self.mappedLogValueSet(variantValueSets[0],
                                                            variantValueSets[1])
                self.variantValueSets.append(thisMappedValueSet)
            return

    pass

fpgaTempAggregationSpec = aggregationSpecification














###############################

parsedLogFilename = "fpga_putty_log_20190228-182812.groomed.log_Mon_Mar_11_15.11.15_2019.parsed.log"

parsedLogFile = open(parsedLogFilename, "r")

for line in parsedLogFile:
    if line in ['\n', "None\n"]:
        continue
    astline = ast.literal_eval(line)
    string_astline = str("::").join(astline)
    print(string_astline)
    tempAggregator.processParsedLogLine(astline)

return True













