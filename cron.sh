#!/bin/bash
pid=$(cat /home/botski/botski/botski/botski.pid)
check=$(ps aux | grep -v grep | grep $pid)
if [ -z "$check" ]
then
echo "Botski does not seem to be running, attempting to start now."
python /home/botski/botski/botski/main.py &
fi
