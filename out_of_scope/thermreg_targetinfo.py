import mculog_parsetypes as pt




include mculog_parsetypes as pt

#Aurix Tricore TC297 Bare metal OS
# Compiled for platform AVFPGA
# Firmware Version Number :01.11.00
# Revision Branch : master
# Build date and time:  Mar  1 2019 00:18:11
# GIT-SHA : b06122e17f349e743a4746e100fbb690e041df2b
# BUILD-ID : 91
# BUILD-TYPE : Release
# COMPILER : tasking
# Boot Reason: 0x0000
# Board Version: 00
# Running Image: avfpga_tasking_rel_91_second_stage
# Bootloader build-id: 91
# UID: 000000002114f406 8471ffd805840040
# Flash FPGA_FLASH, ID: 0x20BB21
# Flash MCU_FLASH, ID: 0x20BB21
# Network Info:
# Netmask:     255.255.255.0
# Gateway:     192.168.19.1
# MAC address: 00-14-22-01-24-08
# IP Address:  192.168.19.200





platforms = ["avfpga", "avepm", "devkit"]
buildtype = ["Release", "Engineering"]
compiler = ["tasking", "tricore"]
bootreason = ["0x0000", "0x0001", "0x0002", "0x0003"]
boardversion = ["00", "01"]
imagetype = ["bootloader", "standalone", "second_stage"]


firmwareDeclLogSpec_key = "Aurix Tricore"
cpuTypeTag = "CPU Type"
appNameTag = "AppName"

firmwareDeclSpec = [[pt.parseLineID,firmwareDeclLogSpec_key],
                      [[pt.setDatumName,cpuTypeTag],[pt.parseDatum,pt.parseDatum]],
                      [[pt.setDatumName],appNameTag],[pt.parseDatum]]

firmwareDeclParseSpec = [[pt.parseLineID, firmwareDeclLogSpec_key],
                         [cpuTypeTag, pt.var_STRING], [appNameTag, pt.var_STRING]]


targetingTag = "Compiled for"
platformTag = "platform"
boardTypes = ["AVFPGA","AVEPM","DEVKIT"]

imageTargetLogSpec = [[pt.parseLineID, targetingTag],
                     [[pt.parseDatumName, platformTag],[pt.parseDatumfromList, boardTypes]]]

imageTargetParseSpec = [[pt.parseLineID, targetingTag],
                        [platformTag, pt.var_STRING]]

revBranchTag = "Revision Branch"
branchNameTag = "Branch"
revisionBranchLogSpec = [[pt.parseLineID, revBranchTag],
                         [[pt.setDatumName,"Branch"],[pt.parseDatum,pt.parseTextWord]]]

revisionBranchParseSpec = [[pt.parseLineID, revBranchTag],
                           [branchNameTag, pt.var_STRING]]


buildIDTag = "BUILD-ID"
buildTypeTag = "BUILD-TYPE"

buildIDLogSpec = [[pt.parseLineID, buildIDTag],
                  [[pt.setDatumName, "buildID"],[pt.parseDatum, pt.parseTextWord]]]

buildIDParseSpec = [[pt.parseLineID, buildIDTag],
                    ["buildID", pt.var_STRING]]

buildTypeLogSpec = [[pt.parseLineID, buildTypeTag],
                    [[pt.setDatumName, "buildType"],[pt.parseDatum, pt.parseTextWord]]]

buildTypeParseSpec = [[pt.parseLineID, buildTypeTag],
                      [["buildType", pt.var_STRING]]]

compilerTypeTag = "COMPILER"
compilerTypeLogSpec = [[pt.parseLineID, compilerTypeTag],
                       [[pt.setDatumName,"compiler"],[pt.parseDatum, pt.parseTextWord]]]

compilerTypeParseSpec = [[pt.parseLineID, compilerTypeTag],
                         ["compiler", pt.var_STRING]]

boardVersionTag = "Board Version"
boardVersionLogSpec = [[pt.parseLineID, boardVersionTag],
                       [[pt.setDatumName, "boardVersion"], [pt.parseDatum, pt.parseTextWord]]]

boardVersionParseSpec = [[pt.parseLineID, boardVersionTag],
                         ["boardVersion", pt.var_STRING]]

runningImageTag = "Running Image"
runningImageLogSpec = [[pt.parseLineID, runningImageTag],
                       [[pt.setDatumName, "runningImage"],[pt.parseDatum, pt.parseTextWord]]]

bootloaderBuildIDTag = "Bootloader build-id"
bootloaderBuildLogSpec = [[pt.parseLineID, bootloaderBuildIDTag],
                      [[pt.setDatumName,"bootloaderBuild"],[pt.parseDatum, pt.parseTextWord]]]

bootloaderBuildParseSpec = [[pt.parseLineID, bootloaderBuildIDTag],
                            ["bootloaderBuild", pt.var_STRING]]
networkIPTag = "IP Address"
macAddressTag = "MAC address"

networkIPLogSpec = [[pt.parseLineID, networkIPTag],
                    [[pt.setDatumName, "ipAddress"],[pt.parseDatum, pt.parseTextWord]]]

networkIPParseSpec = [[pt.parseLineID, networkIPTag], ["ipAddress", pt.var_STRING]]

macAddressLogSPec = [[pt.parseLineID, macAddressTag],
                     [[pt.setDatumName, "macAddress"], [pt.parseDatum, pt.parseTextWord]]]

macAddressParseSpec = [[pt.parseLineID, macAddressTag],
                       ["macAddress", pt.var_STRING]]

uidTag = "UID"

uidLogSpec = [[pt.parseLineID, uidTag], [[pt.setDatumName, "uid1"],[pt.parseDatum, pt.parseTextWord]],
              [[pt.setDatumName, "uid2"],[pt.parseTextWord]]]

uidParseSpec = [[pt.parseLineID, uidTag], ["uid1", pt.var_HEXINT], ["uid2", pt.var_HEXINT]]
