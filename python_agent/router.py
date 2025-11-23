import requests
import re
import json
import base64
import os
import glob
import subprocess
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
    
    # 2. EXTRACT NEW PATIENT FIELDS
    patient_dob = extract_patient_dob(transcript_text)
    patient_age = extract_patient_age(transcript_text)
    patient_sex = extract_patient_sex(transcript_text)
    patient_complaint = extract_patient_complaint(transcript_text)
    
    print(f"📅 Patient DOB: {patient_dob or 'Not provided'}")
    print(f"🎂 Patient Age: {patient_age or 'Not provided'}")
    print(f"👫 Patient Sex: {patient_sex or 'Not provided'}")
    print(f"🏥 Chief Complaint: {patient_complaint or 'Not specified'}")
    
    # 3. EXTRACT CLINICAL CONTEXT for referral reasoning
    clinical_context = extract_clinical_context(transcript_text)
    print(f"📋 Clinical Context: {clinical_context}")
    
    # 4. DETECT SPECIALTY dynamically from registry keys
    detected_specialty = detect_specialty(transcript_text)
    
    if not detected_specialty:
        print("⚠️ No medical specialty detected - likely casual conversation")
        return False

    print(f"✅ Medical Intent Detected: Referral to {detected_specialty.capitalize()}")

    # 5. FIND APPROPRIATE DOCTOR from registry
    doctor = select_doctor(detected_specialty)
    print(f"🔍 Specialist Found: {doctor['name']} at {doctor['clinic']}")
    print(f"📍 Location: {doctor['address']}")
    print(f"⭐ Rating: {doctor['rating']}/5.0")

    # 6. CHECK INSURANCE COVERAGE
    insurance_result = check_insurance_coverage(detected_specialty)
    print(f"💰 Insurance Status: {insurance_result['status']} ({insurance_result['plan']})")
    print(f"💵 Patient Copay: {insurance_result['copay']}")

    # 7. GET RELEVANT MEDICAL CODES with robust fallbacks
    procedure_codes = get_procedure_codes(detected_specialty)
    diagnosis_codes = get_diagnosis_codes(detected_specialty)
    
    # Debug: Print what codes we retrieved
    print(f"🔬 Procedure Codes Retrieved: {len(procedure_codes) if procedure_codes else 0} codes")
    print(f"🧬 Diagnosis Codes Retrieved: {len(diagnosis_codes) if diagnosis_codes else 0} codes")
    
    # 8. GENERATE COMPREHENSIVE PDF REFERRAL FORM (BINARY OUTPUT)
    pdf_binary, pdf_filename = create_referral_pdf(
        patient_name=patient_name,
        doctor=doctor,
        insurance_result=insurance_result,
        clinical_context=clinical_context,
        procedure_codes=procedure_codes,
        diagnosis_codes=diagnosis_codes,
        specialty=detected_specialty,
        patient_dob=patient_dob,
        patient_age=patient_age,
        patient_sex=patient_sex,
        patient_complaint=patient_complaint
    )
    
    # Check if PDF generation was successful
    if not pdf_binary or not pdf_filename:
        print("❌ PDF generation failed - continuing without PDF attachment")
        pdf_binary = None
        pdf_filename = None
    
    # 9. GENERATE PROFESSIONAL HTML EMAIL
    email_html = generate_referral_email_html(
        patient_name=patient_name,
        doctor=doctor,
        insurance_result=insurance_result,
        clinical_context=clinical_context,
        procedure_codes=procedure_codes,
        diagnosis_codes=diagnosis_codes,
        specialty=detected_specialty,
        pdf_filename=pdf_filename,
        patient_dob=patient_dob,
        patient_age=patient_age,
        patient_sex=patient_sex,
        patient_complaint=patient_complaint
    )
    
    # 10. SAVE PDF TO DISK TEMPORARILY FOR MULTIPART FILE UPLOAD
    temp_pdf_path = None
    permanent_pdf_path = None
    if pdf_binary and pdf_filename:
        try:
            temp_pdf_path = pdf_filename
            # Also save a permanent copy for viewing
            permanent_pdf_path = f"preview_{pdf_filename}"
            
            with open(temp_pdf_path, 'wb') as f:
                f.write(pdf_binary)
            with open(permanent_pdf_path, 'wb') as f:
                f.write(pdf_binary)
                
            print(f"💾 Temporary PDF saved: {temp_pdf_path} ({len(pdf_binary)} bytes)")
            print(f"🔍 Preview PDF saved: {permanent_pdf_path}")
            
            # Auto-open the PDF for preview (macOS) - ALWAYS ENABLED
            try:
                subprocess.run(['open', permanent_pdf_path], check=False)
                print(f"👀 PDF automatically opened: {permanent_pdf_path}")
                print(f"📄 Preview should appear in your default PDF viewer")
            except Exception as e:
                print(f"⚠️ Could not auto-open PDF: {e}")
                print(f"💡 Manually open with: open {permanent_pdf_path}")
                # Try alternative methods
                try:
                    import webbrowser
                    webbrowser.open(f'file://{os.path.abspath(permanent_pdf_path)}')
                    print(f"🌐 Opened PDF in browser as fallback")
                except Exception as e2:
                    print(f"⚠️ Browser fallback failed: {e2}")
                
        except Exception as e:
            print(f"❌ Failed to save temporary PDF: {e}")
            temp_pdf_path = None
    
    # 11. SEND TO N8N WEBHOOK WITH MULTIPART FILE UPLOAD
    return send_to_n8n_with_file(
        email="inumakisalt123@gmail.com",
        subject=f"Urgent Referral: {patient_name} - {detected_specialty.title()} Consultation",
        email_html=email_html,
        pdf_file_path=temp_pdf_path,
        pdf_filename=pdf_filename,
        patient_name=patient_name  # Pass patient name explicitly
    )

def extract_patient_name(text):
    """Extract patient name from transcript using regex patterns"""
    # Pattern 1: "refer [Name]" or "send [Name]"
    pattern1 = r"(?:refer|send)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+to"
    match1 = re.search(pattern1, text, re.IGNORECASE)
    
    # Pattern 2: "Patient is [Name]"
    pattern2 = r"patient\s+is\s+([A-Za-z\s]+?)(?:\.|,|\s+is|\s+has)"
    match2 = re.search(pattern2, text, re.IGNORECASE)
    
    # Pattern 3: "[Name] is a" or "[Name] has been"
    pattern3 = r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:is\s+a|has\s+been|reports)"
    match3 = re.search(pattern3, text)
    
    # Pattern 4: Direct name mention with context
    pattern4 = r"([A-Z][a-z]+\s+[A-Z][a-z]+)"
    match4 = re.search(pattern4, text)
    
    if match1:
        return match1.group(1).strip()
    elif match2:
        return match2.group(1).strip().title()
    elif match3:
        name = match3.group(1).strip()
        # Avoid common words that aren't names
        if name.lower() not in ['okay', 'well', 'so', 'the', 'this', 'please', 'refer', 'patient']:
            return name
    elif match4:  
        name = match4.group(1).strip()
        # Check if it looks like a real name (First Last format)
        if len(name.split()) == 2 and all(word.istitle() for word in name.split()):
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

def generate_referral_email_html(patient_name, doctor, insurance_result, clinical_context, procedure_codes, diagnosis_codes, specialty, pdf_filename=None, patient_dob=None, patient_age=None, patient_sex=None, patient_complaint=None):
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
                        <span class="label">Date of Birth:</span> {patient_dob or 'Not provided'}
                    </div>
                    <div class="info-item">
                        <span class="label">Insurance Plan:</span> {insurance_result['plan']}
                    </div>
                </div>
                <div>
                    <div class="info-item">
                        <span class="label">Age:</span> {patient_age or 'Not provided'}
                    </div>
                    <div class="info-item">
                        <span class="label">Sex:</span> {patient_sex or 'Not provided'}
                    </div>
                    <div class="info-item">
                        <span class="label">Network Status:</span> 
                        <span class="network-status">{insurance_result['status']}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Patient Copay:</span> {insurance_result['copay']}
                    </div>
                </div>
            </div>
            
            {f'<div class="info-item" style="margin-top: 15px;"><span class="label">Chief Complaint:</span> <strong>{patient_complaint}</strong></div>' if patient_complaint else ''}
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

def send_to_n8n_with_file(email, subject, email_html, pdf_file_path=None, pdf_filename=None, patient_name=None):
    """Send email with PDF file attachment using multipart/form-data - CRITICAL FIX"""
    # AI-generated code section begins - GitHub Copilot assisted with multipart file upload fix
    
    print(f"🚀 Sending referral email to n8n workflow with file attachment...")
    print(f"📧 Email Details:")
    print(f"   Recipient: {email}")
    print(f"   Subject: {subject}")
    print(f"   HTML Length: {len(email_html)} characters")
    print(f"   PDF File: {pdf_file_path}")
    
    try:
        # Prepare the data payload (non-file fields) - n8n compatible format
        data = {
            "email": email,
            "subject": subject,
            "email_html": email_html,
            "patient_name": patient_name or "Unknown Patient",
            "content_type": "medical_referral"
        }
        
        files = {}
        
        # Add PDF file if available
        if pdf_file_path and pdf_filename:
            try:
                # Open the PDF file for multipart upload
                with open(pdf_file_path, 'rb') as pdf_file:
                    # Read file content
                    pdf_content = pdf_file.read()
                    
                # Add file to files dict (n8n expects 'file' parameter)
                files['file'] = (pdf_filename, pdf_content, 'application/pdf')
                print(f"📎 PDF file attached: {pdf_filename} ({len(pdf_content)} bytes)")
                
            except Exception as e:
                print(f"❌ Failed to read PDF file: {e}")
                files = {}
        
        # Send multipart request with both data and files
        print(f"🌐 Sending POST request to n8n...")
        print(f"📤 Data fields being sent: {list(data.keys())}")
        print(f"📎 File fields being sent: {list(files.keys())}")
        
        response = requests.post(
            N8N_WEBHOOK_URL, 
            data=data,  # Form data fields (accessible as $json.body.email, $json.body.subject, etc.)
            files=files,  # File attachment (accessible as $binary.file)
            timeout=15
        )
        
        # Clean up temporary file
        if pdf_file_path:
            try:
                os.remove(pdf_file_path)
                print(f"🗑️ Temporary PDF file deleted: {pdf_file_path}")
            except Exception as e:
                print(f"⚠️ Warning: Could not delete temporary file: {e}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Referral email with PDF attachment sent to n8n!")
            print("📧 Email notification should arrive shortly")
            return True
        else:
            print(f"❌ n8n Webhook Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
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
# AI-generated code section ends

# ==========================================
# TEST RUNNER - Single Test Mode (No Email Spam) - REMOVED
# ==========================================
    print("   - 'Sarah needs dermatology for her rash'")
    print("   - 'Patient has headaches, refer to neurology'") 
    print("   - 'The weather is nice today' (should fail)")
    
# AI-generated code section ends

# AI-generated code section begins - GitHub Copilot assisted with patient data extraction functions

def extract_patient_dob(text):
    """Extract patient date of birth from transcript"""
    # Pattern 1: "DOB is MM/DD/YYYY" or "date of birth MM/DD/YYYY"
    pattern1 = r"(?:dob|date of birth)(?:\s+is)?\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"
    match1 = re.search(pattern1, text, re.IGNORECASE)
    
    # Pattern 2: "born on MM/DD/YYYY" or "born MM/DD/YYYY"
    pattern2 = r"born(?:\s+on)?\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"
    match2 = re.search(pattern2, text, re.IGNORECASE)
    
    # Pattern 3: Standalone date pattern
    pattern3 = r"\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b"
    match3 = re.search(pattern3, text)
    
    if match1:
        return match1.group(1)
    elif match2:
        return match2.group(1)
    elif match3:
        # Only use standalone date if context suggests it's DOB
        if any(word in text.lower() for word in ['birth', 'age', 'old', 'years']):
            return match3.group(1)
    
    return None

def extract_patient_age(text):
    """Extract patient age from transcript"""
    # Pattern 1: "XX year old" or "XX years old"
    pattern1 = r"(?:is\s+a\s+)?(\d{1,3})\s+years?\s+old"
    match1 = re.search(pattern1, text, re.IGNORECASE)
    
    # Pattern 2: "age is XX" or "age XX"
    pattern2 = r"age(?:\s+is)?\s+(\d{1,3})"
    match2 = re.search(pattern2, text, re.IGNORECASE)
    
    # Pattern 3: "XXyo" (year old abbreviation)
    pattern3 = r"(\d{1,3})\s*yo\b"
    match3 = re.search(pattern3, text, re.IGNORECASE)
    
    if match1:
        age = int(match1.group(1))
        if 0 <= age <= 120:  # Reasonable age range
            return str(age)
    elif match2:
        age = int(match2.group(1))
        if 0 <= age <= 120:
            return str(age)
    elif match3:
        age = int(match3.group(1))
        if 0 <= age <= 120:
            return str(age)
    
    return None

def extract_patient_sex(text):
    """Extract patient sex/gender from transcript"""
    text_lower = text.lower()
    
    # Look for explicit mentions
    male_indicators = ['male', 'he is', 'his', 'him', 'man', 'gentleman', 'mr.']
    female_indicators = ['female', 'she is', 'her', 'woman', 'lady', 'ms.', 'mrs.']
    
    male_count = sum(1 for indicator in male_indicators if indicator in text_lower)
    female_count = sum(1 for indicator in female_indicators if indicator in text_lower)
    
    if male_count > female_count and male_count > 0:
        return "Male"
    elif female_count > male_count and female_count > 0:
        return "Female"
    
    # Look for specific patterns
    if re.search(r'\bgender\s+(?:is\s+)?(?:male|m)\b', text_lower):
        return "Male"
    elif re.search(r'\bgender\s+(?:is\s+)?(?:female|f)\b', text_lower):
        return "Female"
    elif re.search(r'\bsex\s+(?:is\s+)?(?:male|m)\b', text_lower):
        return "Male"
    elif re.search(r'\bsex\s+(?:is\s+)?(?:female|f)\b', text_lower):
        return "Female"
    
    return None

def extract_patient_complaint(text):
    """Extract patient's main complaint from transcript"""
    # Enhanced complaint extraction patterns
    complaint_patterns = [
        r'complaining\s+(?:of\s+)?([^.!?]+)',
        r'chief\s+complaint\s+(?:is\s+)?([^.!?]+)',
        r'presenting\s+with\s+([^.!?]+)',
        r'has\s+been\s+experiencing\s+([^.!?]+)',
        r'reports\s+([^.!?]+)',
        r'suffering\s+from\s+([^.!?]+)',
        r'problem\s+(?:is\s+)?([^.!?]+)',
        r'concern\s+(?:is\s+)?([^.!?]+)'
    ]
    
    for pattern in complaint_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            complaint = match.group(1).strip()
            # Clean up the complaint text
            if len(complaint) > 10 and len(complaint) < 200:
                return complaint
    
    # Fallback to symptom keywords
    symptom_keywords = [
        'pain', 'swelling', 'headache', 'chest pain', 'shortness of breath',
        'rash', 'lesion', 'joint pain', 'back pain', 'dizziness',
        'nausea', 'fever', 'fatigue', 'anxiety', 'depression'
    ]
    
    text_lower = text.lower()
    found_symptoms = []
    for symptom in symptom_keywords:
        if symptom in text_lower:
            found_symptoms.append(symptom)
    
    if found_symptoms:
        return ", ".join(found_symptoms[:3])  # Return up to 3 symptoms
    
    return None

# AI-generated code section ends

# AI-generated code section ends

# ==========================================
# TEST RUNNER - Single Test Mode (No Email Spam) - REMOVED
# ==========================================
    print("   - 'Sarah needs dermatology for her rash'")
    print("   - 'Patient has headaches, refer to neurology'") 
    print("   - 'The weather is nice today' (should fail)")
    
# AI-generated code section ends

# AI-generated code section begins - GitHub Copilot assisted with PDF preview functionality

def test_with_pdf_preview():
    """Interactive test that shows the PDF and lets user customize the test"""
    print("🧪 INTERACTIVE PDF PREVIEW TEST")
    print("=" * 50)
    
    # Ask user for custom input or use default
    print("\n📝 Choose your test:")
    print("1. Default cardiology referral (John Smith)")
    print("2. Custom transcript input")
    
    choice = input("Enter choice (1 or 2, default=1): ").strip() or "1"
    
    if choice == "2":
        print("\n📋 Enter your medical transcript:")
        custom_transcript = input("Transcript: ").strip()
        if not custom_transcript:
            print("⚠️ Empty transcript, using default...")
            custom_transcript = None
    else:
        custom_transcript = None
    
    # Use default or custom transcript
    if custom_transcript:
        test_transcript = custom_transcript
    else:
        test_transcript = """
        I need to refer John Smith to cardiology. He is a 48 year old male, date of birth is 03/15/1975. 
        He has been complaining of chest pain with exertion and shortness of breath. 
        The patient reports these episodes occur during physical activity and resolve with rest. 
        He also mentions palpitations and some dizziness. 
        No radiation of pain to arms or jaw, but increased frequency over the past 2 weeks.
        """
    
    print(f"\n🚀 Processing transcript...")
    result = analyze_transcript(test_transcript)
    
    print(f"\n{'✅ SUCCESS' if result else '❌ FAILED'}")
    
    # Show available PDFs
    preview_pdfs = glob.glob("preview_medical_referral_*.pdf")
    if preview_pdfs:
        latest_pdf = max(preview_pdfs, key=os.path.getctime)
        print(f"📄 Latest PDF: {latest_pdf}")
        
        # Ask if user wants to open it again
        reopen = input("\n🔄 Open PDF again? (y/n, default=n): ").strip().lower()
        if reopen == 'y':
            try:
                subprocess.run(['open', latest_pdf], check=False)
                print(f"👀 PDF reopened: {latest_pdf}")
            except Exception as e:
                print(f"❌ Could not reopen PDF: {e}")
    
    return result

# AI-generated code section ends

# ==========================================
# QUICK CUSTOM TEST FUNCTION
# ==========================================

def quick_custom_test(custom_transcript):
    """Run a quick test with custom transcript and auto PDF preview"""
    print("🚀 PROCESSING CUSTOM TRANSCRIPT")
    print("=" * 50)
    print(f"📝 Transcript: {custom_transcript[:100]}...")
    
    result = analyze_transcript(custom_transcript)
    
    print("\n" + "=" * 50)
    print(f"🎯 RESULT: {'✅ SUCCESS' if result else '❌ FAILED'}")
    print("📧 Email sent! 📄 PDF opened!")
    
    return result

# ==========================================
# MAIN EXECUTION - Run router.py directly
# ==========================================

if __name__ == "__main__":
    print("🚀 MEDICAL REFERRAL SYSTEM - AUTO PDF PREVIEW")
    print("=" * 50)
    
    # Default behavior: Auto PDF preview + Email
    sample_transcript = """
    I need to refer John Smith to cardiology. He is a 48 year old male, date of birth is 03/15/1975. 
    He has been complaining of chest pain with exertion and shortness of breath. 
    The patient reports these episodes occur during physical activity and resolve with rest. 
    He also mentions palpitations and some dizziness. 
    No radiation of pain to arms or jaw, but increased frequency over the past 2 weeks.
    """
    
    print("📝 Processing medical referral with auto PDF preview...")
    print(f"📋 Patient: John Smith (Cardiology)")
    
    result = analyze_transcript(sample_transcript)
    
    print("\n" + "=" * 50)
    print(f"🎯 EXECUTION RESULT: {'✅ SUCCESS' if result else '❌ FAILED'}")
    print("📧 Email sent with PDF attachment!")
    print("📄 PDF automatically opened for preview!")
    print("🎉 System ready for next referral!")

# AI-generated code section ends


