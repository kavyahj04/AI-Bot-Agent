import os
from dotenv import load_dotenv
from fastapi.responses import Response
from fastapi import FastAPI, Request
from twilio.twiml.voice_response import VoiceResponse, Gather

load_dotenv()
app = FastAPI()


#IN-MEMEORY STORAGE
CALL_STATE = {}

#method to generate XML
def twiml_response(vr: VoiceResponse) -> Response :
    return Response(content=str(vr), media_type="text/xml")

#when call gets connected
@app.post("/voice")
async def voice(request: Request):
    
    #get call id
    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    
    #add it to in-memory storage - Coversation Log
    CALL_STATE.setdefault(call_sid, {"turns": [], "turn_count": 0})
    
    patient_text = "Hi, I want to schedule an appointment."

    #store what our bot said and increment the count
    CALL_STATE[call_sid]["turns"].append({"speaker": "patient", "text": patient_text})
    CALL_STATE[call_sid]["turn_count"] += 1

    print(f"[{call_sid}] PATIENT: {patient_text}")
    
    #inform twilio to speak our bot text
    vr = VoiceResponse()

    #TTS
    vr.say(patient_text)

    #after speaking listen to the other person and convert their speech to text, once completed send it to /step
    #STT
    gather = Gather(
        input="speech",
        action="/step",
        method="POST",
        speech_timeout="auto",
    )

    vr.append(gather)

    # If Twilio doesn’t capture speech, it will continue after Gather.
    vr.redirect("/step")
    return twiml_response(vr)

@app.post("/step")
async def step(request: Request):

    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    agent_text = (form.get("SpeechResult") or "").strip()

    CALL_STATE.setdefault(call_sid, {"turns": [], "turn_count": 0})

    if agent_text:
        CALL_STATE[call_sid]["turns"].append({"speaker": "agent", "text": agent_text})
        CALL_STATE[call_sid]["turn_count"] += 1

    patient_text = "Next Monday afternoon would be great. Do you have any openings?"

    CALL_STATE[call_sid]["turns"].append({"speaker": "patient", "text": patient_text})
    CALL_STATE[call_sid]["turn_count"] += 1

    print(f"[{call_sid}] PATIENT: {patient_text}")

    vr = VoiceResponse()

    #TTS
    vr.say(patient_text)

    if CALL_STATE[call_sid]["turn_count"] >= 8:
        vr.say("Thanks. That's all I needed. Bye.")
        vr.hangup()
        return twiml_response(vr)
    
    #STT
    gather = Gather(
        input="speech",
        action="/step",
        method="POST",
        speech_timeout="auto",
    )
    vr.append(gather)

    vr.redirect("/step")
    return twiml_response(vr)

@app.get("/debug/{call_sid}")
def debug(call_sid: str):
   #what we captured
    return CALL_STATE.get(call_sid, {"error": "call_sid not found"})