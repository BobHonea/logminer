import thermreg_log_specification as tlspec
import mculog_utility as mcutil


global thermregRegistryKeyedList

fpgaRegistry_key = "fpgaRegistry_key"
epmRegistry_key = "epmRegistry_key"

def buildAttributeKeys():
    # Build a database of data attributes identified by
    # the logLineSpec_key and position of their names and values
    # in the LoglineSpec, and the ParsedLineSpec
    # TODO: most definitely a TODO
    # TODO: getting by without this until a future refactor
    pass




def registerEpmLogLineSpecs(epmRegistry:mcutil.applicationRegistry):

    # Register keyword lists
    assert (epmRegistry.registerIdList(tlspec.epmLocalAlerts_key, tlspec.epmLocalAlerts))
    assert (epmRegistry.registerIdList(tlspec.epmSensorAddress_key, tlspec.epmSensorAddress))
    #assert (epmRegistry.registerIdList(tlspec.epmWarning_key, tlspec.epmWarning))
    assert (epmRegistry.registerIdList(tlspec.fanLogStatus_key, tlspec.fanLogStatus))

    # Register LogLine Specifications
    assert (epmRegistry.registerLogLineSpecification(tlspec.epmTempSensorLogSpec_key, tlspec.epmTempSensorLogSpec))
    assert (epmRegistry.registerLogLineSpecification(tlspec.localEpmAlertLogSpec_key, tlspec.localEpmAlertLogSpec))
    assert (epmRegistry.registerLogLineSpecification(tlspec.fanlogStatusLogSpec_key, tlspec.fanlogStatusLogSpec))
    assert (epmRegistry.registerLogLineSpecification(tlspec.fanCmdLogSpec_key, tlspec.fanCmdLogSpec))


    return True



def registerFpgaLogLineSpecs(fpgaRegistry:mcutil.applicationRegistry):
    # Register keyword lists
    assert (fpgaRegistry.registerIdList(tlspec.fpgaWarning_key, tlspec.fpgaWarning))
    assert (fpgaRegistry.registerIdList(tlspec.fpgaFanSocket_key, tlspec.fpgaFanSocket))
    assert (fpgaRegistry.registerIdList(tlspec.fanTachCountID_key, tlspec.fanTachCountID))
    assert (fpgaRegistry.registerIdList(tlspec.systemFanID_key, tlspec.systemFanID))
    assert (fpgaRegistry.registerIdList(tlspec.fanLogStatus_key, tlspec.fanLogStatus))
    assert (fpgaRegistry.registerIdList(tlspec.fpgaSensorLocation_key, tlspec.fpgaSensorLocation))

    # Register LogLine Specifications
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fanSpeedLogSpec_key, tlspec.fanSpeedLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fanSpeedLogSpec2_key, tlspec.fanSpeedLogSpec2))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fpgaTempSensorLogSpec_key, tlspec.fpgaTempSensorLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.epm1MaxTempLogSpec_key, tlspec.maxEPM1TempLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.epm2MaxTempLogSpec_key, tlspec.maxEPM2TempLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fanDutyCycleLogSpec_key, tlspec.fanDutyCycleLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fanCmdLogSpec_key, tlspec.fanCmdLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fanlogStatusLogSpec_key, tlspec.fanlogStatusLogSpec))
    assert (fpgaRegistry.registerLogLineSpecification(tlspec.fpgaWarningLogSpec_key, tlspec.fpgaWarningLogSpec))

    return True





def buildRegistries():
    global thermregRegistryKeyedList

    thermregRegistryKeyedList = mcutil.keyedList()
    fpgaRegistry = thermregRegistryKeyedList.getEntry(fpgaRegistry_key)

    if fpgaRegistry == None:
        fpgaRegistry = mcutil.applicationRegistry()
        registerFpgaLogLineSpecs(fpgaRegistry)
        thermregRegistryKeyedList.addEntry(fpgaRegistry_key, fpgaRegistry)


    epmRegistry = thermregRegistryKeyedList.getEntry(epmRegistry_key)

    if epmRegistry == None:
        epmRegistry = mcutil.applicationRegistry()
        registerEpmLogLineSpecs(epmRegistry)
        thermregRegistryKeyedList.addEntry(epmRegistry_key, epmRegistry)

    
    return True



