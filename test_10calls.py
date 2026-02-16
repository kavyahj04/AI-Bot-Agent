import os
import time
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio setup
client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

from_number = os.getenv("TWILIO_FROM_NUMBER")
to_number = os.getenv("TARGET_NUMBER")
public_base = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

print("=" * 60)
print("AUTOMATED TEST CALLS - 10 CALLS")
print("=" * 60)
print(f"Target: {to_number}")
print(f"Webhook: {public_base}/voice")
print("=" * 60)
print()

# Store all call SIDs
call_sids = []

# Run 10 calls
for i in range(1, 11):
    print(f"Making call {i}/10...")
    
    try:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=f"{public_base}/voice",
            record=True
        )
        
        call_sids.append(call.sid)
        print(f"Call initiated: {call.sid}")
        
    except Exception as e:
        print(f"Error: {e}")
        call_sids.append(f"FAILED-{i}")
    
    # Wait between calls (except after last one)
    if i < 10:
        print(f"Waiting 1:30 minutes before next call...")
        time.sleep(60)
        print()







print()
print("=" * 60)
print("ALL CALLS COMPLETED!")
print("=" * 60)
print(f"Total calls: {len(call_sids)}")
print()
print("Call SIDs:")
for idx, sid in enumerate(call_sids, 1):
    print(f"  {idx}. {sid}")
print()
print("View transcripts at:")
print(f"   {public_base}/transcript/[CALL_SID]")
print("=" * 60)