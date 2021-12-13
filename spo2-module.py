import enum
import time
from time import sleep
import serial
import array as arr

PACKET_LENGTH_INDEX=0
PARAMETER_TYPE_INDEX=1
PACKET_TYPE_INDEX=2
PACKET_ID_INDEX=3
SERIAL_BYTE_1_INDEX=4
SERIAL_BYTE_2_INDEX=5
SERIAL_BYTE_3_INDEX=6
SERIAL_BYTE_4_INDEX=7
DATA_INDEX=8
CHECKSUM_INDEX=9

PR_LOW_INDEX=8
PR_HIGH_INDEX=9
SPO2_INDEX=10
PI_LOW_INDEX=11
PI_HIGH_INDEX=12
STATUS_INFO_1_INDEX=13
STATUS_INFO_2_INDEX=14

START_CHAR="fa"
PARAM_TYPE=0x03
DC=0x01
DR=0x02
DA=0x03
DD=0x04
DATA_DEFAULT=0x00
CMD_SUCCESS=0x07
CMD_FAILURE=0x06

#patient type data
PATIENT_TYPE_ADULT=0x00
PATIENT_TYPE_CHILD=0x01
PATIENT_TYPE_NEONATE=0x02

#sesitivity setting data
LOW_SENSITIVITY=0x00
MIDDLE_SENSITIVITY=0x00
HIGH_SENSITIVITY=0x00
HIGHEST_SENSITIVITY=0x00

#packet ID
ANSWER_ID=0x80 #DA
HANDSHAKE_REQ_ID=0x81 #DD
VERSION_INFO_ID=0x82 #DA
MODULE_SELF_TEST_RES_ID=0x83 #DA
REALTIME_WAVEFORM_ID=0x84 #DD
MEASUREMENT_RESULT_ID=0x85 #DD
VARIATION_INDEX_RESULT_ID=0x86 #DD
REPORT_SENSOR_ERR_ID=0x87 #DA
TEMPERATURE_PKT_ID=0x80 #DD
HANDSHAKE_RES_ID=0x01
PKT_SELF_TEST_RES_ENQ_ID=0x03
PATIENT_TYPE_SETTING_ID=0x04
SESITIVITY_SETTING_ID=0x05

def print_pkt(pkt):
    print([hex(x) for x in pkt])

def handshake(ser):
    handshake = bytearray([0xfa,0x0b,0x03,0x01,0x01,0x2f,0x00,0x00,0x00,0x00,0x3f]);
    ser.write(handshake)
    sleep(1)

def module_init():
    ser = serial.Serial("/dev/ttyUSB0",
        baudrate = 9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None)
    handshake(ser)
    ser.reset_input_buffer()
    return ser

def print_mesurement_result(rx_data_list):
    PR_LOW=rx_data_list[PR_LOW_INDEX];
    PR_HIGH=rx_data_list[PR_HIGH_INDEX];
    SPO2=rx_data_list[SPO2_INDEX];
    PI_LOW=rx_data_list[PI_LOW_INDEX];
    PI_HIGH=rx_data_list[PI_HIGH_INDEX];
    
    print("PR_LOW ", end=' : ' )
    print(PR_LOW, end='\t')
    print("PR_HIGH ", end=' : ' )
    print(PR_HIGH, end='\t')
    print("SPO2 ", end=' : ' )
    print(SPO2, end='\t')
    print("PI_LOW ", end=' : ' )
    print(PI_LOW, end='\t')
    print("PI_HIGH ", end=' : ' )
    print(PI_HIGH)

def main():
    ser=module_init()
    while 1:
        #sleep(1)
        rx_data=ser.read_until(expected=bytes.fromhex(START_CHAR))
        rx_data_list=list(rx_data)
    
        if (len(rx_data_list) < 10):
            continue
    
        if (rx_data_list[PARAMETER_TYPE_INDEX] != PARAM_TYPE):
            continue
    
        if (rx_data_list[PACKET_ID_INDEX] == HANDSHAKE_REQ_ID):
            print("Handshake Requested")
            handshake()
            print("Handshake Done")
    
        if ((rx_data_list[PACKET_ID_INDEX] == MEASUREMENT_RESULT_ID) and
                (rx_data_list[PACKET_LENGTH_INDEX] == 0x11)):
            print_mesurement_result(rx_data_list)

main()
