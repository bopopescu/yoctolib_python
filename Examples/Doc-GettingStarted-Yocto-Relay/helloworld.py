# ********************************************************************
#
#  $Id: helloworld.py 36033 2019-06-28 14:42:17Z seb $
#
#  An example that show how to use a  Yocto-Relay
#
#  You can find more information on our web site:
#   Yocto-Relay documentation:
#      https://www.yoctopuce.com/EN/products/yocto-relay/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yocto_api import *
from yocto_relay import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number> <channel> < A | B >')
    print(scriptname + ' <logical_name> <channel>  < A | B >')
    print(scriptname + ' any <channel> < A | B >')
    print('Example:')
    print(scriptname + ' any 2 B')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')


if len(sys.argv) < 4:
    usage()

target = sys.argv[1].upper()
channel = sys.argv[2]
state = sys.argv[3].upper()

# Setup the API to use local USB devices
errmsg = YRefParam()
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'ANY':
    # retreive any Relay then find its serial #
    relay = YRelay.FirstRelay()
    if relay is None:
        die('No module connected')
    m = relay.get_module()
    target = m.get_serialNumber()

print('using ' + target)
relay = YRelay.FindRelay(target + '.relay' + channel)

if not (relay.isOnline()):
    die('device not connected')

if state == 'A':
    relay.set_state(YRelay.STATE_A)
else:
    relay.set_output(YRelay.STATE_B)
YAPI.FreeAPI()
