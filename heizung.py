#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Informationen und Kommentare
# - parameter Array ist config für Abfrage und Berechnung
#   hex request wird mit ebusd gesendet
#   bei addition wird mit folgender Zeile addiert.
#   bei Übersetzung wird kommender Wert (int) über übersetzungsarray getauscht
# - bei Fehlern wird je nach config (maxretry) nach angegebener Zeit (waitretry) wiederholt und erneut versucht. bei zu vielen fehlern wird abgebrochen
# - bei Fehlern beim senden, wird in log datei geschrieben
# - waitbetween = Zeit in sekunden zwischen parametern (nicht zu gering, sonst wird bus kommunikation beeinträchtigt!)
# - waitafter = Zeit in Sekunden zwischen kompletten Abfragen (5min sind ok.)

import os
import paho.mqtt.client as mqtt
import time
from datetime import datetime

# 	 		   name bzw. mqtt-pfad				 hex request      Multiplikator			 addition		 negation   Einheit	   Übersetzung
parameter = [['OB/i11_LeistungAktuell',			'08502203d85010',			0.1,			False,			False,		'kW',		0 ],
			 ['OB/i12_TempAussenMittel',		'085022037e0c0a',			0.1,			False,			 True,		'°C',		0 ],
			 ['OB/i13_Waermeanforderung',		'08502203b80200',			0.1,			False,			False,		'°C',		0 ],
			 ['OB/i30_TempVLKessel',			'08502203941d0c',			0.1,			False,			False,		'°C',		0 ],
			 ['OB/i31_TempAbgas',			    '08502203094501',			0.1,			False,			False,		'°C',		0 ],
			 ['OB/i33_TempAussen',			    '08502203740c00',			0.1,			False,			 True,		'°C',		0 ],
			 ['OB/i34_TempWW_TSO_B3',			'08502203cc0e00',			0.1,			False,			False,		'°C',		0 ],
			 ['OB/i40_SchaltspielBrenner',		'08502203d07d0c',		 1000.0,			 True,			False,		'',			0 ],
			 ['OB/i40_SchaltspielBrenner',		'085022038c7c0c',			1.0,			False,			False,		'',			0 ],
			 ['OB/i42_BetrStundenBrenner',		'08502203687f0c',		 1000.0,			 True,			False,		'h',		0 ],
			 ['OB/i43_BetrStundenBrenner',		'08502203347e0c',			1.0,			False,			False,		'h',		0 ],
			 ['OB/i45_LetzteWartung',			'085022030abc02',		   10.0,			False,			False,		'h',		0 ],
			 ['OB/i46_OelZaehler_1000',			'0850220336d00e',		 1000.0,			 True,			False,		'l',		0 ],
			 ['OB/i47_OelZaehler',			    '085022036ad10e',			1.0,			False,			False,		'l',		0 ],
			 ['SOL/901_TempPufO_TPO_B10',		'f6502203607600',			0.1,			False,			False,		'°C',		0 ],
			 ['SOL/901_TempPufU_TPU_B11',		'f6502203ac7800',			0.1,			False,			False,		'°C',		0 ],
			 ['SOL/902_StatusDTR',			    'f65022035af102',			1.0,			False,			False,		'',		 	1 ],
			 ['SOL/903_TempKollektor_TKO_T1',	'f650220332290a',			0.1,			False,			 True,		'°C',		0 ],
			 ['SOL/903_TempSolU_TSU_T2',		'f6502203d62a0a',			0.1,			False,			False,		'°C',		0 ],
			 ['SOL/904_TempSolVL_TKV_T3',		'f65022038a2b0a',			0.1,			False,			False,		'°C',		0 ],
			 ['SOL/904_TempSolRL_TKR_T4',		'f6502203422c0a',			0.1,			False,			False,		'°C',		0 ],
			 ['SOL/905_Durchfluss',			    'f6502203488200',			0.01,			False,			False,		'l/min',	0 ],
			 ['SOL/905_Leistung',			    'f650220385db01',			0.001,			False,			False,		'kW',		0 ],
			 ['SOL/906_ErtragSeit_Wh',			'f6502203388700',			0.001,			 True,			False,		'',			0 ],
			 ['SOL/906_ErtragSeit_kWh',			'f6502203a88800',			1.0,			 True,			False,		'',			0 ],
			 ['SOL/906_ErtragSeit_MWh',			'f6502203f48900',		 1000.0,			False,			False,		'kWh',		0 ],
			 ['SOL/906_ErtragResetDat_Tag',		'f6502203aa8106',			1.0,			False,			False,		'dd',		0 ],
			 ['SOL/906_ErtragResetDat_Mon',		'f6502203f68006',			1.0,			False,			False,		'mm',		0 ],
			 ['SOL/906_ErtragResetDat_Jahr',	'f6502203627f06',			1.0,			False,			False,		'yy',		0 ],
			 ['SOL/907_ErtragSum_Wh',			'f6502203867c06',			0.001,			 True,			False,		'',			0 ],
			 ['SOL/907_ErtragSum_kWh',			'f6502203da7d06',			1.0,			 True,			False,		'',			0 ],
			 ['SOL/907_ErtragSum_MWh',			'f65022033e7e06',		 1000.0,			False,			False,		'kWh',		0 ],
			 ['SOL/908_ErtragSum_Wh',			'f6502203628606',			0.001,			 True,			False,		'',			0 ],
			 ['SOL/908_ErtragSum_kWh',			'f65022033e8706',			1.0,			False,			False,		'kWh',		0 ],
			 ['HK2/413_TempVL_FBH',			    '51502203900f00',			0.1,			False,			False,		'°C',		0 ],
			 ['HK3/523_TempVL_HK',			    '52502203900f00',			0.1,			False,			False,		'°C',		0 ]]

uebersetzung = [[''],
	[' ','Frost','Hand','Not','Pump.schutz','AP unten','Kennlinie','Stagnat','aus','Sol.Energie','Rückkühlung','K-Schutz','Sonder','Stabilisierung','Ertrag','Regelung'] #SOL/902/StatusDTR
]

# settings
tempfile = '/tmp/ebusread'
mqtttopic = 'heizung'
waitbetween = 5
waitafter = 300
waitretry = 2
maxretry = 2

# init
antwort = ''
lsb_hex = ''
lsb_int = 0
hsb_hex = ''
hsb_int = 0
wert = 0.00
retry = 0
x = 0
hsb_bin = '00000000'
vorzeichen = ''

print("[INFO] eBus Reading 2.5.1")
print("------------------------------------------------------------------------------")
print("[INFO] Tempfile: %s" % (tempfile))

# mqtt connect
def on_connect(client, userdata, flags, rc):
        print("[MQTT] connected with code " + str(rc))
print("[MQTT] connecting to 192.168.178.88:1883 ...")
client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.178.88", 1883, 60)
print("[MQTT] Topic: %s" %(mqtttopic))
client.loop_start()

print(" ")

while True:
	# array loop
	with open('negation.log', 'a') as negation:
		now = datetime.now()
		negation.write('\n%s;' % (now.strftime("%Y-%m-%d %H:%M:%S")))

	while x < len(parameter):
		if retry == 0 and wert == 0:
			print(" ")

		try:
			## abfrage
			os.system('ebusctl hex %s > %s' % (parameter[x][1], tempfile))
			with open(tempfile, 'r') as file:
				antwort = file.read().replace('\n', '')
			print("[eBus] %-9s : %6s" % (parameter[x][0], antwort))

			# wandlung & berechnung
			lsb_hex = antwort[2:4]
			hsb_hex = antwort[4:6]

			if parameter[x][4] == False: # für Werte die nicht negativ werden
				lsb_int = int(lsb_hex, 16)
				hsb_int = int(hsb_hex, 16)
				wert += ((lsb_int + hsb_int * 256) * parameter[x][2])
			else:
				lsb_bin = "{0:08b}".format(int(lsb_hex, 16))
				hsb_bin = "{0:08b}".format(int(hsb_hex, 16))
				lsb_int = int(lsb_hex, 16)
				hsb_int = int(hsb_hex, 16)
				lsb_bin_negiert = lsb_bin.replace('0', '#').replace('1', '0').replace('#', '1')
				hsb_bin_negiert = hsb_bin.replace('0', '#').replace('1', '0').replace('#', '1')
				lsb_int_negiert = int(lsb_bin_negiert, 2)
				hsb_int_negiert = int(hsb_bin_negiert, 2)

				if lsb_bin[0] == '0': #positiv
					wert += ((lsb_int + hsb_int * 256) * parameter[x][2])
					vorzeichen = '+'
				else: #negativ
					# wert += ((((lsb_int_negiert +1) / 256) + hsb_int_negiert) * parameter[x][2] * (-1))
					wert -= ((lsb_int_negiert + 1) + hsb_int_negiert / 256) * parameter[x][2]
					vorzeichen = '-'

				## debug Negation!
				with open('negation.log', 'a') as negation:
					negation.write(';%s;%s;%s;%s;%s;%s;%s;%s;%s;%d;%d;%d;%d;%s;%.4f;' % (parameter[x][0], parameter[x][1], antwort, lsb_hex, hsb_hex, lsb_bin, hsb_bin, lsb_bin_negiert, hsb_bin_negiert, lsb_int, hsb_int, lsb_int_negiert, hsb_int_negiert, vorzeichen, wert))

			print("[eBus] Wert: %.2f" %(wert))
			
			# mqtt send
			if parameter[x][3] == False:
				if parameter[x][6] == 0:
					print("[MQTT] Sende Wert: %.2f %s" %(wert, parameter[x][5]))
					client.publish('%s/%s/wert' % (mqtttopic, parameter[x][0]), wert, 1)
				else:
					print("[MQTT] Sende Wert: %s" %(uebersetzung[int(parameter[x][6])][int(wert)]))
					client.publish('%s/%s/wert' % (mqtttopic, parameter[x][0]), uebersetzung[int(parameter[x][6])][int(wert)], 1)
				client.publish('%s/%s/einheit' % (mqtttopic, parameter[x][0]), parameter[x][5], 1)
				wert = 0.00
			else:
				print("[MQTT] Senden übersprungen. Warte auf Addition")

			# sleep
			time.sleep(waitbetween)
			retry = 0
			x += 1
		except KeyboardInterrupt:
			print("Strg+C: Script abgebrochen!")
			break
		except:
			if retry < maxretry:
				print("[WARN] Retry %d" %(retry+1))
				retry += 1
				time.sleep(waitretry)
			else:
				print("[WARN] Fehler. Datensatz übersprungen!")
				if parameter[x][3] == False:
					if wert != 0:
						now = datetime.now()
						with open('heizung-error.log', 'a') as errorlog:
						    errorlog.write('%s;%s;%.2f\n' % (now.strftime("%Y-%m-%d %H:%M:%S"), parameter[x][0], wert))
					x += 1
				else:
					print("[WARN] Gesamte Addition wird übersprungen!")
					if parameter[x+1][3] == False:
						x += 2
					elif parameter[x+2][3] == False:
						x += 3
					elif parameter[x+3][3] == False:
						x += 4

				retry = 0
				wert = 0.00


	print("[INFO] Fertig. Waiting ...")
	time.sleep(waitafter)
	x = 0

# clean
os.remove(tempfile)
