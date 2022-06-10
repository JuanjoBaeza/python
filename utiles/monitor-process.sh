#!/bin/bash

# Launch in remote with ssh root@MachineB 'bash -s' < monitor-process.sh

PROC=mc
LOG=/home/juanjo/Alertas/logfile.log

echo "" > $LOG

ORIGPID=`ps -ef | grep -v grep | grep "$PROC" | awk '{print $2}'`

while true;
  do
    PID=`ps -ef | grep -v grep | grep "$PROC" | awk '{print $2}'`
    echo `date -u` " "  $PID >> $LOG
    sleep 2
    echo $PID

      if [[ $PID -ne $ORIGPID ]]
      then
       echo "The PID changed, new PID: $PID"
       echo "Sending email alert"
       exit 0
      fi
  done
exit