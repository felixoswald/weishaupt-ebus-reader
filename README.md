# Weishaupt eBus Reader
Read and decode messages from Weishaupt devices using ebus protocol

## structure
EBUS<br>
&nbsp; ├ WTC-OB<br>
&nbsp; ├ WCM-EM2<br>
&nbsp; ├ WCM-EM3<br>
&nbsp; ├ WCM-SOL<br>
&nbsp; ├ WCM-COM<br>
&nbsp; └ eBus to USB converter<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└ Raspberry Pi<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓ via Network/MQTT<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ioBroker<br>

## my devices
- [ESERA eBus to USB converter](https://www.esera.de/produkte/ebus/135/1-wire-hub-platine)
  - [DIY eBus to USB converter](https://ebus.github.io/adapter/)
- [Raspberry Pi 3b+](https://www.rasppishop.de/Raspberry-Pi-3-Model-B-14-GHz-64Bit-Quad-Core)

## additional informations
- [ebusd](https://github.com/john30/ebusd/wiki)
- [ebusd-weishaupt-configuration](https://github.com/J0EK3R/ebusd-configuration-weishaupt)

