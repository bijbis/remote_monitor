#!/usr/bin/bash

PIDFILE=/var/run/remote_monitor.pid

case $1 in
   start)
       # Launch your program as a detached process
       python3 "/root/dev/remote_monitor/main.py" 2>> /root/dev/remote_monitor/log &
       # Get its PID and store it
       echo $! > ${PIDFILE} 
   ;;
   stop)
      kill `cat ${PIDFILE}`
      # Now that it's killed, don't forget to remove the PID file
      rm ${PIDFILE}
   ;;
   *)
      echo "usage: scraper {start|stop}" ;;
esac
exit 0
