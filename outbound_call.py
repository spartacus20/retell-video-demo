import os
from twilio_server import TwilioClient
from dotenv import load_dotenv
load_dotenv()
twilio_client = TwilioClient()

#Esto es para hacer outbound calls.
twilio_client.create_phone_call("+441865951774", "+447749592936", os.environ['RETELL_AGENT_ID'])#from,to
