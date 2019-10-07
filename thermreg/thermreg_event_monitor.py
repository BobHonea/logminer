## specifications used in constraint testing
## mobileEye specified
import decimal as dec
import thermreg_aggregation as ta
import collections as coll



fanUpTransitionTemperatures = [40, 44.5, 49, 53.5, 58, 62.6, 67, 71.5, 76, 80.5, 120]
fanDownTransitionTemperatures = [ 35.5, 40, 44.5, 49, 53.5, 58, 62.6, 67, 71.5, 76, 80.5, 120]

tempSystemHistory = ["a0MaxTemp", "sysMaxTemp", "epm1MaxTemp", "epm2MaxTemp"]
fanControlHistoryLabels = ["a0TachVal", "a0Pwm", "systemTach", "systemPwm"]

RegIntervalSpec = \
    coll.namedtuple('RegIntervalSpec',
           'ordinal, lowTemp, hiTemp, pwmSetting, dutyCycle, checkTempAlerts')

FanIntervalSpec = coll.namedtuple('FanIntervalSpec',
                                  'pwmSetting, dutyCycle, tachCount, rpm')

## fan+temp control matrix from mobilEye Spec

regInterval0 = RegIntervalSpec(ordinal=0,lowTemp=-40,hiTemp=40,pwmSetting=25,dutyCycle=10,checkTempAlerts=False)
regInterval1 = RegIntervalSpec(ordinal=1,lowTemp=44.5,hiTemp=49,pwmSetting=50,dutyCycle=20,checkTempAlerts=False)
regInterval2 = RegIntervalSpec(ordinal=2,lowTemp=49,hiTemp=53.5,pwmSetting=77,dutyCycle=30,checkTempAlerts=False)
regInterval3 = RegIntervalSpec(ordinal=3,lowTemp=53.5,hiTemp=58,pwmSetting=102,dutyCycle=40,checkTempAlerts=False)
regInterval4 = RegIntervalSpec(ordinal=4,lowTemp=58,hiTemp=62.5,pwmSetting=128,dutyCycle=50,checkTempAlerts=False)
regInterval5 = RegIntervalSpec(ordinal=5,lowTemp=62.5,hiTemp=67,pwmSetting=154,dutyCycle=60,checkTempAlerts=False)
regInterval6 = RegIntervalSpec(ordinal=6,lowTemp=67, hiTemp=71.5,pwmSetting=180,dutyCycle=70,checkTempAlerts=False)
regInterval7 = RegIntervalSpec(ordinal=7,lowTemp=71.5,hiTemp=76,pwmSetting=205,dutyCycle=80,checkTempAlerts=False)
regInterval8 = RegIntervalSpec(ordinal=8,lowTemp=76,hiTemp=80.5,pwmSetting=230,dutyCycle=90,checkTempAlerts=False)
regInterval9 = RegIntervalSpec(ordinal=9,lowTemp=80.5,hiTemp=76,pwmSetting=255,dutyCycle=100,checkTempAlerts=True)

## fan control and sensor expectations

fanInterval0 = FanIntervalSpec(pwmSetting=25, dutyCycle=10, tachCount=1233, rpm=2433)
fanInterval1 = FanIntervalSpec(pwmSetting=51, dutyCycle=20, tachCount=605, rpm=4958)
fanInterval2 = FanIntervalSpec(pwmSetting=76, dutyCycle=30, tachCount=397, rpm=7556)
fanInterval3 = FanIntervalSpec(pwmSetting=152, dutyCycle=40, tachCount=None, rpm=None)
fanInterval4 = FanIntervalSpec(pwmSetting=None, dutyCycle=50, tachCount=None, rpm=None)
fanInterval5 = FanIntervalSpec(pwmSetting=None, dutyCycle=60, tachCount=None, rpm=None)
fanInterval6 = FanIntervalSpec(pwmSetting=None, dutyCycle=70, tachCount=None, rpm=None)
fanInterval7 = FanIntervalSpec(pwmSetting=None, dutyCycle=80, tachCount=None, rpm=None)
fanInterval8 = FanIntervalSpec(pwmSetting=None, dutyCycle=90, tachCount=None, rpm=None)
fanInterval9 = FanIntervalSpec(pwmSetting=None, dutyCycle=100, tachCount=None, rpm=None)

RegulationSpec = [regInterval0, regInterval1, regInterval2, regInterval3,
                  regInterval4, regInterval5, regInterval6, regInterval7,
                  regInterval8, regInterval9]

fanControlSpec = [fanInterval0, fanInterval1, fanInterval2, fanInterval3, fanInterval4,
                  fanInterval5, fanInterval6, fanInterval7, fanInterval8, fanInterval9]

ALERTVAR_NONE = 0
ALERTVAR_TEMPERATURE = 1
ALERTVAR_A0FAN_PWM_VS_RPM = 2
ALERTVAR_A2468FAN_PWM_VS_RPM = 3
ALERTVAR_RPM = 4

A0FAN_RPM_VS_PWM_0PCT = 1
A2468FAN_RPM_VS_PWM_0PCT = 2

MEASURE_NONE = 0
MEASURE_RANGE = 1
MEASURE_VALUE = 2
MEASURE_CONDITION = 3


# over 100C temperature alert
# over 85C Warning
# pwm != 0 and rpm < min_rpm
# min_rpm(a) > 0; min_rpm( a2 | a4 | a6 | a8 ) == 0


alertMatrixHeader = [ "Alert Number", "Alert Name", "Low Temp", "HighTemp"]
alertRange =    [[ 0, ALERTVAR_TEMPERATURE, [85,  120], "Temperature ALERT" ],
                 [ 1, ALERTVAR_TEMPERATURE, [100, 120], "Overtemperature ALERT"],
                 [ 2, ALERTVAR_A0FAN_PWM_VS_RPM, A0FAN_RPM_VS_PWM_0PCT, "A0 Fan Failure ALERT" ],
                 [ 3, ALERTVAR_A2468FAN_PWM_VS_RPM, A2468FAN_RPM_VS_PWM_0PCT, "System Fan Failure ALERT"]]




## Temp Events
## crossing "LowTemp" to lower temp (set pwm to lower temp range setting)
## crossing "HighTemp" to higher temp (set pwm to higher temp range setting)
## increasing to temperature >= 85 degree - enter Temp Alert
## increasing to temperature >= 100 degree - enter Overtemperature Alert
##
##
##
## Fan Events
## Fan not matching speed for Pwm Setting (need table fanSpeed vs PWM)
##   - Fan Alert for that fan (all fans' PWM set to Maximum / full speed)
##

class tempInterval(object):
    ordinal = None
    lowTemp = None
    hiTemp = None
    pwmSetting = None
    dutyCycle = None
    checkTempAlert = None

    def __init__(self, ordinal, lowTemp, hiTemp, pwmSetting, dutyCycle, checkTempAlert):
        self.ordinal = ordinal
        self.lowTemp = lowTemp
        self.hiTemp = hiTemp
        self.pwmSetting = pwmSetting
        self.dutyCycle = dutyCycle
        self.checkTempAlert = checkTempAlert
        return
    pass

class tempTransitionSpec(object):

    intervalList = None
    intervalCount = None
    intervalIndex = None

    def __init__(self, specificationMatrix):
        self.intervalList = []

        for item in specificationMatrix:
            self.intervalList.append(tempInterval(item[0], item[1], item[2], item[3], item[4], item[5]))
            self.intervalCount = len(self.intervalList)
            self.intervalIndex = 0
            continue

        return


    def getIntervalByTemp(self, temperature) -> tempInterval:
        foundInterval = None

        for tempInterval in self.intervalList:
            if temperature < tempInterval.lowTemp:
                break
            elif temperature == tempInterval.lowTemp:
                foundInterval = tempInterval
            elif temperature <= tempInterval.hiTemp:
                foundInterval = tempInterval
            else:
                continue

        if foundInterval == None:
            raise ValueError

        return foundInterval


    def getIntervalByOrdinal(self, ordinal):
        if ordinal >=0 and ordinal < self.intervalCount:
            return self.intervalList[ordinal]
        else:
            raise ValueError

    pass


VALUE_UNKNOWN = 0
VALUE_ABOVE_THRESHOLD = 1
VALUE_AT_THRESHOLD = 2
VALUE_BELOW_THRESHOLD = 3

tempList = ["a0MaxTemp", "sysMaxTemp", "epm1MaxTemp", "epm2MaxTemp"]


class tempTracker(object):


    A0_FAN_FAIL = None
    A2_FAN_FAIL = None
    A4_FAN_FAIL = None
    A6_FAN_FAIL = None
    A8_FAN_FAIL = None
    A0_85C_ALERT = None
    A0_100C_ALERT = None
    A2468_85C_ALERT = None


    previousTempList = None
    currentTempList = None
    previousInterval = None
    currentInterval = None

    tempLabels = None

    def __init__(self, tempLabelList):
        self.prevousInterval = None
        self.previousTempList = None
        self.currentInterval = None
        self.currentTempList = None
        self.tempLabels = tempLabelList
        self.transitionSpec = tempTransitionSpec()
        return


    def eventsDetected(self):
        eventString = ""
        return eventString

    def newTempWithinInterval(self,index):
        # check current temp against last temp interval
        if self.currentInterval == None:
            # there is no previous interval
            return False

        currentTemperature = self.currentTempList[index]
        return (self.currentInterval.lowTemp < currentTemperature or
                self.currentInterval.hiTemp > currentTemperature)


    def setCurrentInterval(self,index):
        # push current interval (at index) to previous interval set (at index)
        # define new current interval set member at index
        if self.previousInterval == None:
            return

        currentTemperature = self.currentTempList[index]
        prevInterval = self.previousInterval[index] = self.currentInterval[index]

        if prevInterval.lowTemp > currentTemperature or \
                prevInterval.hiTemp < currentTemperature:
            # temperature outside previous interval
            self.currentInterval[index] = currInterval = self.transitionSpec.getIntervalByTemp(currentTemperature)
        else:
            # remain within range
            self.currentInterval = prevInterval


        self.currentInterval[index] = thisInterval = self.transitionSpec.getIntervalByTemp(currentTemperature)
        if thisInterval.lowTemp > currentTemperature:
            pass



    def processIntervalTransition(self, index):
        # initiate any temp-interval transition-triggered actions
        #
        currInterval = self.currentInterval[index]

        if currInterval.checkTempAlert == True:
            lowTempIndex = alertMatrixHeader.index("Low Temp")
            highTempIndex = alertMatrixHeader.index("High Temp")

            for alert in alertRange:
                lowTemp = alert[lowTempIndex]
                highTemp = alert[highTempIndex]
                currentTemperature

                if currentTemperature >= lowTemp or currentTemperature <= highTemp:
                    # temp is within this Alert's range
                    print("ALERT DETECTION: @" + tempList[index] + " : " + alert[alertMatrixHeader.index("Alert Name")])

        else:
            prevInterval = self.previousInterval[index]


        return


    def iterate(self, tempList):
        ## take temperatures
        ## check to see if they are in last interval
        ## get new interval data
        ## note if there is a change or action
        ## store event, action set

        self.thisTempList = tempList
        for index,tempName in enumerate(self.tempLabels):
            if not self.newTempWithinInterval(index):
                self.updateInterval(index)
                self.processIntervalTransition(index)
                continue


        self.previousInterval = self.currentInterval
        return



class eventTracker(object):



    def __init__(self, eventTypeString, eventVariables, eventDetector):

        return

    pass


class thermRegulationMonitor(object):


    def __init__(self):
        pass
    def closeInterval(self, ordinal):
        pass
    def openInterval(self,ordinal):
        pass
    def reportTempInterval(self, maxTempData:list):
        pass
    def reportFanControlInterval(self, fanControlData:list):
        pass
    def reportSystemAlertInterval(self, systemAlertData:list):
        pass
    def getExpectedEvents(self):
        pass
    def getUnexpectedEvents(self):
        pass
    def getIntervalComplianceStatus(self):
        pass
    def getIntervalComplianceMessages(self):
        pass
    def getIntervalNonComplianceMessages(self):
        pass



def unittest_event_monitor():
    ## feed data series to the event monitor
    ## verify the events in the data occur as they should
    return