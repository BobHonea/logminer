# !/usr/bin/python
#
#  python class module
#  SequencedData hold a sequenced dataset
#
## Log Parser Variable Types



COMPARE_AB_EQUAL        = 1
COMPARE_A_LT_B          = 2
COMPARE_A_LT_EQUAL_B    = 3
COMPARE_A_GT_B          = 4
COMPARE_A_GT_EQUAL_B    = 5
COMPARE_AB_UNEQUAL      = 6



decimal_text = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



def compareNumber(comparison, arg_a, arg_b):
    if comparison == COMPARE_AB_EQUAL:
        return arg_a == arg_b
    elif comparison == COMPARE_AB_UNEQUAL:
        return arg_a != arg_b
    elif comparison == COMPARE_A_LT_B:
        return arg_a < arg_b
    elif comparison == COMPARE_A_GT_B:
        return arg_a > arg_b
    elif comparison == COMPARE_A_GT_EQUAL_B:
        return arg_a >= arg_b
    elif comparison == COMPARE_A_LT_EQUAL_B:
        return arg_a <= arg_b
    else:
        raise ValueError


# compare_hms()
# compare sequence in hours-minutes-seconds
# ':' is the acknowledged seperator
# h:m:s, m:s, s are all parsed formats
# i.e., hours or hours:minutes may be absent
#


def getHMSNumber( number_text, number_max ):
    if not type(number_text, float):

        number = int(number_text)
        if number <= number_max and number >= 0:
            return number

    else:
        floatnumber = float(number_text)
        if (floatnumber <= float(number_max)) and (floatnumber >= 0.0):
            return floatnumber

    raise ValueError


def convertHMStoFloatSeconds(hms_text):
    hms_parts = hms_text.split(':')
    if len(hms_parts) == 3:
        hours = getHMSNumber(hms_parts[0], 23)
    else:
        hours = 0

    if len(hms_parts) >= 2:
        minutes = getHMSNumber(hms_parts[1], 59)
    else:
        minutes = 0

    seconds_parts = hms_parts[2].split('.')
    if len(seconds_parts) == 2:
        # seconds is floating point
        seconds = float(hms_parts[2])
        return float(hours * 60 + minutes * 60) + seconds
    else:
        seconds = int(seconds_parts)
        return float(hours * 60 + minutes * 60 + seconds)



def compareHMS(comparison, arg_a, arg_b):
    float_a = convertHMStoFloatSeconds(arg_a)
    float_b = convertHMStoFloatSeconds(arg_b)

    return( compareNumber(comparison, float_a, float_b) )


class sequencedData(object):
    # create a data pair list with sequence value (time or ordinal), and datum
    # implement adding ordered pairs in sequence, earlier followed by next in time
    # the sequence may be a discontinuous number or timevalue
    #
    # the use cases are:
    # 1. 	sequentially build up the sequenced data
    # 2.	data sequenced by provided or self-generated monotonic ordinals
    # 3.	data sequenced by time (milliseconds)
    # 4.	data searchable by ordinal
    # 5.	data searchable by value
    # 6.	data max, min parameters maintained, obtainable
    # 7.	data sequentially readable
    # 8.

    DATUM_UNORDERED = 0
    DATUM_SEQUENCED_ORDINALLY = 1
    DATUM_NUMERICALLY_TIMESTAMPED = 2
    DATUM_HMS_TIMESTAMPED = 3


    # hard reset
    # re-initialize all data

    def hardReset(self):
        self.datum_count = 0
        self.datum_list = []
        self.datum_index = 0

        self.matched_index = None
        self.sequence_list = []
        self.datum_list = []


    # soft_reset()
    # does not delete data

    def softReset(self):
        self.datum_index = 0
        self.matched_sequence = None




    def __init__(self, compare_function):
        self.hardReset()
        self.compareFunction = compare_function
        return

    def appendSequencedDatum(self, sequence, datum):
        # receive a sequence-ordinal and a datum
        # the sequence value is expected to monotonic in a series of
        # invocations of this function.
        self.datum_list.append(datum)
        self.sequence_list.append(sequence)
        self.datum_count += 1
        return

    def appendDatum(self, datum):
        self.appendSequencedDatum(self.datum_index, datum)
        return

    def purgeData(self):
        self.hardReset()
        return

    def getDatumByOrdinal(self, sequence):
        if sequence < len(self.sequence_list):
            self.datum_index = self.sequence_list.index(sequence)
            return self.datum_list[self.datum_index]
        raise ValueError


    def getFirstSequence(self):
        return self.sequence_list[0]

    def getLastSequence(self):
        return self.sequence_list[-1]

    def get_matched_sequence(self):
        # return the sequence value of the last datum
        # that was matched in a requested search
        if self.matched_sequence != None:
            return self.sequence_list[self.matched_index]
        raise ValueError



    def getDatumIndex(self):
        return self.datum_index

    def setDatumIndex(self, datum_index):
        if datum_index >= self.datum_count:
            raise ValueError
        else:
            self.datum_index = datum_index
        return



    def getDatumCount(self):
        return self.datum_count

    def getFirstDatum(self) -> object:
        """

        :rtype:
        """
        if (self.datum_count > 0):
            return (self.datum_list[0])

        raise ValueError

    def getNextDatum(self):
        self.datum_index+=1
        if self.datum_index < self.datum_count:
            return (self.datum_list[self.datum_index])
        return None


    def getCurrentDatum(self):
        if self.datum_index < self.datum_count:
            return self.datum_list[self.datum_index]
        raise ValueError


    def getCurrentSequence(self):
        if self.datum_index < self.datum_count:
            return self.sequence_list[self.datum_index]
        raise ValueError

    def incrementDatumIndex(self):
        if (self.datum_index + 1) < self.datum_count:
            self.datum_index += 1
        return

    def getLastDatum(self):
        # return the final datum in the datum list
        if self.datum_count > 0:
            return self.datum_list[self.datum_count-1]
        raise ValueError


    # getMatchingDatumSequence()
    #
    # Search from current datum_index in data until data match
    # is found. Return sequence value for matched datum

    def getMatchingDatumSequence(self,datum):
        # search upward, sequentially in the datum list for a matching
        # datum. return the index of the match.
        #print("count:"+str(self.datum_count))

        while self.datum_index < self.datum_count:
            #print(str(self.sequence_list[self.datum_index])+':'+str(self.datum_list[self.datum_index]))
            if self.compareFunction(COMPARE_AB_EQUAL, self.datum_list[self.datum_index], datum):
                self.matched_index = self.datum_index
                return self.sequence_list[self.datum_index]

            self.datum_index+=1

        return None

    def getFirstMatchingDatumSequence(self, datum):
        # search for a matching datum from the beginning
        # of the datum list
        self.datum_index = 0
        return self.getMatchingDatumSequence(datum)


    def getNextMatchingDatumSequence(self, datum):
        # get the matching datum value's sequence for
        # a datum indexed higher than the present pointer
        self.datum_index+=1
        return self.getMatchingDatumSequence(datum)

    def getCompareTypePositiveDatum(self,comparetype,datum):
        # Get the next datum in the datum list (incrementing index) that
        # matches the supplied datum per the comparison specification
        # return the matching datum, or the None-value on match/no-match
        #print("count:"+str(self.datum_count))

        while self.datum_index < self.datum_count:
            #print(str(self.sequence_list[self.datum_index])+':'+str(self.datum_list[self.datum_index]))
            if self.compareFunction(comparetype, self.datum_list[self.datum_index], datum):
                self.matched_index = self.datum_index
                return datum

            self.datum_index+=1

        return None

    def getFirstCompareTypePositiveDatum(self, comparetype, datum):
        # find the next instance of matching datum
        # return the matching datum value
        self.datum_index = 0
        return self.getCompareTypePositiveDatum(comparetype, datum)

    def getNextCompareTypePositiveDatum(self, comparetype, datum):
        # find the next instance of matching datum
        # return the matching datum value
        return self.getCompareTypePositiveDatum(comparetype, datum)


    def getFirstCompareTypePositiveSequence(self, comparetype, datum):
        # Find the first instance of matching datum
        # return the sequence value for that datum
        self.softReset()
        self.getCompareTypePositiveDatum(comparetype, datum)
        return self.sequence_list[self.datum_index]

    def getNextCompareTypePositiveSequence(self, comparetype, datum):
        # Find the next instance of matching datum
        # return the sequence value for that datum
        self.datum_index+=1
        self.getCompareTypePositiveDatum(comparetype, datum)
        return self.sequence_list[self.datum_index]






