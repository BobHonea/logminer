import thermreg_main as TLogParse


## Thermal Test Runner : (ThermalTestRunner.py)
##
## This is the main() driver for the Thermal Log Reviewer
##
## This module is the top level management for the
## Log Review Process.

## REVIEW OF REQUIREMENTS
## ======================
## The processing of a Log File depends on its definition.
## Atomis of Meanings:  The least unit of meaning is a single number or word.
## Meaning Package:     The common aggregation of meanings is a single text line.
##                      Call it a "log-line".
## Independence:        each log-line and its elements are semantically independent of
##                      other log-lines, and their elements.
## Consistency:         The underlying source code that generates a log-line type is fixed
## Definability:        The syntax of a log-line type is fixed, and can be extrapolated
## Feasibility:         A syntax language (tokens, meanings, rules) exists which can
##                      express precisely the syntax of each log-line type.
## Code-ability:        The complexity of the syntax for interpreting the log-lines can be
##                      about the same as the complexity of the code which generates it.
##                      The underlying code exists:: the decoding syntax can be implemented.
##
## Modularizeable:      base-class::
#                       The base design of all log lines, and of the ensemble of log-lines
##                      occurring in each log-file-type extend generally from design rules
##                      existing in the log-line generating files. This consistency can be
##                      discerned, defined, and employed to generate a base class for log-line
##                      parsing of acceptable complexity.
##
##                      parsing-process:
#                       Each log-file type can be processed with algorithms extended from
##                      a single parsing base-class.
##
##                      parsing-process-regularity and re-useability:
#                       The process of parsing is consistent among all log-files and may be
##                      analyzed, and implemented by a regular set of processes that employ
##                      parsing classes extended from the base-class, and initialized with
##                      key definitions and log-line rules for that log-file.
##
## Stress Relief:       Now that these key design issues have been confronted and expressed,
##                      They can guide and empower the process of design and implementation.
##                      If one of the principles proves defective, the design foundation must
##                      be revisited or abandoned.
##
##
## 1. Instantiate Log Parser
## 2. Provision Log Parser with:
##      a) Log Line Definitions
##      b) Data IDs / keys
##
## 3. Instantiate Data Sequencers
## 4. Provision Data Sequencers with:
##      a) Data Demand Profiles
##      b) Data Record Profile
##
## 5. Instantiate Data Dispatch Manager
## 6. Provision Data Dispatch Mgr. with:
##      a) Data Sequencer Manifest
##      b) Log Line Manifest
##      c) Data Manifest
##
##  7. Drive Log Parser process, produce data for analysis
##      a) for each of FPGA, EPM1, EPM2
##          i)      from all the parameter values used in a log-file:
##                  derive sets of parameter values that express the same
##                  exact 'type of meaning'; e.g. fan-speed, fan-socket ID...
##
##          ii)     define a keyword that names each parameter set.
##          iii)    list all the parameter sets used in the log-file.
##                  as  list whose elements are [ parameter-set-keword, [parameter-set] ]
##          iv)     for each distinct log-line type:
##                  1. derive its syntax
##                  2. express its syntax using logparse-class-syntax.
##                  3. list the syntaxa of all log-line types in the log-file
##          v)      list of parameter-sets (iii), and log-line syntaxa (iv) define the
##                  unique configuration of the logparse class required to parse
##                  the given log-file
##
##          vi)     The analysis of the log-file requires a database of log data
##                  searchable by sequence-or-time to facilitate discovery of the system
##                  evolution, and supporting review of its conformance to system constraints.
##
##          vii)    Each data type requires a database definition, and a record definition,
##                  where each record is emitted upon parsing a single log line.
##
##          viii)   As log-lines are parsed in order of occurance in the log-file, their
##                  data payload must be distributed to the appropriate database(s) as
##                  they are parsed.
##
##          ix)     each specific database:
##                  1. must be defined before parsing begins.
##                  2. must retain all information entered, searchable by sequence-or-time.
##                  3. must be accessible, post-parsing, by the analysis process(es).
##                  4. must expose the semantic format of its record type(s), to facilitate
##                     data access.
##
##          x)      the process of parsing a log-file can therefore be expressed as three
##                  phases:
##                  1.  log-parse set-up
##                  2.  log-parse to database(s)
##                  3.  analysis of log-file data from database(s).
##                  4.  report of specific, and general system performance, as logged.
##
##          xi)     log-parse set-up comprises:
##                  1.  instantiation of a logparse class
##                  2.  registration of log-line syntaxa for the logfile
##                  3.  registration of parameter-sets supporting the syntaxa
##                  4.  instantiation of databases to receive parser output data
##                  5.  registration of each database's data-demand from the registered
##                      log-line syntaxa.
##
##          xii)    log-parse to database(s) comprises:
##                  1.  line-by-line intake and parsing of all lines of a log-file
##                  2.  ill-formed, and blank lines may be withheld from parsing
##                  3.  for each database with a registered data demand:
##                      i)  presentation of demanded parsed log-line dataset do databse
##                          for inspection storage of relevant data items.
##                      ii) accumulation and/or refactoring of data into records for retrieval
##                          and analysis.
##                      iii)storage of completed datasets into indexable database.
##
##          xiii)   log-data analysis comprises:
##                  1. generation of a report of conformance to specification
##                  2. generation of data sampling, reduction, or chart to express
##                     human digestible data and insights.
##
##
##
##  8. Drive the Log Analyzer and Report Generator
##      a) generate min/max data history
##      b) generate alert on/off history
##      c) generate alert on/off expectation history
##      d) generate fanspeed change history
##          d.1) System Fanspeed (a2..a8)
##          d.2) FPGA Fanspeed (a0)
##      e) generate fanspeed change expectation histories (x.1, x.2)
##      f) generate fanspeed change hysteresis verification (x.2, x.2)
##      g) generate alert on/off verification
##      h) generate defect list
##      i) generate pass/fail declaration
##
##  9. Done





def main():



    ## for each file possible (epm1, epm2, fpga)
    ## verify file available and open file


    ## for each file / board
    ##







if __name__ == "__main__":
    main()