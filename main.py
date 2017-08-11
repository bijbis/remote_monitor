from producer import ProducerThread
from consumer import ConsumerThread
from queue import Queue
from db import Influx
from SeriesHelper import RemoteMonitor
import time


if __name__ == '__main__':
    q = Queue()
    database = Influx(database='influxDB', user='root', passcode='root', dbname='test',
                      port=8086, host='localhost')
    columns = ['current', 'power', 'voltage', 'total_energy', 'A', 'B', 'C', 'D']
    RemoteMonitor.Meta.client = database.db
    RemoteMonitor.Meta.series_name = 'remote_monitor'
    RemoteMonitor.Meta.fields = columns
    p = ProducerThread(name='ModbusPull', que=q)
    c = ConsumerThread(name='InfluxDBwriter', que=q, db=database, cols=columns)
    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
