import os
import json
import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from retell import Retell
from pydantic import BaseModel


router = APIRouter()

RETELL_API_KEY = os.getenv("RETELL_API_KEY")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")


if not RETELL_API_KEY:
    print("RETELL_API_KEY no está configurado en las variables de entorno")
    raise ValueError("RETELL_API_KEY no está configurado")

retell = Retell(api_key=RETELL_API_KEY)

load_dotenv(override=True)


class Item(BaseModel):
    call_id: str


async def send_call_id(item: Item):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            os.getenv("MAKE_WEBHOOK_URL"), json=item.model_dump()
        )
        if response.status_code != 201:
            raise HTTPException(
                status_code=response.status_code, detail="Error calling external API"
            )
        return response.json()


@router.post("/webhook")
async def handle_webhook(request: Request):
    try:
        post_data = await request.json()

        if post_data["event"] == "call_ended":

            if MAKE_WEBHOOK_URL:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        os.getenv("MAKE_WEBHOOK_URL"), json=post_data
                    )
                    if response.status_code != 201:
                        raise HTTPException(
                            status_code=response.status_code,
                            detail="Error calling external API",
                        )
            else:
                print("MAKE_WEBHOOK_URL not configured. Skipping external API call.")
        elif post_data["event"] == "call_started":
            pass
        elif post_data["event"] == "call_analyzed":
            pass
        else:
            print("Unknown event", post_data["event"])
        return JSONResponse(status_code=200, content={"received": True})
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return JSONResponse(status_code=400, content={"message": "Invalid JSON"})
    except KeyError as e:
        print(f"Missing required key in data: {e}")
        return JSONResponse(status_code=400, content={"message": f"Missing required key: {e}"})
    except Exception as e:
        print(f"Unexpected error in webhook: {e}")
        return JSONResponse(status_code=500, content={"message": "Webhook Internal Server Error"})
