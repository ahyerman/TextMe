from config import account_sid, auth_token, to_number, from_number
from twilio.rest import TwilioRestClient
import json, urllib2, sys

northwood = [440, 442, 443]
bb = [437, 438, 433, 434]
cn = [414, 415]
cs = [417, 418]
nwx = [412]
d2dn = [420]
d2ds = [419]
ox = [424]

try:
	stop = sys.argv[1]
except:
	print "didnt run script with arg"
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
	message += "Power Center:\n"
elif stop == "149":
	message += "Hutchins:\n"
elif stop == "98":
	message += "Pierpont:\n"
elif stop == "88":
	message += "Cooley:\n"
for bus in bus_at_stop:
	route = bus['route']
	time = bus['avg']
	if route in northwood:
		message += "Northwood "
	elif route in bb:
		message += "Burs. "
	elif route in cn:
		message += "Com. North "
	elif route in cs:
		message += "Com. South "
	elif route in nwx:
		message += "NWX "
	elif route in d2dn:
		message += "D2D North "
	elif route in d2ds:
		message += "D2D Central"
	elif route in ox:
		message += "Ox shuttle "
	message += str(time)
	message += " min to stop\n"

print message 
message = client.messages.create(to=to_number, from_=from_number,
	body=message)
