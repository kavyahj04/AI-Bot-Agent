Project overview
This project is an automated voice testing system. It places phone calls to a clinic receptionist agent, simulates a patient conversation, saves transcripts, and generates a bug report from the transcripts.

Purpose
The goal of this project is to automatically test a voice receptionist AI instead of manually calling it. The system simulates real patient conversations, collects transcripts, and identifies failures such as repeated questions, incorrect understanding, or conversation loops.

Technologies used
Twilio for telephony and speech processing
OpenAI for transcript analysis and bug detection
FastAPI for webhook server
Railway for cloud hosting and deployment

Conversation logic
The patient responses are not random. Each call loads a predefined scenario. The system tracks what information was already given such as name and date of birth, so it does not repeat answers. If the agent asks something unexpected, the fallback logic generates a reasonable response.



How the system works
Step 1 A call is started using Twilio from a script in this repo
Step 2 Twilio connects the call and requests instructions from the server endpoint /voice
Step 3 The server returns TwiML instructions that tell Twilio what to say and when to listen
Step 4 Twilio listens to the receptionist and converts speech to text
Step 5 Twilio sends the recognized text to the server endpoint /step
Step 6 The server chooses the next patient response and sends back new TwiML
Step 7 This loop continues until the call ends, then the transcript is saved


Files in this repository
app.py
This is the main FastAPI server. Twilio calls these endpoints during a live phone call.
Purpose of app.py
1 It starts the conversation when Twilio hits the /voice endpoint
2 It continues the conversation loop in the /step endpoint by reading SpeechResult from Twilio and choosing the next patient response
3 It stores call state per CallSid in memory so each call has its own turns, turn count, slots, and scenario
4 It ends the call after a maximum number of turns and saves the transcript

scenarios.json
This file contains patient scenarios. A scenario includes the patient goal and details such as name and date of birth. The response logic uses this scenario to decide what the patient should say.

test_10calls.py
This script runs 10 calls automatically. It starts one call at a time and waits between calls. It is used to generate the required set of transcripts.

twilio_test_call.py
This script starts a single call. It is used to quickly test the Twilio setup and confirm that Twilio can reach the deployed server.'

twilio_test.py
This script is a basic Twilio credential check. It confirms that Twilio credentials are correct and the Twilio client can access the account.

collect_transcripts.py
This script collects transcripts and helps organize them for review or submission.

transcripts.json
This file stores saved transcripts for calls. Each transcript includes the call id and the ordered list of turns with speaker and text.

bug_analyzer.py
This script reads transcripts and calls OpenAI to produce a bug analysis summary. It helps identify patterns like misunderstandings, loops, or missing information.

BUG_REPORT.md
This file contains the bug report generated from the transcript analysis.

requirements.txt
This file lists the Python dependencies required to run the project.

Environment variables
Create a file named .env and set the following values
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_FROM_NUMBER
TARGET_NUMBER
PUBLIC_BASE_URL
OPENAI_API_KEY
Notes about PUBLIC_BASE_URL
PUBLIC_BASE_URL is the public URL where Twilio can reach the server.
When deployed on Railway, this should be the Railway service URL.
During local development, this can be an ngrok URL.

How to run locally
1 Install dependencies
pip install -r requirements.txt
2 Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port 5000
3 Set PUBLIC_BASE_URL to your public URL and then run a test call
python twilio_test_call.py
4 Run 10 calls to generate transcripts
python test_10calls.py
5 Generate bug report using OpenAI
python bug_analyzer.py
Deployment on Railway
1 Deploy the FastAPI server app.py on Railway
2 Set all environment variables in Railway
3 Set PUBLIC_BASE_URL to the Railway deployed URL
4 Run the call scripts from your machine using the same environment variables

Expected outputs
10 call transcripts saved in transcripts.json
Bug report saved in BUG_REPORT.md