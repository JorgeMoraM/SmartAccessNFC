import pymongo
import datetime
import json
import hashlib, binascii
import paho.mqtt.client as mqtt
import time

lastLog = 0

def on_connect(client, userdata, flags, rc):
	print("connected with result code "+str(rc))
	client.subscribe("puertas/#")


def accessCheck(msg, area):
	#global lastLog
	verifiedUsr = False
	ontimeUsr = False
	nfcid=msg.payload.decode()
	print(nfcid) #debug
	nfcid=nfcid.encode('UTF-8')
	dk = hashlib.pbkdf2_hmac('sha256', nfcid, b'salt', 100000)
	hk=binascii.hexlify(dk)
	hk=hk.decode('ascii')
	print(hk) #debug
	if users.find({"id":hk}).count() == 1:
		verifiedUsr = True
		user=users.find_one({"id":hk})
		if timeCheck(user):
			ontimeUsr = True
		user=user["Name"]
		accesslog = {"user":user,"area":area,
		"time":datetime.datetime.now()
		}
		print ("welcome "+user)
	else:
		verifiedUsr = False
		accesslog = {"user":"UNKNOWN USER: "+hk,
		"area":area,
		"time":datetime.datetime.now()
		}
	#if accesslog["user"] != lastLog["user"] or accesslog["area"] != lastLog["area"]:
	db.acceses.insert_one(accesslog)

	#lastLog=accesslog

	return verifiedUsr and ontimeUsr


def main_callback(client, userdata, message):
	area = 1
	if (accessCheck(message, area)):
		client.publish("puertas/principal","PERMITTED")
	else: 
		client.publish("puertas/principal", "DENIED")
	client.disconnect()
#	time.sleep(4)

def protyp_callback(client, userdata, message):
	area = 2
	if (accessCheck(message, area)):
		client.publish("puertas/prototipado","PERMITTED")
	else:
		client.publish("puertas/prototipado","DENIED")
	client.disconnect()
#	time.sleep(4)

def privCheck(user, area):
	areas = user["areas"]
	return area in areas

def timeCheck(user):
	start=datetime.time(int(user["start"]),0,0)
	end=datetime.time(int(user["end"]),0,0)
	t=datetime.datetime.now()
	h=t.hour
	m=t.minute
	s=t.second
	tnow=datetime.time(h,m,s)
	if start <= end:
		return start <= tnow <= end
	else:
		return start <= tnow or tnow <= end

dbclient = pymongo.MongoClient("localhost",27017)
db=dbclient.nfcusers
users=db.users
acceses=db.acceses

while True:
	client = mqtt.Client()
	client.connect("localhost",1883,60)

	client.on_connect = on_connect
	client.message_callback_add("puertas/principal", main_callback)
	client.message_callback_add("puertas/prototipado", protyp_callback)
	time.sleep(3)

	client.loop_forever()

