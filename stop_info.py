from config import account_sid, auth_token
from twilio.rest import TwilioRestClient
import json, urllib2, sys

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
	# if route == 442:
	if route == 443:
		message += "Northwood "
	# elif route == 437:
	elif route == 438:
		message += "Burs. "
	message += str(time)
	message += " min to stop\n"
 
message = client.messages.create(to="+12489332002", from_="+12482923363",
	body=message)
