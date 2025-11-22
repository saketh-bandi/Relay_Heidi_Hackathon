import requests
import re
import json
from mock_db import SPECIALIST_REGISTRY, INSURANCE_PLANS

# ==========================================
# CONFIGURATION
# ==========================================
# PASTE YOUR N8N URL HERE (Make sure it's the PRODUCTION URL)
N8N_WEBHOOK_URL = "https://bandisaketh.app.n8n.cloud/webhook/d0e00876-000c-4117-a223-4197c37b9611" 

def analyze_transcript(transcript_text):
    print(f"\n🧠 Analyzing transcript...")
    
    # 1. EXTRACT SPECIALTY
    detected_specialty = None
    for specialty in SPECIALIST_REGISTRY.keys():
        if specialty in transcript_text.lower():
            detected_specialty = specialty
            break
    
    if not detected_specialty:
        print("⚠️ No specialty found (This is good if the text was just chatting).")
        return False

    print(f"✅ Intent Detected: Referral to {detected_specialty.capitalize()}")

    # 2. FIND DOCTOR
    doctor = SPECIALIST_REGISTRY[detected_specialty][0]
    print(f"🔍 Found Specialist: {doctor['name']} at {doctor['hospital']}")

    # 3. CHECK INSURANCE
    patient_insurance = "Blue Cross" 
    plan_details = INSURANCE_PLANS.get(patient_insurance)
    is_covered = detected_specialty in plan_details["covered_specialties"]
    status_msg = "IN-NETWORK" if is_covered else "OUT-OF-NETWORK"
    print(f"💰 Insurance Check ({patient_insurance}): {status_msg}")

    # 4. PREPARE DATA
    n8n_payload = {
        "patient_name": "Saketh Demo",
        "doctor_name": doctor['name'],
        "hospital": doctor['hospital'],
        "action": f"Referral ({status_msg})",
        "insurance_status": status_msg,
        "copay": plan_details['copay'] if is_covered else "100%",
        "email": "inumakisalt123@gmail.com"
    }

    # 5. SEND TO N8N (This was commented out before!)
    print(f"🚀 Sending data to n8n...") 
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=n8n_payload)
        if response.status_code == 200:
            print("✅ SUCCESS: Sent to n8n! Check your email.")
        else:
            print(f"❌ n8n Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    
    return True

# ==========================================
# TEST RUNNER
# ==========================================
if __name__ == "__main__":
    # This one SHOULD work and send an email
    print("--- TEST 1: Valid Referral ---")
    analyze_transcript("Okay Saketh, I am going to refer you to Cardiology for that checkup.")
    
    # This one SHOULD say "No specialty found"
    print("\n--- TEST 2: Invalid Text ---")
    analyze_transcript("The weather is nice today.")