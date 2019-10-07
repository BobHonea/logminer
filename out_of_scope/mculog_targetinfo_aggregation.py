
## ********************
#   TARGET INFORMATION
## ********************
#
# the epmTempSensor
#

from out_of_scope import thermreg_targetinfo as ti

tempAggregator_key = "targetInfoAgg_key"

## "a2l" is the first label in the publishing cycle of the temperatures
## "epm2max" is the last HOWEVER: there may be an fpga only, or fpga+epm1 only
## system. In that case "a0r" or "epm1Max" would be the last labels
## TODO: deal with variant sync labels
aggregateSysInfo = \
[ "platform", "fwversion", "revbranch", "buildtimedate", "git-sha",
  "buildid", "buildtype", "compiler", "bootreason", "boardversion",
  "runningimage", "bootldrbuildid", "uid1", "uid2", "netip","netmask", "netgateway"]


mapped_epmBoardInfo = [ ti.firmwareDeclLogSpec,
                        [[pt.parseLineID, ti.firmwareDeclLogSpec_key],]]
tempSyncLabels = ["a2l", "epm2Max"]

mapped_epmTempSensorValues = \
    [tlspec.epmTempSensorParseSpec, [
        [["*"], ["device 0x90 via bus 0"], ["epmx90b0"]],
        [["*"], ["device 0x90 via bus 1"], ["epmx90b1"]],
        [["*"], ["device 0x94 via bus 1"], ["epmx94b1"]],
        [["*"], ["device 0x94 via bus 1"], ["epmx94b1"]]
    ]]

fpgaTempAggregateRecordMap = \
    ["a0l", "a0r", "a2l", "a2r", "a4l", "a4r",
     "a6l", "a6r", "a8l", "a8r", "epm1Max", "epm2Max"]

## mapped value(s)
## [[log line filter], [log line value label list],
mappedFpgaTempValues = [tlspec.fpgaTempSensorParseSpec, [
    [["fansocket", "a0"], ["local temperature", "remote temperature"], ["a0l", "a0r"]],
    [["fansocket", "a2"], ["local temperature", "remote temperature"], ["a2l", "a2r"]],
    [["fansocket", "a4"], ["local temperature", "remote temperature"], ["a4l", "a4r"]],
    [["fansocket", "a6"], ["local temperature", "remote temperature"], ["a6l", "a6r"]],
    [["fansocket", "a8"], ["local temperature", "remote temperature"], ["a8l", "a8r"]]
]]
mappedEpm1MaxTempValues = [tlspec.maxEPM1TempParseSpec, [
    [["*"], ["epm1MaxTemp"], ["epm1Max"]]
]]

mappedEpm2MaxTempValues = [tlspec.maxEPM2TempParseSpec, [
    [["*"], ["epm2MaxTemp"], ["epm2Max"]]
]]

targetInfoAggregationList = [ mapped_firmwareDeclSpec, mapped_imageTarget]

