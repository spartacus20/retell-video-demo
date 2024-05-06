import urllib.parse
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.websockets import WebSocketState
from twilio.twiml.voice_response import VoiceResponse
from retell import Retell
from twilio_server import TwilioClient
import os
import urllib


app = FastAPI()
twilio_client = TwilioClient()
retell = Retell(api_key=os.getenv("RETELL_API_KEY"))


# jorge
twilio_client.register_phone_agent("", os.getenv("RETELL_AGENT_ID"))


load_dotenv(override=True)


@app.post("/outbound-call")
async def handle_twilio_voice_webhook(request: Request):
    body = await request.json()
    to_number = body.get("to_number")
    custom_varibles = body.get("custom_variables")
    twilio_client.create_phone_call(
        "", to_number, os.environ["RETELL_AGENT_ID"], custom_varibles
    )  # from,to
    return PlainTextResponse("Done")


@app.post("/twilio-voice-webhook/{agent_id_path}")
async def handle_twilio_voice_webhook(request: Request, agent_id_path: str):

    query_params = request.query_params
    custom_variables = {key: query_params[key] for key in query_params}

    try:
        # Check if it is machine
        post_data = await request.form()
        if "AnsweredBy" in post_data and post_data["AnsweredBy"] == "machine_start":
            print(post_data["AnsweredBy"])
            twilio_client.end_call(post_data["CallSid"])
            return PlainTextResponse("")
        elif "AnsweredBy" in post_data:
            return PlainTextResponse("")

        call_response = retell.call.register(
            agent_id=agent_id_path,
            audio_websocket_protocol="twilio",
            audio_encoding="mulaw",
            sample_rate=8000,  # Sample rate has to be 8000 for Twilio
            from_number=post_data["From"],
            to_number=post_data["To"],
            retell_llm_dynamic_variables=custom_variables,
            metadata={"twilio_call_sid": post_data["CallSid"]},
        )
        print(f"Call response: {call_response}")

        response = VoiceResponse()
        start = response.connect()
        start.stream(
            url=f"wss://api.retellai.com/audio-websocket/{call_response.call_id}"
        )
        return PlainTextResponse(str(response), media_type="text/xml")
    except Exception as err:
        print(f"Error in twilio voice webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
