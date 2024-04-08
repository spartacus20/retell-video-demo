from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.websockets import WebSocketState
from twilio.twiml.voice_response import VoiceResponse
from retell import Retell
from twilio_server import TwilioClient
import os


app = FastAPI()
twilio_client = TwilioClient()
retell = Retell(api_key= os.getenv('RETELL_API_KEY'))


#Mofify the phone number.
twilio_client.register_phone_agent("+441865951774", os.getenv('RETELL_AGENT_ID'))




load_dotenv(override=True)

@app.post("/twilio-voice-webhook/{agent_id_path}")
async def handle_twilio_voice_webhook(request: Request, agent_id_path: str):
    try:
        # Check if it is machine
        post_data = await request.form()
        if 'AnsweredBy' in post_data and post_data['AnsweredBy'] == "machine_start":
            twilio_client.end_call(post_data['CallSid'])
            return PlainTextResponse("")
        elif 'AnsweredBy' in post_data:
            return PlainTextResponse("")

        call_response = retell.call.register(
            agent_id=agent_id_path,
            audio_websocket_protocol="twilio",
            audio_encoding="mulaw",
            sample_rate=8000, # Sample rate has to be 8000 for Twilio
            from_number=post_data['From'],
            to_number=post_data['To'],
            metadata={"twilio_call_sid": post_data['CallSid']}
        )
        print(f"Call response: {call_response}")

        response = VoiceResponse()
        start = response.connect()
        start.stream(url=f"wss://api.retellai.com/audio-websocket/{call_response.call_id}")
        return PlainTextResponse(str(response), media_type='text/xml')
    except Exception as err:
        print(f"Error in twilio voice webhook: {err}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
