import threading
import struct
import time
from modbus import Modbus
from pymodbus3.exceptions import ModbusException
import sys
import os


class ProducerThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, que=None,
                 args=(), kwargs=None, verbose=None):
        super(self.__class__, self).__init__()
        self.target = target
        self.name = name
        self.q = que

    def run(self):
        modbus = Modbus.Modbus('paulharrison.hopto.org')
        while True:
            item = []
            try:
                # Order: [current, power, voltage]
                current_avg = modbus.read(3008, 2)  # 3008 stores average current
                power_avg = modbus.read(3058, 2)    # 3058 stores average power
                voltage_avg = modbus.read(3024, 2)  # 3024 stores average voltage
                total_energy = modbus.read(45098, 2)
                A = modbus.read(45118, 2)  
                B = modbus.read(45120, 2)  
                C = modbus.read(45122, 2) 
                D = modbus.read(45124, 2)
                item.append(current_avg)
                item.append(power_avg)
                item.append(voltage_avg)
                item.append(total_energy)
                item.append(A)
                item.append(B)
                item.append(C)
                item.append(D)
                time.sleep(60)
            except struct.error:
                print('Struct Error exception', file=sys.stderr)
                time.sleep(2)
                os._exit(1)
            except ModbusException:
                print('Modbus I/O exception', file=sys.stderr)
                time.sleep(2)
                os._exit(1)
            self.q.put(item)
