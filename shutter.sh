#!/bin/bash
SHUTTER_PIN=24
if [ ! -d /sys/class/gpio/gpio${SHUTTER_PIN} ]
then
  echo ${SHUTTER_PIN} > /sys/class/gpio/export
  sleep 0.2
fi
echo "Releasing shutter with pin ${SHUTTER_PIN}"
echo "out" > /sys/class/gpio/gpio${SHUTTER_PIN}/direction
echo "1" > /sys/class/gpio/gpio${SHUTTER_PIN}/value
sleep 0.5
echo "0" > /sys/class/gpio/gpio${SHUTTER_PIN}/value
