from twilio.rest import Client
from dotenv import load_dotenv
import os
import urllib

load_dotenv()
class TwilioClient:

    def __init__(self):
        self.client = Client(
            os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_AUTH_TOKEN"]
        )

    def end_call(self, sid):
        try:
            call = self.client.calls(sid).update(
                twiml="<Response><Hangup></Hangup></Response>",
            )
            print(f"Ended call: ", vars(call))
        except Exception as err:
            print(err)

    def register_phone_agent(self, phone_number, agent_id):
        try:
            phone_number_objects = self.client.incoming_phone_numbers.list(limit=200)
            numbers_sid = ""
            for phone_number_object in phone_number_objects:
                if phone_number_object.phone_number == phone_number:
                    number_sid = phone_number_object.sid
            if number_sid is None:
                print(
                    "Unable to locate this number in your Twilio account, is the number you used in BCP 47 format?"
                )
                return
            phone_number_object = self.client.incoming_phone_numbers(number_sid).update(
                voice_url=f"{os.environ['NGROK_IP_ADDRESS']}/twilio-voice-webhook/{agent_id}"
            )
            print("Register phone agent:", vars(phone_number_object))
            return phone_number_object
        except Exception as err:
            print(err)

    def create_phone_call(self, from_number, to_number, agent_id, custom_variables):

        #Avoid errors.
        if not isinstance(custom_variables, dict):
            custom_variables = {}

        query_string = urllib.parse.urlencode(custom_variables)
        try:
            call = self.client.calls.create(
                machine_detection="Enable",
                machine_detection_timeout=8,
                async_amd="true",
                async_amd_status_callback=f"{os.getenv('NGROK_IP_ADDRESS')}/twilio-voice-webhook/{agent_id}",
                url=f"{os.environ['NGROK_IP_ADDRESS']}/twilio-voice-webhook/{agent_id}?{query_string}",
                to=to_number,
                from_=from_number
            )
            print(f"Call from: {from_number} to: {to_number}")
            return call
        except Exception as err:
            print(err)

    def get_call_status(self, call_id):
        call_status = self.client.calls(call_id).fetch()
        return call_status
