import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

call_sids = [
    "CA1520bdd996077110cd50b1492dbf8812",
    "CAd4480833609e5b69d23507b584a62db3",
    "CA6b78652e16beb1eb889b218c91859d57",
    "CAead1967f2438977af596e32be1a526d7",
    "CA6ffcfd4737ee931daa7db164c3b1a27c",
    "CA8dbba99e2820073773a806fc285a126f",
    "CAde1076c610f02e2f81c2bc62d74c57db",
    "CA81762d61ad65a671d7d37a876d617beb",
    "CA5e1efd2252c224373a568871c96b34ba",
    "CA3099f0ec095db7433443b8ea1cd2a343"
]

base_url = os.getenv("PUBLIC_BASE_URL")

all_transcripts = []

print("Fetching")
for i, call_sid in enumerate(call_sids, 1):
    print(f"  {i}/10: {call_sid}")
    
    try:
        url = f"{base_url}/transcript/{call_sid}"
        response = requests.get(url)
        
        if response.status_code == 200:
            transcript = response.json()
            all_transcripts.append(transcript)
            print(f"Fetched")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Save all transcripts to one file
output_file = "transcripts.json"
with open(output_file, 'w') as f:
    json.dump(all_transcripts, f, indent=2)

print(f"\All transcripts saved to: {output_file}")
print(f"Total calls: {len(all_transcripts)}")