import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()


with open('transcripts.json', 'r') as f:
    transcripts = json.load(f)

prompt = f"""You are analyzing {len(transcripts)} call transcripts from a medical clinic AI agent. 

Find bugs and quality issues in the AGENT's responses. For each bug:
- Category (e.g., Context Loss, Name Confusion, Repetition, STT Failure)
- Severity (Critical/Major/Minor)
- Call ID where it occurred
- Specific example from transcript
- Why it matters

Here are the transcripts:

{json.dumps(transcripts, indent=2)}

Provide a structured bug report in markdown format."""

# Call OpenAI
try:
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'gpt-4',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 2000,
            'temperature': 0.3
        }
    )
    
    if response.status_code == 200:
        bug_report = response.json()['choices'][0]['message']['content']
        
        # Save bug report
        with open('BUG_REPORT.md', 'w') as f:
            f.write(bug_report)
        
        print("Bug report generated: BUG_REPORT.md")
        print("\n" + "="*60)
        print(bug_report)
        print("="*60)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f" Error: {e}")