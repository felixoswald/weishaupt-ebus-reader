# Weishaupt eBus Reader
This script reads and decodes messages from Weishaupt devices using ebus protocol and [ebusd daemon](https://github.com/john30/ebusd).<br>
All Hex-values are reverse engineered by logging the WebUI requests and decode them.<br>
They are processed and sent to ioBroker via MQTT and own home automation API.

Script currently only in German.

## eBus devices / structure
EBUS<br>
&nbsp; ├ WTC-OB<br>
&nbsp; ├ WCM-EM2<br>
&nbsp; ├ WCM-EM3<br>
&nbsp; ├ WCM-SOL<br>
&nbsp; ├ WCM-COM<br>
&nbsp; └ [ESERA eBus to USB converter](https://www.esera.de/produkte/ebus/135/1-wire-hub-platine)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ [Raspberry Pi 3b+](https://www.rasppishop.de/Raspberry-Pi-3-Model-B-14-GHz-64Bit-Quad-Core)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓ via Ethernet/MQTT<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ioBroker<br>

## ressources
- [ebusd](https://github.com/john30/ebusd/wiki)
- [ebusd weishaupt-configuration file by J0Ek3R](https://github.com/J0EK3R/ebusd-configuration-weishaupt)