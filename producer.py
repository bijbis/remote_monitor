import threading
import struct
import time
from modbus import Modbus
from pymodbus3.exceptions import ModbusException


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
                power_avg = modbus.read(3057, 2)    # 3057 stores average power
                voltage_avg = modbus.read(3024, 2)  # 3024 stores average voltage
                item.append(current_avg)
                item.append(power_avg)
                item.append(voltage_avg)
            except struct.error:
                continue
            except ModbusException:
                continue
            self.q.put(item)
            time.sleep(4)
