import os
from dotenv import load_dotenv
from fastapi.responses import Response
from fastapi import FastAPI, Request
from twilio.twiml.voice_response import VoiceResponse, Gather
import json
from datetime import datetime
from openai import OpenAI

load_dotenv()
app = FastAPI()


#IN-MEMEORY STORAGE
CALL_STATE = {}

#Loads scenarios.json
def load_scenario(filename="scenarios.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {filename} not found!")
        return None

#Hybrid responses
def get_bot_response(agent_text, scenario):
    agent_lower = agent_text.lower()
    
    best_match = None
    best_match_length = 0
    
    # Check each response rule
    for response in scenario.get("responses", []):
        # Check if any keyword matches
        for keyword in response.get("keywords", []):
            keyword_lower = keyword.lower()
            if keyword_lower in agent_lower:
                if len(keyword_lower) > best_match_length:
                    best_match = response["reply"]
                    best_match_length = len(keyword_lower)
    
    # Return best match or default
    if best_match and best_match_length > 4:
        print(f"Using JSON response : {best_match_length} chars)")
        return best_match
    
    # If no match, return a default
    print(f"Using AI fallback")
    return ask_ai(agent_text, scenario)

#ask openai
def ask_ai(agent_text, scenario):
    persona = scenario.get("persona", {})
    
    prompt = f"""You are a patient calling a medical clinic.

    Your details:
    - Name: {persona.get('name', 'Unknown')}
    - Date of birth: {persona.get('dob', 'Unknown')}
    - Phone: {persona.get('phone', 'Unknown')}
    - Insurance: {persona.get('insurance', 'Unknown')}
    - Reason for visit: {persona.get('reason', 'General checkup')}

    The clinic agent just said: "{agent_text}"

    Respond naturally as this patient would. Keep it brief (1-2 sentences max). Be helpful and answer their question directly.

    Your response:"""

    try:
        import requests
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 100,
                'temperature': 0.7
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"AI API Error: {response.status_code} - {response.text}")
            return "Could you repeat that please?"
            
    except Exception as e:
        print(f"AI Error: {e}")
        return "Could you repeat that please?"

#Save conversation to JSON file
def save_transcript(call_sid, call_data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{call_sid}_{timestamp}.json"
    
    transcript = {
        "call_sid": call_sid,
        "scenario": call_data.get("scenario", {}).get("name", "unknown"),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "turn_count": call_data.get("turn_count", 0),
        "turns": call_data.get("turns", [])
    }
    
    with open(filename, 'w') as f:
        json.dump(transcript, f, indent=2)
    
    print(f"[{call_sid}] Transcript saved: {filename}")
    return filename

#get in XML Format
def twiml_response(vr: VoiceResponse) -> Response :
    return Response(content=str(vr), media_type="text/xml")

#when call gets connected
@app.post("/voice")
async def voice(request: Request):
    
    #get call id
    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    
    # Load scenario
    scenario = load_scenario("scenarios.json")
    if not scenario:
        scenario = {"initial_message": "Hi, I need help.", "responses": []}
            
        # Initialize call state with scenario
    CALL_STATE.setdefault(call_sid, {
            "turns": [], 
            "turn_count": 0,
            "scenario": scenario
    })

    patient_text = scenario["initial_message"]

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

#Conversation continues here
@app.post("/step")
async def step(request: Request):

    form = await request.form()
    call_sid = form.get("CallSid", "unknown")
    agent_text = (form.get("SpeechResult") or "").strip()
    # print(f"[{call_sid}] RAW FORM DATA: {dict(form)}")
    # print(f"[{call_sid}] SPEECH RESULT: '{agent_text}'")

    CALL_STATE.setdefault(call_sid, {
    "turns": [],
    "turn_count": 0,
    "slots": {
        "name_given": False,
        "dob_given": False,
        "reason_given": False
    }
})


    if agent_text:
        CALL_STATE[call_sid]["turns"].append({"speaker": "agent", "text": agent_text})
        CALL_STATE[call_sid]["turn_count"] += 1
        print(f"[{call_sid}] AGENT: {agent_text}")
    else:
        print(f"[{call_sid}] AGENT: (empty or no speech detected)")

    
    #fetch the scenario assigned to it
    scenario = CALL_STATE[call_sid].get("scenario", {})

    if agent_text:
        patient_text = get_bot_response(agent_text, scenario)
    else:
        patient_text = "I'm sorry, I didn't catch that."
    
    CALL_STATE[call_sid]["turns"].append({"speaker": "patient", "text": patient_text})
    CALL_STATE[call_sid]["turn_count"] += 1

    print(f"[{call_sid}] PATIENT: {patient_text}")

    vr = VoiceResponse()

    #TTS
    vr.say(patient_text)

    if CALL_STATE[call_sid]["turn_count"] >= 12:
        vr.say("Thanks. That's all I needed. Bye.")
        print(f"[{call_sid}] ENDING CALL after {CALL_STATE[call_sid]['turn_count']} turns")
        
        save_transcript(call_sid, CALL_STATE[call_sid])
        
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

#View saved transcripts
@app.get("/transcript/{call_sid}")
def get_transcript(call_sid: str):
    import glob
    
    # Find the transcript file
    files = glob.glob(f"{call_sid}_*.json")
    
    if files:
        with open(files[0], 'r') as f:
            return json.load(f)
    else:
        return {"error": "Transcript not found", "call_sid": call_sid}
    
   