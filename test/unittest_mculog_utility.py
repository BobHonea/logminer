import mculog_utility as util
import mculog_time as mcutime



def test_timestamp_class():
    #define timestamp by user

    timestamp_format = "%d.%m.%Y %H:%M:%S"
    timestamp_example = "06.04.2019 00:00:01"

    userstamp = mcutime.timeutil(mcutime.timeutil.TIMEID_USERDEFINED,
                                 timestamp_example,
                                 timestamp_format)

    assert(userstamp.discoverTimeFormat(timestamp_example)==False)
    assert(userstamp.computeEpochTime(timestamp_example)==1554508801)
    assert(userstamp.computeEpochTime("01:00:01 12:00:00")==None)


    #define timestamp class with UNDISCOVERED type

    tstamp = mcutime.timeutil()


    assert (tstamp.discoverTimeFormat("00:00:00"))

    assert (tstamp.setSessionTime("00:00:01") == 1.0)
    assert (tstamp.setSessionTime("13:33:61") == 48841.0)
    assert (tstamp.setSessionTime("23:59:59") == 86399)

    tstamp.set_timeFormatInfo(tstamp.timeMDY24HMS)

    assert (tstamp.setSessionTime("04/31/2019 16:15:21")==0)


    return False






test_list = [ test_timestamp_class ]


def main():
    for test in test_list:
        assert(test())
    return


if __name__== "__main__":
  main()
