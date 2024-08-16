from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

router = APIRouter()


def extract_transcript_and_tools(json_data):
    transcript = []

    for item in json_data["transcript_with_tool_calls"]:
        if item["role"] in ["agent", "user"]:
            speaker = item["role"].capitalize()
            content = item["content"]
            transcript.append(f"{speaker}: {content}")
        elif item["role"] == "tool_call_invocation":
            tool_name = item["name"]
            transcript.append(f"[Agent executes tool: {tool_name}]")

    return "\n\n".join(transcript)


@router.post("/extract_advanced_transcript")
async def handle_webhook(request: Request):
    json_data = await request.json()
    transcript = extract_transcript_and_tools(json_data)
    return JSONResponse({"transcript": transcript}, status_code=200)
