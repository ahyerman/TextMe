from config import account_sid, auth_token
from twilio.rest import TwilioRestClient
import json, urllib2

stop = "43"

client = TwilioRestClient(account_sid, auth_token)

# object should be JSON response for Power center stop
object = urllib2.urlopen("http://mbus.doublemap.com/map/v2/eta?stop=" + stop)
object = json.load(object)
print object

try:
	bus_at_stop = object['etas'][stop]['etas']
	print object

except:
	bus_at_stop = ""
	print "exception thrown parsing JSON response"

message = ""
if stop == "43":
	message += "\nPower Center:\n"
for bus in bus_at_stop:
	route = bus['route']
	time = bus['avg']
	if route == 442:
		message += "Northwood "
	elif route == 437:
		message += "Burs. "
	message += str(time)
	message += " min to stop\n"
 
# message = client.messages.create(to="+12489332002", from_="+12482923363",
# 	body=message)
