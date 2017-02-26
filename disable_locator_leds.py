#!/usr/bin/python
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.equipment.EquipmentLocatorLed import EquipmentLocatorLed
import argparse

parser = argparse.ArgumentParser(description='Disable all locator leds in a UCS domain.')
parser.add_argument('-i','--ucsm_ip', help='UCSM IP Address',required=True)
parser.add_argument('-u','--ucsm_usr',help='UCSM User', required=True)
parser.add_argument('-p','--ucsm_pw',help='UCSM Password', required=True)
args = parser.parse_args()

# UCSM Login
try:
    handle = UcsHandle(args.ucsm_ip,args.ucsm_usr,args.ucsm_pw)
    handle.login()
except:
    print "Unable to connect to UCSM " + args.ucsm_ip
    raise

# Query for Locator LEDs
locator_leds = handle.query_classid("EquipmentLocatorLed")

# Turn all Locator LEDs off
for locator_led in locator_leds:
    if locator_led.oper_state == 'on':
        parentdn = locator_led.dn.replace('/locator-led','')
        print "Turning off LED on " + parentdn
        mo = EquipmentLocatorLed(parent_mo_or_dn=parentdn, admin_state="off")
        handle.add_mo(mo, True)
        handle.commit()
