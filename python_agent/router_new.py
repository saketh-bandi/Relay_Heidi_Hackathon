import requests
import re
import json
from datetime import datetime
from mock_db import SPECIALIST_REGISTRY, INSURANCE_PLANS, PROCEDURE_CODES, DIAGNOSIS_CODES
from pdf_generator import create_referral_pdf

# AI-generated code section begins - GitHub Copilot assisted with creating comprehensive medical transcript analysis
# ==========================================
# CONFIGURATION
# ==========================================
# PASTE YOUR N8N URL HERE (Make sure it's the PRODUCTION URL)
N8N_WEBHOOK_URL = "https://bandisaketh.app.n8n.cloud/webhook/d0e00876-000c-4117-a223-4197c37b9611"

def analyze_transcript(transcript_text):
    """
    Comprehensive medical transcript analysis for healthcare referral processing with PDF generation
    """
    print(f"\n🧠 Analyzing transcript: '{transcript_text[:50]}...'")
    
    # 1. EXTRACT PATIENT NAME using regex patterns
    patient_name = extract_patient_name(transcript_text)
    print(f"👤 Patient Identified: {patient_name}")
    
    # 2. EXTRACT CLINICAL CONTEXT for referral reasoning
    clinical_context = extract_clinical_context(transcript_text)
    print(f"📋 Clinical Context: {clinical_context}")
    
    # 3. DETECT SPECIALTY dynamically from registry keys
    detected_specialty = detect_specialty(transcript_text)
    
    if not detected_specialty:
        print("⚠️ No medical specialty detected - likely casual conversation")
        return False

    print(f"✅ Medical Intent Detected: Referral to {detected_specialty.capitalize()}")

    # 4. FIND APPROPRIATE DOCTOR from registry
    doctor = select_doctor(detected_specialty)
    print(f"🔍 Specialist Found: {doctor['name']} at {doctor['clinic']}")
    print(f"📍 Location: {doctor['address']}")
    print(f"⭐ Rating: {doctor['rating']}/5.0")

    # 5. CHECK INSURANCE COVERAGE
    insurance_result = check_insurance_coverage(detected_specialty)
    print(f"💰 Insurance Status: {insurance_result['status']} ({insurance_result['plan']})")
    print(f"💵 Patient Copay: {insurance_result['copay']}")

    # 6. GET RELEVANT MEDICAL CODES with robust fallbacks
    procedure_codes = get_procedure_codes(detected_specialty)
    diagnosis_codes = get_diagnosis_codes(detected_specialty)
    
    # Debug: Print what codes we retrieved
    print(f"🔬 Procedure Codes Retrieved: {len(procedure_codes) if procedure_codes else 0} codes")
    print(f"🧬 Diagnosis Codes Retrieved: {len(diagnosis_codes) if diagnosis_codes else 0} codes")
    
    # 7. GENERATE PDF REFERRAL LETTER
    pdf_filename = create_referral_pdf(
        patient_name=patient_name,
        doctor=doctor,
        insurance_result=insurance_result,
        clinical_context=clinical_context,
        procedure_codes=procedure_codes,
        diagnosis_codes=diagnosis_codes,
        specialty=detected_specialty
    )
    
    # 8. GENERATE PROFESSIONAL HTML EMAIL
    email_html = generate_referral_email_html(
        patient_name=patient_name,
        doctor=doctor,
        insurance_result=insurance_result,
        clinical_context=clinical_context,
        procedure_codes=procedure_codes,
        diagnosis_codes=diagnosis_codes,
        specialty=detected_specialty,
        pdf_filename=pdf_filename
    )
    
    # 9. PREPARE SIMPLIFIED PAYLOAD - Smart Backend, Dumb Pipe Architecture
    n8n_payload = {
        "email": "inumakisalt123@gmail.com",
        "subject": f"Urgent Referral: {patient_name} - {detected_specialty.title()} Consultation",
        "email_html": email_html,
        "pdf_filename": pdf_filename
    }

    # 10. SEND TO N8N WEBHOOK  
    return send_to_n8n(n8n_payload)

def extract_patient_name(text):
    """Extract patient name from transcript using regex patterns"""
    # Pattern 1: "Patient is [Name]"
    pattern1 = r"patient\s+is\s+([A-Za-z\s]+?)(?:\.|,|$)"
    match1 = re.search(pattern1, text, re.IGNORECASE)
    
    # Pattern 2: "for [Name]" or "[Name] needs"
    pattern2 = r"(?:for|patient)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    match2 = re.search(pattern2, text)
    
    # Pattern 3: Direct name mention at start
    pattern3 = r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    match3 = re.search(pattern3, text.strip())
    
    if match1:
        return match1.group(1).strip().title()
    elif match2:
        return match2.group(1).strip()
    elif match3:
        name = match3.group(1).strip()
        # Avoid common words that aren't names
        if name.lower() not in ['okay', 'well', 'so', 'the', 'this', 'please', 'refer']:
            return name
    
    return "Walk-In Patient"

def extract_clinical_context(text):
    """Enhanced clinical context extraction with better symptom detection"""
    # AI-generated code section begins - GitHub Copilot assisted with improved clinical context extraction
    
    # Split text into sentences for better analysis
    sentences = re.split(r'[.!?]+', text)
    
    # Enhanced symptom keywords for better detection
    symptom_keywords = [
        'pain', 'complains', 'swelling', 'headache', 'chest pain', 'shortness of breath',
        'rash', 'lesion', 'mole', 'skin', 'itching', 'burning',
        'joint pain', 'knee pain', 'back pain', 'fracture', 'injury',
        'seizure', 'memory loss', 'confusion', 'numbness', 'tingling',
        'palpitations', 'murmur', 'irregular heartbeat', 'dizziness',
        'anxiety', 'depression', 'symptoms', 'bleeding', 'fever',
        'nausea', 'vomiting', 'fatigue', 'weakness', 'difficulty breathing'
    ]
    
    # Strategy 1: Find sentence with symptoms/complaints
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 10:  # Skip very short fragments
            continue
            
        sentence_lower = sentence.lower()
        for keyword in symptom_keywords:
            if keyword in sentence_lower:
                # Found a symptom sentence - this is likely our clinical context
                context = sentence.strip()
                if len(context) > 15:
                    return context[:200] + ("..." if len(context) > 200 else "")
    
    # Strategy 2: Find sentence before 'refer' keyword
    text_lower = text.lower()
    refer_pos = text_lower.find('refer')
    if refer_pos > 20:
        # Look for sentence before 'refer'
        before_refer = text[:refer_pos].strip()
        # Get the last sentence before 'refer'
        before_sentences = re.split(r'[.!?]+', before_refer)
        if before_sentences and len(before_sentences) > 0:
            last_sentence = before_sentences[-1].strip()
            if len(last_sentence) > 15:
                return last_sentence[:200] + ("..." if len(last_sentence) > 200 else "")
    
    # Strategy 3: Look for sentences with 'presenting with' or 'has been experiencing'
    presentation_patterns = [
        r'presenting with ([^.!?]+)',
        r'has been experiencing ([^.!?]+)',
        r'complaining of ([^.!?]+)',
        r'reports ([^.!?]+)',
        r'suffering from ([^.!?]+)'
    ]
    
    for pattern in presentation_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            context = match.group(0).strip()
            if len(context) > 15:
                return context[:200] + ("..." if len(context) > 200 else "")
    
    # Strategy 4: Fallback to first 150 characters
    fallback_context = text.strip()[:150]
    if len(text.strip()) > 150:
        fallback_context += "..."
    
    return fallback_context if fallback_context else "General consultation requested - no specific symptoms documented"
    
    # AI-generated code section ends

def detect_specialty(text):
    """Dynamically detect medical specialty from registry keys"""
    text_lower = text.lower()
    
    for specialty in SPECIALIST_REGISTRY.keys():
        if specialty in text_lower:
            return specialty
    
    # Check for common synonyms
    specialty_synonyms = {
        "cardiology": ["heart", "cardiac", "cardiologist"],
        "dermatology": ["skin", "dermatologist", "derm"],
        "orthopedics": ["bone", "joint", "orthopedic", "ortho"],
        "neurology": ["brain", "neurologist", "neuro", "nerve"]
    }
    
    for specialty, synonyms in specialty_synonyms.items():
        for synonym in synonyms:
            if synonym in text_lower:
                return specialty
    
    return None

def select_doctor(specialty):
    """Select the best available doctor from the specialty"""
    doctors = SPECIALIST_REGISTRY[specialty]
    # For demo, select highest rated doctor
    return max(doctors, key=lambda x: x['rating'])

def check_insurance_coverage(specialty):
    """Check insurance coverage for the detected specialty"""
    # For demo, using Blue Cross as default patient insurance
    patient_insurance = "Blue Cross"
    plan_details = INSURANCE_PLANS.get(patient_insurance)
    
    if not plan_details:
        return {
            "plan": "Uninsured",
            "status": "SELF-PAY",
            "copay": "100% Patient Responsibility",
            "deductible": "N/A"
        }
    
    is_covered = specialty in plan_details["covered_specialties"]
    
    return {
        "plan": patient_insurance,
        "status": "IN-NETWORK" if is_covered else "OUT-OF-NETWORK",
        "copay": plan_details['copay'] if is_covered else "100% Patient Responsibility",
        "deductible": plan_details.get('deductible', 'N/A')
    }

def get_procedure_codes(specialty):
    """Get relevant CPT procedure codes for the specialty with default fallback"""
    return PROCEDURE_CODES.get(specialty, PROCEDURE_CODES.get("default", []))

def get_diagnosis_codes(specialty):
    """Get relevant ICD-10 diagnosis codes for the specialty with default fallback"""
    return DIAGNOSIS_CODES.get(specialty, DIAGNOSIS_CODES.get("default", []))

def generate_referral_email_html(patient_name, doctor, insurance_result, clinical_context, procedure_codes, diagnosis_codes, specialty, pdf_filename=None):
    """Generate professional HTML referral email - Smart Backend Implementation"""
    # AI-generated code section begins - GitHub Copilot assisted with professional medical referral HTML generation
    
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Format procedure codes for display - Handle both list and dict structures
    procedure_list = ""
    if isinstance(procedure_codes, list) and procedure_codes:
        # Handle list structure (original format)
        for proc in procedure_codes[:3]:  # Show top 3 procedures
            procedure_list += f"<li><strong>{proc['code']}</strong> - {proc['description']} ({proc['cost']})</li>"
    elif isinstance(procedure_codes, dict) and procedure_codes:
        # Handle dict structure (updated format)
        if 'cpt' in procedure_codes and 'desc' in procedure_codes:
            procedure_list += f"<li><strong>{procedure_codes['cpt']}</strong> - {procedure_codes['desc']}</li>"
        else:
            procedure_list += "<li>Standard consultation and evaluation codes apply</li>"
    else:
        procedure_list += "<li>Standard consultation codes will be determined</li>"
    
    # Format diagnosis codes for display - Handle both list and string structures  
    diagnosis_list = ""
    if isinstance(diagnosis_codes, list) and diagnosis_codes:
        # Handle list structure (original format)
        for diag in diagnosis_codes[:3]:  # Show top 3 diagnoses
            diagnosis_list += f"<li><strong>{diag['code']}</strong> - {diag['description']}</li>"
    elif isinstance(diagnosis_codes, str) and diagnosis_codes:
        # Handle string structure (updated format)
        diagnosis_list += f"<li><strong>{diagnosis_codes}</strong> - Pending evaluation</li>"
    else:
        diagnosis_list += "<li>Diagnosis codes to be determined after evaluation</li>"
    
    # Determine network status styling
    network_style = ""
    if insurance_result['status'] == "OUT-OF-NETWORK":
        network_style = "color: #dc3545; font-weight: bold;"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #007bff; margin-bottom: 20px; }}
            .section {{ margin-bottom: 20px; padding: 15px; border: 1px solid #dee2e6; border-radius: 5px; }}
            .context-box {{ background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #6c757d; font-style: italic; }}
            .urgent {{ color: #dc3545; font-weight: bold; }}
            .network-status {{ {network_style} }}
            h1 {{ color: #007bff; margin: 0; }}
            h2 {{ color: #495057; border-bottom: 2px solid #007bff; padding-bottom: 5px; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .info-item {{ margin-bottom: 10px; }}
            .label {{ font-weight: bold; color: #495057; }}
            ul {{ margin: 10px 0; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏥 MEDICAL REFERRAL REQUEST</h1>
            <p><strong>Date:</strong> {current_date}</p>
        </div>

        <div class="section">
            <h2>📋 RECIPIENT INFORMATION</h2>
            <div class="info-item">
                <span class="label">Doctor:</span> {doctor['name']} (NPI: {doctor['npi']})
            </div>
            <div class="info-item">
                <span class="label">Clinic:</span> {doctor['clinic']}
            </div>
            <div class="info-item">
                <span class="label">Address:</span> {doctor['address']}
            </div>
            <div class="info-item">
                <span class="label">Rating:</span> ⭐ {doctor['rating']}/5.0
            </div>
        </div>

        <div class="section">
            <h2>👤 PATIENT INFORMATION</h2>
            <div class="info-grid">
                <div>
                    <div class="info-item">
                        <span class="label">Patient Name:</span> {patient_name}
                    </div>
                    <div class="info-item">
                        <span class="label">Insurance Plan:</span> {insurance_result['plan']}
                    </div>
                </div>
                <div>
                    <div class="info-item">
                        <span class="label">Network Status:</span> 
                        <span class="network-status">{insurance_result['status']}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Patient Copay:</span> {insurance_result['copay']}
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔬 CLINICAL INFORMATION</h2>
            <div class="info-item">
                <span class="label">Action Required:</span> <span class="urgent">Specialist Consultation - {specialty.title()}</span>
            </div>
            
            <div class="info-item">
                <span class="label">Relevant CPT Codes:</span>
                <ul>{procedure_list}</ul>
            </div>
            
            <div class="info-item">
                <span class="label">Potential Diagnosis Codes (ICD-10):</span>
                <ul>{diagnosis_list}</ul>
            </div>
        </div>

        <div class="section">
            <h2>📋 PATIENT HISTORY / NOTES</h2>
            <div class="context-box">
                <strong>Clinical Presentation:</strong><br>
                {clinical_context}
            </div>
            <div style="margin-top: 15px;">
                <div class="info-item">
                    <span class="label">Referral Urgency:</span> Routine (Standard Priority)
                </div>
                <div class="info-item">
                    <span class="label">Referral Type:</span> Specialist Consultation - {specialty.title()}
                </div>
                {f'<div class="info-item"><span class="label">📄 Referral Letter Attached:</span> <strong>{pdf_filename}</strong></div>' if pdf_filename else ''}
            </div>
        </div>

        <div style="margin-top: 30px; padding: 15px; background: #e9ecef; border-radius: 5px; font-size: 0.9em; color: #6c757d;">
            <p><strong>Generated by:</strong> Healthcare Referral Processing System</p>
            <p><strong>Timestamp:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><em>This referral was automatically processed and requires physician review.</em></p>
            {f'<p><strong>📄 PDF Attachment:</strong> {pdf_filename}</p>' if pdf_filename else ''}
        </div>
    </body>
    </html>
    """
    
    return html_template.strip()
    
    # AI-generated code section ends

def send_to_n8n(payload):
    """Send the simplified email payload to n8n webhook - Dumb Pipe Implementation"""
    print(f"🚀 Sending referral email to n8n workflow...")
    print(f"📧 Email Payload Summary:")
    print(f"   Recipient: {payload['email']}")
    print(f"   Subject: {payload['subject']}")
    print(f"   HTML Length: {len(payload['email_html'])} characters")
    print(f"   PDF Attachment: {payload.get('pdf_filename', 'None')}")
    print(f"   Email Type: Professional Medical Referral with PDF")
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ SUCCESS: Referral processed and sent to n8n!")
            print("📧 Email notification should arrive shortly")
            return True
        else:
            print(f"❌ n8n Webhook Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: n8n webhook took too long to respond")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not reach n8n webhook")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False
# AI-generated code section ends

# ==========================================
# TEST RUNNER - Single Test Mode (No Email Spam)
# ==========================================
if __name__ == "__main__":
    print("🧪 Testing Healthcare Transcript Analysis System with PDF Generation")
    print("=" * 70)
    print("ℹ️  Running SINGLE test to avoid email spam")
    
    # Single test: Complete referral with clinical context
    print("\n--- SINGLE TEST: Complete Medical Referral with PDF ---")
    result = analyze_transcript("Patient is John Smith presenting with chest pain and shortness of breath. I am going to refer him to Cardiology for cardiac evaluation.")
    
    if result:
        print("\n✅ SUCCESS: System working correctly!")
        print("📧 One professional referral email sent to n8n")
        print("📄 PDF referral letter generated locally")
    else:
        print("\n❌ FAILED: System detected no medical intent")
    
    print("\n🏁 Single test complete - No email spam!")
    print("\n💡 To test other scenarios, modify the transcript text above")
    print("   Examples:")
    print("   - 'Sarah needs dermatology for her rash'")
    print("   - 'Patient has headaches, refer to neurology'") 
    print("   - 'The weather is nice today' (should fail)")
    
# AI-generated code section ends
