RAVEn to MQTT bridge
====================

This is a little project that monitors a Rainforest RAVEn ZigBee USB Adaptor, and passes along instantaneous and total demand messages to a Mosquitto server.

Configuration is in `server.ini`; an example file is in `server.ini.sample`.

It requires the `paho-mqtt` Python module.

To run:

```
python runner.py server.ini
```
