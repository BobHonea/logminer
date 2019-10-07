#
#
# logLine class performs checking of the hand-drawn syntax for the log line
# and generates the log line parse specification for the aggregator
# currently, the log line parse spec for aggregation is drawn by hand
# *** this demands too much of script users
# *** hand designing the initial parse specification is hard enough
#
#

class logLine(object):
    m_logSpec = None
    m_logSpecValid = False
    m_parseSpec = None
    m_parseSpecValid = False

    key = None

    def __init__(self, logSpec: list, key: str):
        self.m_parseSpecValid = self.verifyLogSpec()
        self.m_logSpecValid = self.generateParseSpec()
        return

    def verifyLogSpec(self):
        return False

    def generateParseSpec(self):
        # generate Parse Spec based on Log Spec

        # check
        return False

    def parseSpec(self):
        if self.m_parseSpecValid:
            return self.parseSpec
        else:
            return None


###-----------END---- in PROGRESS DESIGN