# !/usr/bin/python
#
# test the methods of Data Sequence

import mculog_data_sequence as ds
import unittest


testDataSet = [ [0, 22], [2, 33], [3, 22], [6, 100], [9, 44], [16, 33],
                 [17, 24], [20, 33]]

DATASET_ITEMS = len(testDataSet)


# create sequencer
# add sequence of data, autosequence
# verify data set size
# reset sequencer
# verify reset


def unit_test_1():

    seqData = ds.sequencedData(ds.compareNumber)
    for pair in testDataSet:
        seqData.appendSequencedDatum(pair[0],pair[1])

    # verify that the count of items in sequence matches the source
    assert(DATASET_ITEMS == seqData.getDatumCount())


    # verify that the data match the source
    seqData.setDatumIndex(0)

    for datumIndex in range(0, DATASET_ITEMS):
        if datumIndex==0:
            assert(testDataSet[datumIndex][1] == seqData.getFirstDatum())
        else:
            assert(testDataSet[datumIndex][1] == seqData.getNextDatum())
        datumIndex+=1

    seqData.hardReset()
    assert(seqData.getDatumCount() == 0)

    print("unittest 1 complete")
    return True



# create sequencer
# add sequence of data, autosequence
# verify sequence of key data items
# destroy data set
def unit_test_2():
    #print("begin unit test 2")
    seqData = ds.sequencedData(ds.compareNumber)
    for pair in testDataSet:
        seqData.appendSequencedDatum(pair[0],pair[1])



    sequence = seqData.getFirstMatchingDatumSequence(22)
    assert(sequence == 0)
    sequence = seqData.getNextMatchingDatumSequence(22)
    assert(sequence == 3)

    print("unittest 2 complete")
    return True

# create sequencer
# add sequence of data, autosequence
# test get_..._comparetype_positive_datum()
# find datum greater than reference, verify sequence
# find datum less than reference, verify sequence
# find datum not equal to reference, verify sequence
# find datum equal to reference, verify sequence
# destroy data set
def unit_test_3():
    #print("begin unit test 2")
    seqData = ds.sequencedData(ds.compareNumber)
    for pair in testDataSet:
        seqData.appendSequencedDatum(pair[0],pair[1])

    seqData.getFirstCompareTypePositiveDatum(ds.COMPARE_AB_EQUAL, 22)
    sequence = seqData.getCurrentSequence()
    assert(sequence == 0)

    seqData.getNextCompareTypePositiveDatum(ds.COMPARE_AB_UNEQUAL,22)
    sequence = seqData.getCurrentSequence()
    assert(sequence == 2)

    seqData.getNextCompareTypePositiveSequence(ds.COMPARE_A_LT_B,33)
    sequence = seqData.getCurrentSequence()

    assert(sequence == 3)

    seqData.getNextCompareTypePositiveSequence(ds.COMPARE_A_GT_B, 25)
    sequence = seqData.getCurrentSequence()
    assert(sequence == 6 )

    print("unittest 3 complete")
    return True


test_list = [ unit_test_1, unit_test_2, unit_test_3]


def main():
    for test in test_list:
        assert(test())
    return


if __name__== "__main__":
  main()
