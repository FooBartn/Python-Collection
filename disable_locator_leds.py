#!/usr/bin/python
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.equipment.EquipmentLocatorLed import EquipmentLocatorLed
import sys, getopt

def main(argv):

    try:
        opts,args = getopt.getopt(argv,"h:i:u:p:",["ucsm_ip=","ucsm_usr=","ucsm_pw"])
    except getopt.GetoptError:
        print 'disable_locator_leds.py -ip <ucsm ip address> -usr <ucsm user name> -pw <ucsm password>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'disable_locator_leds.py -i <ucsm ip address> -u <ucsm user name> -p <ucsm password>'
            sys.exit()
        elif opt in ("-i", "--ucsm_ip"):
            ucsm_ip = arg
        elif opt in ("-u", "--ucsm_usr"):
            ucsm_usr = arg
        elif opt in ("-p", "--ucsm_pw"):
            ucsm_pw = arg
    
    # UCSM Login
    try:
        handle = UcsHandle(ucsm_ip,ucsm_usr,ucsm_pw)
        handle.login()
    except:
        print "Unable to connect to UCSM " + ucsm_ip
        raise
    
    # Query for Locator LEDs
    locator_leds = handle.query_classid("EquipmentLocatorLed")
    
    # Turn all Locator LEDs off
    for locator_led in locator_leds:
        if locator_led.oper_state == 'on':
            parentdn = locator_led.dn.replace('/locator-led','')
            print "Turning off LED on " + parentdn
            mo = EquipmentLocatorLed(parent_mo_or_dn=parentdn, id="1", admin_state="off", board_type="single", name="")
            handle.add_mo(mo, True)
            handle.commit()

if __name__ == '__main__':
    main(sys.argv[1:])
