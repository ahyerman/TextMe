# TextMe
An application leveraging twilio API to send SMS updates about bus arrival time.

Tired of constantly checking a map to find the nearest bus, I used twilio and doublemap API to create a seamless application to update me on bus information. Inside this repo you'll find two python files. One contains a script to run using a cron job or at utility to update bus arrival times at a set time every week. The other, a back end to a server allowing a nice sms feature.

To use this application, you will need to set up a free account on twilio. The needed variables are a twilio SID, auth token, and phone number. Once these are acheived, a script can be run with the at utility similar to weekly.sh.

The server is easily deployed with dependencies noted in requirements.txt. I opted to deploy on aws ec2. Once deployed, copy the public IP or domain name to your twilio phone number (in twilio settings) and you should be good to go!

Note: This repo does not contain config.py. In order to run the script you will
need to create config.py in the working directory and put the variables account_sid and auth_token
