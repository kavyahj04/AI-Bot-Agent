import os
from dotenv import load_dotenv
from twilio.rest import Client

#load env variables
load_dotenv()

#required tokens 
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

#safety check
if not account_sid or not auth_token:
    raise ValueError("Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN in .env")

#create twilio Client
client = Client(account_sid, auth_token)

#to list incoming numbers
numbers = client.incoming_phone_numbers.list(limit=5)

for n in numbers:
    print(f"Incoming phone number: {n.phone_number}")