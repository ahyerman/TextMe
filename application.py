from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
#from config import account_sid, auth_token
import twilio.twiml, urllib2, os, json


application = Flask(__name__)

northwood = [440, 441, 442, 443]
bb = [433, 434, 436, 437, 438] #435???
cn = [414, 415]
cs = [417, 418]
nwx_out = [412]
nwx_in = [411]
d2dn = [420]
d2ds = [419]
ox = [424, 425]
night_owl = [423]
number = os.environ['PHONE_NUMBER']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

client = TwilioRestClient(account_sid, auth_token)
 
# message = client.messages.get("MM800f449d0399ed014aae2bcc0cc2f2ec")
# print message.body
fail_string = "couldnt find route servicing stop"\
                "\nText: supported stops\nfor a list of stops we support"

@application.route("/", methods=['POST'])
def send_bus_info():
	"""Respond to message of bus stop with eta info."""
	try:
		# doesnt work right now
		# for some reason request parameters are not around
		# find a way to get them!
		# message_sid = request.form['MessageSid']
		body = request.form['Body']
		print body
	except:
		print "couldnt find message body"
		messages = client.messages.list()
		body = messages[0].body
	
	request = body.lower().strip()
	resp = twilio.twiml.Response()
	if request == "supported stops":
		message = "Supported stops are: pierpont, ugli, markley, "\
			"cclittle, cooley, power center, law, fxb in, fxb out, "\
			"im in, im out, john"
		resp.message(message)
		return str(resp)
		
	if request in ["pierpont", "pp", "98"]:
		stop = "98"
	elif request in ["ugli", "shapiro", "ug", "76"]:
		stop = "76"
	elif request == "markley":
		stop = "29"
	elif request in ["cclittle", "cc", "ccl"]:
		stop = "137"
	elif request in ["power center", "pc"]:
		stop = "43"
	elif request == "cooley":
		stop = "88"
	elif request in ["law", "hutch", "hutchins", "law quad"]:
		stop = "149"
	elif request == "fxb in":
		stop = "94"
	elif request == "fxb out":
		stop = "91"
	elif request == "im out":
		stop = "64"
	elif request == "im in":
		stop = "80"
	elif request == "john":
		stop = "68"
	else:
		resp.message(fail_string)
		return str(resp)
	bus_at_stop = make_req(stop)
	if bus_at_stop == "":	
		resp.message("couldnt find route servicing stop")
		return str(resp)

	message = parse_busses(bus_at_stop, request)
	resp.message(message)
	return str(resp)

def parse_busses(data, request):
	message = str(request)
	message += "\n"
	for bus in data:
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
		elif route in d2dn:
			message += "D2D to Central "
		elif route in d2ds:
			message += "D2D to North "
		elif route in ox:
			message += "Ox shuttle "
		elif route in night_owl:
			message += "Night Owl "
		elif route in nwx_in:
			message += "NWX to north "
		elif route in nwx_out:
			message += "NWX to central "
		message += str(time)
		message += " min to stop\n"
	return message


def make_req(stop):
	object = urllib2.urlopen("http://mbus.doublemap.com/map/v2/eta?stop=" + stop)
	object = json.load(object)
	
	try:
		bus_at_stop = object['etas'][stop]['etas']
		print bus_at_stop
	except:
		bus_at_stop = ""
		print "no routes servicing stop"
	if stop == "98":
		object = urllib2.urlopen("http://mbus.doublemap.com/map/v2/eta?stop=101")
		object = json.load(object)
		try:
			add_stuff = object['etas']["101"]['etas']
			print add_stuff

			for bus in add_stuff:
				bus_at_stop.append(bus)
			print bus_at_stop
		except:
			print "failed getting murfin inbound"

	if stop == "137":
		object = urllib2.urlopen("http://mbus.doublemap.com/map/v2/eta?stop=138")
		object = json.load(object)
		try:
			add_stuff = object['etas']["138"]['etas']
			print add_stuff

			for bus in add_stuff:
				bus_at_stop.append(bus)
			print bus_at_stop
		except:
			print "failed getting cclittle ruthven"

	return bus_at_stop


if __name__ == "__main__":
	application.run(debug=True)
