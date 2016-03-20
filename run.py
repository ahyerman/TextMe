from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
from config import account_sid, auth_token
import twilio.twiml, urllib2

app = Flask(__name__)


client = TwilioRestClient(account_sid, auth_token)
 
# message = client.messages.get("MM800f449d0399ed014aae2bcc0cc2f2ec")
# print message.body


@app.route("/", methods=['GET', 'POST'])
def send_bus_info():
	"""Respond to message of bus stop with eta info."""
	messages = client.messages.list(from_=2489332002,)
	# sid =  messages[0].sid
	body = messages[0].body
	print body	

	resp = twilio.twiml.Response()
	
	if body == "Pierpont":
		stop = "98"
	elif body == "Power center":
		stop = "43"
	elif body == "Cooley":
		stop = "88"
	elif body == "Law":
		stop = "149"
	else:
		resp.message("Couldnt find stop")
		return str(resp)
	
	object = urllib2.urlopen("http://mbus.doublemp.com/map/v2/eta?stop=" + stop)
	object = json.load(objct)
	
	try:
		bus_at_stop = object['etas'][stop]['etas']
	except:
		bus_at_stop = ""
		print "no routes servicing stop"
		resp.message("couldnt find route servicing stop")
		return str(resp)

	message = str(body)
	message += "\n"
	for bus in bus_at_stop:
		route = bus['route']
		time = bus['time']
		#if route == 442:
		if route == 443:
			message += "Northwoord "
		#elif route == 437:
		elif route == 438:
			message += "Burs. "
		message += str(time)
		message += " min to stop\n"

	resp.message(message)
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)
