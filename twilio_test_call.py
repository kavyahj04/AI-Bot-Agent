import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")
to_number = os.getenv("TARGET_NUMBER")
public_base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
print("PUBLIC_BASE_URL =", public_base)
print("VOICE URL =", f"{public_base}/voice")

client = Client(account_sid, auth_token)

# bot_message = """
# <Response>
# <Say voice = "alice">
# Hello,This is a test message"
# <Say/>
# </Response>
# """

call = client.calls.create(
    to=to_number,
    from_=from_number,
    url=f"{public_base}/voice",
    method="POST"
)

print(call.sid)