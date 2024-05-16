import os
import json
import httpx
import asyncio
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from retell import Retell
from pydantic import BaseModel


router = APIRouter()

retell = Retell(api_key=os.getenv("RETELL_API_KEY"))

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
        valid_signature = retell.verify(
            json.dumps(post_data, separators=(",", ":")),
            api_key=str(os.getenv("RETELL_API_KEY")),
            signature=str(request.headers.get("X-Retell-Signature")),
        )

        # if not valid_signature:
        #     print(
        #         "Received Unauthorized",
        #         post_data["event"],
        #         post_data["data"]["call_id"],
        #     )
        #     return JSONResponse(status_code=401, content={"message": "Unauthorized"})

        # MODIFY DEPENDING ON YOUR NEEDS.
        if post_data["event"] == "call_started":

            print("Call started event", post_data["data"]["call_id"])
        elif post_data["event"] == "call_ended":
            #HTTP REQUEST TO MAKE WEBHOOK
            asyncio.create_task(
                send_call_id(Item(call_id=post_data["data"]["call_id"]))
            )
            print("Call ended event", post_data["data"]["call_id"])
        elif post_data["event"] == "call_analyzed":
            print("Call analyzed event", post_data["data"]["call_id"])
        else:
            print("Unknown event", post_data["event"])

        return JSONResponse(status_code=200, content={"received": True})
    except Exception as err:
        print(f"Error in webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
