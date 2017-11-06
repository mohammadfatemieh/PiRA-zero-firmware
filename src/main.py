#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import BQ2429x
import MCP3021
import smbus as smbus
import RPi.GPIO as GPIO
import time
import os
from resin import Resin
resin = Resin()


def main():

    debug_main()
    # debug_it_all()
    time.sleep(30)

    ## Go to sleep if charging is not connected
    if sensor_bq.get_status(BQ2429x.CHRG_STAT) == "No input" and \
       os.environ['CHARGING_ACTION'] == '1':
        resin.models.supervisor.shutdown(device_uuid=os.environ['RESIN_DEVICE_UUID'], app_id=os.environ['RESIN_APP_ID'])
        print 'Shutting down as scheduled.'
    ## Go to sleep if charging is not connected
    if sensor_bq.get_status(BQ2429x.CHRG_STAT) == "No input":
        print 'No input detected: ' = sensor_bq.get_status(BQ2429x.CHRG_STAT)
    ## Go to sleep if charging is not connected
    if os.environ['CHARGING_ACTION'] == '1':
        print 'env variable detected: ' + os.environ['CHARGING_ACTION']

def debug_main():

    print '==============================================='
    print 'BQ2429x  : status - VBUS_STAT : ' \
        + str(sensor_bq.get_status(BQ2429x.VBUS_STAT))
    print 'BQ2429x  : status - CHRG_STAT : ' \
        + str(sensor_bq.get_status(BQ2429x.CHRG_STAT))
    print 'BQ2429x  : status - PG_STAT ---- : ' \
        + str(sensor_bq.get_status(BQ2429x.PG_STAT))
    print 'MCP3021  : status - voltage --: ' \
        + str(sensor_mcp.get_voltage()) + 'V'


def debug_it_all():

    print '==============================================='
    print 'BQ2429x  : status - VSYS ------- : ' \
        + str(sensor_bq.get_status(BQ2429x.VSYS_STAT))
    print 'BQ2429x  : status - THERM_STAT - : ' \
        + str(sensor_bq.get_status(BQ2429x.THERM_STAT))
    print 'BQ2429x  : status - PG_STAT ---- : ' \
        + str(sensor_bq.get_status(BQ2429x.PG_STAT))
    print 'BQ2429x  : status - DPM_STAT --- : ' \
        + str(sensor_bq.get_status(BQ2429x.DPM_STAT))
    print 'BQ2429x  : status - CHRG_STAT -- : ' \
        + str(sensor_bq.get_status(BQ2429x.CHRG_STAT))
    print 'BQ2429x  : status - VBUS_STAT -- : ' \
        + str(sensor_bq.get_status(BQ2429x.VBUS_STAT))
    print 'BQ2429x  : fault - NTC_FAULT --- : ' \
        + str(sensor_bq.get_faults(BQ2429x.NTC_FAULT))
    print 'BQ2429x  : fault - BAT_FAULT --- : ' \
        + str(sensor_bq.get_faults(BQ2429x.BAT_FAULT))
    print 'BQ2429x  : fault - CHRG_FAULT -- : ' \
        + str(sensor_bq.get_faults(BQ2429x.CHRG_FAULT))
    print 'BQ2429x  : fault - BOOST_FAULT - : ' \
        + str(sensor_bq.get_faults(BQ2429x.BOOST_FAULT))
    print 'BQ2429x  : fault - WATCHDOG_FAULT: ' \
        + str(sensor_bq.get_faults(BQ2429x.WATCHDOG_FAULT))
    print 'MCP3021  : status - voltage -----: ' \
        + str(sensor_mcp.get_voltage())


if __name__ == '__main__':

    #check system variables
    #charging action if system should stay on when on charge, default on
    charging_action=os.getenv('CHARGING_ACTION', 1)
    print 'CHARGING_ACTION: '+ str(charging_action)

    # referencing the sensors

    sensor_bq = BQ2429x.BQ2429x()
    sensor_mcp = MCP3021.MCP3021()

    # configure GPIOs

    timer_en_pin = 17
    rtc_en_pin = 22
    self_en_pin = 18

    timer_done_pin = 27

    # Set GPIO mode: GPIO.BCM or GPIO.BOARD

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(timer_en_pin, GPIO.IN)
    GPIO.setup(rtc_en_pin, GPIO.IN)

    # Check for power-up scenario

    timer_en_state = GPIO.input(timer_en_pin)
    rtc_en_state = GPIO.input(rtc_en_pin)

    # Self-enable

    GPIO.setup(self_en_pin, GPIO.OUT)
    GPIO.output(self_en_pin, 1)

    # Assert done for timer

    GPIO.setup(timer_done_pin, GPIO.OUT)
    GPIO.output(timer_done_pin, 1)

    # convert variable into str

    print 'Timer EN state ' + str(timer_en_state)
    print 'RTC EN state ' + str(rtc_en_state)

    print 'Disable charge timer'
    sensor_bq.set_charge_termination(10010010)
    print 'Configure pre-charge'
    sensor_bq.set_ter_prech_current(1111,0001)

    while 1:
        main()
