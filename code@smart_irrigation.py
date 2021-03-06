import requests
import sys
import time
import ibmiotf.application
import ibmiotf.device
import random
r=requests.get('http://api.openweathermap.org/data/2.5/weather?q=Guntur,IN&appid=42a67b9e8ecd9620c2fe1471361c3e53')


#Provide your IBM Watson Device Credentials
organization = "w1gnzn"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "123456789"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])

        if cmd.data['command']=='motoron':
                print("Motor is ON")
                
        elif cmd.data['command']=='motoroff':
                print("Motor is OFF")
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()


#print("response is")
#print(r.json())
#for i in r.json():
    #print(i)

#print(r.json()["main"])
#print("temparature value:")
#print(r.json()["main"]["temp"])
while True:
    print("humidity value:")
    print(r.json()["main"]["humidity"])
    hum=r.json()["main"]["humidity"]
    temk=r.json()["main"]["temp"]
    #print("temperature in kelvin is:",temk)
    temperature=temk-272.15
    print("temperature in celcius is:",temperature)
    mois=random.randrange(20,60,2)
    print("moisture level of soil is:",mois)
    if(temperature>32 | mois<35):
        req_sms=requests.get('https://www.fast2sms.com/dev/bulk?authorization=TPnud1eh5Bfyt2FpHoWXGwlC7NSsKYLmIz6MEvRi8a93jgAZbDDvuxwEg9eBdjmP7OLRpJ2MsIhoZ54a&sender_id=FSTSMS&message=Temperature,Moisture%20level%20of%20soil%20are%20improper&language=english&route=p&numbers=7075001212,9121852344')
    data = { 'Temperature' : temperature, 'Moisture': mois, 'Humidity': hum }
        #print (data)
    def myOnPublishCallback():
            print ("Published Temperature = %s C" % temperature, "Humidity = %s %%" % hum, "to IBM Watson")

    success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
            print("Not connected to IoTF")
    time.sleep(2)
        
    deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
