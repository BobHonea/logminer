system_fan_remote_sensor_transistor = ["q46", "q49", "q26", "q3"]
fpgaFanRemoteSensor = ["fpga heatsink"]
system_sensor_ids = ["a2", "a4", "a6", "a8"]
fpga_sensor_id = "a0"
epm_sensor_chips = ["u60", "u61", "u62", "u63"]
epm_sensor_address = ["90", "94"]
epm_sensor_channel = ["1", "2"]

epm1_temp_report = "max epm1 temperature f2.2 deg C"
epm2_temp_report = "max epm2 temperature f2.2 deg C"
epm_temp_report = "read temperature from device 0x94 via bus 1: 126.0 C"




testlines = ["sensor A8 local temperature 42.50 deg C remote temperature 0.0 deg C",
             "max EPM1 temperature 42.50 deg C",
             "max EPM2 temperature 42.0 deg C",
             "Fan A2 duty cycle :100, PWM :0xFF"]

printable = [int, float, str, list, dict, tuple]


#   parse_log_events( logfilename, eventfilename)
#
#	fills an open empty eventfile with event records parsed from
#	the open log file
#
#	The log file may be epm, or fpga style.
#	All log events are parsed, regardless of origin file type
#
#   Returns - Integer Results Code

#PARSE_EVENT_UNDEFINED = 0
#PARSE_EVENT_FPGA = 1
#PARSE_EVENT_EPM1 = 2
#PARSE_EVENT_EPM2 = 3
#PARSE_EVENT_LOG_CORRUPT = -1
#PARSE_EVENT_LOG_EMPTY = -2