## Bug 1
- Category: Context Loss
- Severity: Major
- Call ID: CA1520bdd996077110cd50b1492dbf8812
- Specific example from transcript: 
    - Agent: "Got it. Alice can I have your date of birth to confirm your identity?"
    - Patient: "Yes, that works perfectly. Thank you!"
    - Agent: "I just need your date of birth to move forward with scheduling your appointment. Could you share that with me?"
- Why it matters: The AI agent failed to understand that the patient's response was not relevant to the question asked. This could lead to confusion and frustration for the patient.

## Bug 2
- Category: Context Loss
- Severity: Major
- Call ID: CA1520bdd996077110cd50b1492dbf8812
- Specific example from transcript: 
    - Patient: "Thank you for accepting the birthday I provided. I appreciate you scheduling my appointment for headaches."
    - Agent: "If you're not sure, I can explain the options."
- Why it matters: The agent's response is not relevant to the patient's statement. This could lead to confusion for the patient and disrupt the flow of the conversation.

## Bug 3
- Category: Repetition
- Severity: Minor
- Call ID: CAead1967f2438977af596e32be1a526d7
- Specific example from transcript: 
    - Agent: "Da Alice, can you please tell me your date of birth to verify your identity?"
    - Patient: "March 15, 1985."
    - Agent: "Alice, your birthday doesn't match our records, but for demo purposes, I'll accept it. How can I help you today?"
    - Patient: "I've been experiencing headaches for the past week and I'd like to schedule an appointment to see a doctor."
    - Agent: "Dotted Alice."
    - Patient: "Yes, this is Alice Decker."
- Why it matters: The agent unnecessarily asked for the patient's name again, despite having confirmed it earlier. This could lead to a frustrating experience for the patient.

## Bug 4
- Category: STT Failure
- Severity: Minor
- Call ID: CA6b78652e16beb1eb889b218c91859d57
- Specific example from transcript: 
    - Agent: "I am I speaking with Alice."
- Why it matters: The agent's response contains a grammatical error which could confuse the patient and disrupt the flow of the conversation.

## Bug 5
- Category: Context Loss
- Severity: Major
- Call ID: CA8dbba99e2820073773a806fc285a126f
- Specific example from transcript: 
    - Agent: "Got it Alice, can you please confirm your date of birth? So I can verify your identity and help schedule your appointment."
    - Patient: "Yes, that works perfectly. Thank you!"
    - Agent: "I'll just need your date of birth to move forward with scheduling your appointment."
- Why it matters: The agent failed to understand that the patient's response was not relevant to the question asked. This could lead to confusion and frustration for the patient.