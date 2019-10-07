import collections as coll
#import mculog_utility
import time
#import calendar
import pytz
import datetime as dtime

## Provide UTC and Local TimeZone dates on demand
## Initialize based on User Provided "Initial" Time/TimeDate
## ..based on User Provided Time/TimeDate String Format
##
## timestamp is the time management class for the mculog parser
## it converts timestamps of various types to UTC Epoch Time
## the UTC Epoch occurred at the GPSWeek Rollover event on
## April 6 2019, Midnight.
##
## GPS Week timestamps (easily obtained from PUTTY) will be
## measured as if the week began at the GPSWeek Rollover Epoch
## If the User uses MDYHMS or similar variants for TIMEDATE
## detect and parse those formats into GPSWeek Rollover Epoch Time
##
##

class timeutil(object):
    ## configuration for timestamp types
    ## classifying timestamps by the number of variables in each
    ## ONLY ONE timestamp per class can be the DEFAULT
    ## the default is reckoned to be the timestamp type when
    ## the format is guessed heuristically
    ## if a non-default format is to be used, it must be configured
    ## by the class initializer

    EPOCHTYPE_UNIX = 1
    EPOCHTYPE_GPSWEEK = 2

    TIMEID_DISCOVER = -1

    ## todo: IMPLEMENT USERDEFINED TIMESTAMP FORMATS
    ## todo: CAN BE DEFINED FROM A CONFIG FILE
    TIMEID_USERDEFINED = -2
    FMT_USERDEFINED = None

    TimeSpec = coll.namedtuple('TimeSpec', 'id, format, itemCount, isdefault ')

    # 12 hour, month/day cycles
    TIMEID_MDY12HMS = 0
    # 24 hour, month/day cycles
    TIMEID_MDY24HMS = 1
    # 24 hour, 366 day, cycle
    TIMEID_YD24HMS = 2
    # 12 hr HMS only
    TIMEID_12HMS = 3
    # 24 hr HMS only
    TIMEID_24HMS = 4
    # GPS WEEK-SECONDS w/ MILLISECONDS
    TIMEID_GPSWSMS = 5
    # GPS WEEK_SECONDS
    TIMEID_GPSWS = 6
    # 12 HR MDYHMSZ
    TIMEID_MDY12HMSZ = 7
    # 24 hr MDYHMSZ
    TIMEID_MDY24HMSZ = 8
    # 12 HR MDYHMSz
    TIMEID_MDY12HMSz = 9
    # 24 hr MDYHMSz
    TIMEID_MDY24HMSz = 10

    parsedTimeElements = ['%H', '%I', '%p', '%M', '%S', '%m', '%d', '%y', '%Y', '%z', '%Z', '%G', '_MIL']

    timeSpecList = [
        TimeSpec(id=TIMEID_MDY12HMS, format='%m %d %y %I %M %S %p', itemCount=7, isdefault=True),
        TimeSpec(id=TIMEID_MDY24HMS, format='%m %d %y %H %M %S', itemCount=6, isdefault=True),
        TimeSpec(id=TIMEID_YD24HMS, format='%Y %D %H %M %S', itemCount=5, isdefault=True),
        TimeSpec(id=TIMEID_12HMS, format='%I %M %S %p', itemCount=4, isdefault=True),
        TimeSpec(id=TIMEID_24HMS, format='%H %M %S', itemCount=3, isdefault=True),
        TimeSpec(id=TIMEID_GPSWSMS, format='%G _MIL', itemCount=2, isdefault=True),
        TimeSpec(id=TIMEID_GPSWS, format='%G', itemCount=1, isdefault=True),
        TimeSpec(id=TIMEID_MDY12HMSZ, format = "%d.%m.%Y %H:%M:%S %p %Z", itemCount=7, isdefault=True),
        TimeSpec(id=TIMEID_MDY24HMSZ, format = "%d.%m.%Y %H:%M:%S %Z", itemCount=8, isdefault=False),
        TimeSpec(id=TIMEID_MDY12HMSz, format = "%d.%m.%Y %H:%M:%S %p %z", itemCount=7, isdefault=True),
        TimeSpec(id=TIMEID_MDY24HMSz, format = "%d.%m.%Y %H:%M:%S %z", itemCount=8, isdefault=False)
        ]

    timeSpecIDsWithHMS = [TIMEID_MDY12HMS, TIMEID_MDY24HMS, TIMEID_YD24HMS,
                          TIMEID_24HMS, TIMEID_12HMS, TIMEID_MDY12HMSZ,
                          TIMEID_MDY24HMSZ]

    timeSpecIDsWithGPSWS = [TIMEID_GPSWS,
                            TIMEID_GPSWSMS]

    timeSpecIDs = timeSpecIDsWithHMS + timeSpecIDsWithGPSWS

    timeFormat = None
    timeFormatElements = None
    timeFormatID = None
    userDefinedFormat = None
    userDefinedElements = None
    epochType = None

    lastTime = None
    initialTime = None

    epochTimeStruct = None
    defaultDateTime_naive = None
    defaultDateTime_aware = None
    gpsWeekSeconds = None
    epochSeconds = None
    tzoneType = None

    TZONETYPE_SPECIFIC = 1
    TZONETYPE_UTCOFFSET = 2
    TZONETYPE_NAIVE = 3
    TZONETYPE_UNDEFINED = 0

    ## TODO: insure that changes in daylight savings time and
    ## TODO: leap years, and sidereal adjustments, etc do not
    ## TODO: lead to inaccuracies in time measurement.

    EPOCH_TIMEDATE_FORMAT = "%m.%d.%Y %H:%M:%S %Z"

    ## Setting GPS WEEK ROLLOVER Date as the default date
    ## On April 6 2019, the GPS WEEK rolls over from 1023 to 0
    GPSWEEK_ROLLOVER_042019 = "04.06.2019 00:00:00 UTC"


    ## Unix Epoch Declaration
    UNIX_EPOCH_012019 = "1.1.1970 00:00:00 UTC"


    def __init__(self,
                 time_format_id=TIMEID_DISCOVER,
                 initial_datetime_string=GPSWEEK_ROLLOVER_042019,
                 userdef_format=EPOCH_TIMEDATE_FORMAT,
                 timezone_string='UTC', is_dst=0, epoch_type=EPOCHTYPE_GPSWEEK):

        # initialize time parameters
        # default timedate to last GPS Week Rollover second in UTC timezone
        # on that base, intialize the user's time / timedate settings.

        if timezone_string in pytz.all_timezones:
            self.userTimezone = pytz.timezone(timezone_string)
        else:
            print("user timezone = ["+timezone_string+"]  is unknown; not a pytz timezone")
            raise ValueError

        if epoch_type == self.EPOCHTYPE_GPSWEEK:
            self.epochType = self.EPOCHTYPE_GPSWEEK
        else:
            self.epochType = self.EPOCHTYPE_UNIX

        ## TODO: does is_dst require value checking ?

        self.initial_isdst = is_dst
        self.lastTime = None
        self.initialTime = None
        self.userDefinedFormat = None
        self.userDefinedElements = None
        ## Init TimeDate Base with a Default Date in UTC
        self.initEpochTimeStruct()
        ## Init TimeDate per User Specification
        self.set_timeFormatInfo(time_format_id,
                                userdef_format,
                                initial_datetime_string)
        return


    def initEpochTimeStruct(self):
        ## Default DateTime begins on GPSWEEK Rollover in UTC TZONE
        ##

        if (self.epochType == self.EPOCHTYPE_GPSWEEK):
            epoch_timedate_string = self.GPSWEEK_ROLLOVER_042019
        else:
            epoch_timedate_string = self.UNIX_EPOCH_012019

        self.timeStructEpoch = time.strptime(epoch_timedate_string, self.EPOCH_TIMEDATE_FORMAT)


        self.utcTimeZone = pytz.timezone('UTC')
        self.initialDateTime = dtime.datetime(self.timeStructEpoch.tm_year,
                                              self.timeStructEpoch.tm_mon,
                                              self.timeStructEpoch.tm_mday,
                                              self.timeStructEpoch.tm_hour,
                                              self.timeStructEpoch.tm_min,
                                              tzinfo=self.utcTimeZone)
        return


    def getUserTimeID(self):
        if self.timeFormatID == None:
            print("ERROR: Time Format ID is UNDEFINED")
            raise ValueError

        return self.timeFormatID

    def getTimeFormatInfo(self, time_spec_id):
        this_timeSpec = self.getTimeSpec(time_spec_id)

        self.timeFormat = this_timeSpec.format
        self.timeFormatElements = this_timeSpec.itemCount
        self.timeFormatID = this_timeSpec.id
        return

    def set_timeFormatInfo(self,
                           time_format_id,
                           userdefined_format,
                           initial_datetime_string):

        if time_format_id in self.timeSpecIDs:
            self.getTimeFormatInfo(time_format_id)

        elif time_format_id == self.TIMEID_DISCOVER:
            # this format will be discovered when
            self.timeFormat = None
            self.timeFormatElements = None
            self.timeFormatID = self.TIMEID_DISCOVER


        elif time_format_id == self.TIMEID_USERDEFINED:
            if not self.discoverTimeFormat(userdefined_format):
                # not a match for existing parseSpecs, going rogue
                # verify elements of format are recognized by timedate parser
                userdefined_elements = self.listFormatElements(userdefined_format)
                for ordinal, element in enumerate(userdefined_elements, 0):
                    if element not in self.parsedTimeElements:
                        raise ValueError

            # userdef format matches existing timedate attribute ensemble
            # or has an ensemble that is supported by parser capabilities
            self.timeFormat = self.userDefinedFormat = userdefined_format
            userdefined_elements = self.listFormatElements(userdefined_format)
            self.timeFormatElements = self.userDefinedElements = userdefined_elements
            self.timeFormatID = self.TIMEID_USERDEFINED

        else:
            raise ValueError

        ## set initial datetime
        ## set a utc time, or a specific localized time
        ## no naive time



        if '%z' in self.timeFormatElements:
            self.tzoneType = self.TZONETYPE_SPECIFIC
            if '%Z' in self.timeFormatElements:
                raise ValueError
        elif '%Z' in self.timeFormatElements:
            self.tzoneType = self.TZONETYPE_UTCOFFSET
        else:
            self.tzoneType = self.TZONETYPE_NAIVE


            ## localization has been defined for a pytz timezone or UTC+/-NN:NN
            localized = self.tzoneType != self.TZONETYPE_NAIVE
            pass

        self.initialDateTime = time.strptime(self.timeFormat, initial_datetime_string)
        self.lastTime = None
        self.initialTime = None
        return

    def listFormatElements(self, format_string):
        # return the list of format specifications without
        # intermediate punctuation, and whitespace
        formatList = []
        formatDetected = False

        for character in format_string:
            if character.isalpha():
                if formatDetected == True:
                    formatList.append('%' + character)
                    formatDetected = False
            elif character == '%':
                if formatDetected:
                    # '%%' detected, just an escaped '%'
                    formatDetected = False
                else:
                    formatDetected = True
            continue

        return formatList

    # '.' is parsed from format string
    # a '.' may be part of a formatted value that is fixed/floating point
    # parsing the '.' from format is harmless
    # parsing the '.' from the expression is unsafe
    # ----------------------------------------------
    # '+' and '-' are not in the seperator list
    # they can be a part of number values
    # stripping them destroys information

    seperator_list = [':',  "\\", ' ', '.']

    def multisepSplit(self, time_string: str, seperator_list: list = None):
        reformat_string = time_string
        if seperator_list == None:
            seperator_list = self.seperator_list

        default_seperator = seperator_list[0]
        for ordinal, seperator in enumerate(seperator_list, 1):
            if ordinal == 0:
                default_seperator = seperator
                continue

            reformat_string = reformat_string.replace(seperator, default_seperator)

        return reformat_string.split(default_seperator)

    def getTimeSpec(self, spec_id) -> TimeSpec:

        for specOrdinal, timeSpec in enumerate(self.timeSpecList):
            if timeSpec.id == spec_id:
                return timeSpec
            continue

        raise ValueError

    def discoverTimeFormat(self, tstamp_string):

        tstamp_elements = self.listFormatElements(tstamp_string)
        #        tstamp_elements = self.multisepSplit(tstamp_string, self.seperator_list)
        tstamp_element_count = len(tstamp_elements)

        for specOrdinal, timeSpecID in enumerate(self.timeSpecIDs, 0):
            this_timeSpec = self.getTimeSpec(timeSpecID)

            if tstamp_element_count == this_timeSpec.itemCount:
                if this_timeSpec.isdefault == True:
                    default_format = this_timeSpec.format

                    ## TODO: find out why cmp() didn't work
                    ## TODO: don't need it anymore - algo change

                    ## OK when presented format's elements are 1 to 1
                    ## match with a pre-defined default format.
                    ##    ***INDEPENDENT OF ELEMENT ORDER***

                    for elementOrdinal, element in enumerate(tstamp_elements, 0):
                        if element not in default_format:
                            # not a predefined format
                            return False

                    # matches a predefined format
                    self.timeFormatID = timeSpecID
                    self.timeFormat = this_timeSpec.format
                    self.timeFormatElements = self.listFormatElements(self.timeFormat)
                    return True
            # not yet a match
            continue

        return False


    def computeEpochTime(self, time_string):


        this_structime = time.strptime(time_string, self.timeFormat)

        # get epoch seconds from timestruct
        epochSeconds = self.currentTime = time.mktime(this_structime)
        tstring=time.strftime(self.timeFormat, this_structime)
        return epochSeconds

    def computeEpochTime1(self, time_string):
        tm__hour = tm__min = tm__sec = tm__year = tm__mday = None
        tm__yday = tm__mon = tm__isdst = tm__wday = tm__gmtoff = None
        tm__zone = None

        time_attributes = self.multisepSplit(time_string, self.seperator_list)
        erase_tm_yday = False
        erase_tm_wday = False

        date_changed = '%y' in self.timeFormatElements or \
                        '%m' in self.timeFormatElements or \
                        '%d' in self.timeFormatElements or \
                        '%Y' in self.timeFormatElements or \
                        '%j' in self.timeFormatElements


        for index, attribute in enumerate(time_attributes, 0):
            format_code = self.timeFormatElements[index]
            if format_code == '%H' or format_code == '%I':
                tm__hour = int(attribute)
            elif format_code == '%p':
                # important that this is processed AFTER '%I'
                if str(attribute).lower in ['p', 'pm']:
                    tm__hour = int(tm__hour) + 12
            elif format_code == '%M':
                tm__min = int(attribute)
            elif format_code == '%S':
                tm__sec = int(attribute)
            elif format_code == '%m':
                tm__mon = int(attribute)
            elif format_code == '%d':
                tm__mday = int(attribute)
            elif format_code == '%j':
                tm__yday = int(attribute)
            elif format_code == '%y':
                ## force full year precision
                tm__year = int(attribute) + 2000
            elif format_code == '%Y':
                tm__year = int(attribute)
            elif format_code == '%z':
                tm__zone = attribute
            elif format_code == '%Z':
                tm__zone = attribute
            else:
                raise ValueError

        if not date_changed:
            if tm__mon == None:
                tm__mon = self.timeStruct_RO2019.tm_mon
            if tm__mday == None:
                tm__mday = self.timeStruct_RO2019.tm_mday
            if tm__wday == None:
                tm__wday = self.timeStruct_RO2019.tm_wday
            if tm__yday == None:
                tm__yday = self.timeStruct_RO2019.tm_yday
            if tm__year == None:
                tm__year = self.timeStruct_RO2019.tm_year
            if tm__isdst == None:
                tm__isdst = self.timeStruct_RO2019.tm_isdst
#            if tm__zone == None:
#                tm__zone = self.timeStruct_RO2019.tm_zone

        #if tm__gmtoff == None:
        #    tm__gmtoff = self.timeStruct_RO2019.tm_gmtoff


        current_structime = time.struct_time([tm__year, tm__mon,
                                              tm__mday, tm__hour,
                                              tm__min, tm__sec,
                                              tm__wday, tm__yday,
                                              tm__isdst, tm__zone,
                                              tm__gmtoff])

        # get epoch seconds from timestruct
        epochSeconds = self.currentTime = time.mktime(current_structime)

        return epochSeconds

    def setSessionTime(self, time_string):
        if self.timeFormatID not in self.timeSpecIDs:
            # timestamp format uninitialized means it is
            # time to finish initializing necessary attributes

            if self.timeFormatID == self.TIMEID_DISCOVER:
                if not self.discoverTimeFormat(time_string):
                    raise ValueError

            # At this point the timestamp format is established
            # timeStruct template has default date information
        if self.timeFormatID == self.TIMEID_USERDEFINED or \
                self.timeFormatID in self.timeSpecIDsWithHMS:

            self.epochTime = self.computeEpochTime(time_string)
            self.lastTime = self.currentTime
            self.currentTime = self.epochTime
            return self.currentTime

        elif self.timeFormatID in self.timeSpecIDsWithGPSWS:
            raise NotImplemented

        else:
            raise ValueError

    def getSessionSeconds(self, time_string):
        if self.epochSeconds != None:
            return self.epochSeconds

        raise ValueError

    def getDifferenceInSeconds(self, time_string_1, time_string_2):
        time1 = self.computeEpochTime(time_string_1)
        time2 = self.computeEpochTime(time_string_2)
        return time2 - time1

    pass