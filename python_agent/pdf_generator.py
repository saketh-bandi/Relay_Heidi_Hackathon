# pdf_generator.py
# AI-generated code section begins - GitHub Copilot assisted with robust medical PDF generation

from fpdf import FPDF
from datetime import datetime
import os
import re

def sanitize_text_for_pdf(text):
    """Sanitize text for PDF generation by removing problematic characters"""
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove or replace problematic Unicode characters
    replacements = {
        # Smart quotes
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        # Em dash, en dash
        '\u2014': '-', '\u2013': '-',
        # Other common problematic characters
        '\u2022': '-', '\u2026': '...', '\u00a0': ' ',
        # Remove emojis and other high Unicode characters
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove any remaining non-ASCII characters using regex
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    # Encode to latin-1 and handle errors by replacing problematic characters
    try:
        # First try to encode/decode to catch issues
        text.encode('latin-1')
        return text
    except UnicodeEncodeError:
        # Replace any remaining problematic characters
        return text.encode('latin-1', errors='replace').decode('latin-1')

class MedicalReferralFormPDF(FPDF):
    """Professional Medical Referral Form PDF Generator - Complete Form Layout"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """PDF Header with medical letterhead styling"""
        try:
            # Header background
            self.set_fill_color(20, 50, 120)  # Professional dark blue
            self.rect(0, 0, 210, 30, 'F')
            
            # Header text
            self.set_font('Arial', 'B', 18)
            self.set_text_color(255, 255, 255)  # White text
            self.cell(0, 20, 'MEDICAL REFERRAL FORM', 0, 1, 'C')
            
            # Subtitle
            self.set_font('Arial', '', 10)
            self.cell(0, 8, 'Healthcare Provider Network', 0, 1, 'C')
            self.ln(5)
        except Exception as e:
            print(f"Warning: PDF header generation issue: {e}")
        
    def footer(self):
        """PDF Footer with timestamp and page numbers"""
        try:
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(100, 100, 100)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer_text = sanitize_text_for_pdf(f'Generated: {timestamp} | Page {self.page_no()}')
            self.cell(0, 10, footer_text, 0, 0, 'C')
        except Exception as e:
            print(f"Warning: PDF footer generation issue: {e}")

    def draw_form_box(self, x, y, width, height, label, content, multiline=False):
        """Draw a labeled form box with content"""
        try:
            # Draw box border
            self.set_draw_color(100, 100, 100)
            self.rect(x, y, width, height)
            
            # Label background
            self.set_fill_color(240, 240, 240)
            self.rect(x, y, width, 8, 'F')
            
            # Label text
            self.set_font('Arial', 'B', 8)
            self.set_text_color(0, 0, 0)
            self.set_xy(x + 2, y + 1)
            sanitized_label = sanitize_text_for_pdf(label)
            self.cell(width - 4, 6, sanitized_label, 0, 0, 'L')
            
            # Content
            self.set_font('Arial', '', 10)
            self.set_xy(x + 2, y + 10)
            sanitized_content = sanitize_text_for_pdf(str(content))
            
            if multiline:
                # For multiline content, use a contained multi_cell
                available_width = width - 4
                available_height = height - 12
                # Manually handle text wrapping within the box
                if len(sanitized_content) > 50:
                    lines = []
                    words = sanitized_content.split()
                    current_line = ""
                    
                    for word in words:
                        test_line = current_line + (" " if current_line else "") + word
                        if len(test_line) <= 50:  # Rough character limit per line
                            current_line = test_line
                        else:
                            if current_line:
                                lines.append(current_line)
                            current_line = word
                    
                    if current_line:
                        lines.append(current_line)
                    
                    # Print each line
                    for i, line in enumerate(lines[:3]):  # Max 3 lines
                        self.set_xy(x + 2, y + 10 + (i * 5))
                        self.cell(available_width, 5, line, 0, 0, 'L')
                else:
                    self.cell(available_width, 5, sanitized_content, 0, 0, 'L')
            else:
                # Single line content
                self.cell(width - 4, 5, sanitized_content, 0, 0, 'L')
                
        except Exception as e:
            print(f"Warning: Failed to draw form box '{label}': {e}")

    def draw_large_text_box(self, x, y, width, height, label, content):
        """Draw a large text box for detailed information"""
        try:
            # Draw box border
            self.set_draw_color(100, 100, 100)
            self.rect(x, y, width, height)
            
            # Label background
            self.set_fill_color(240, 240, 240)
            self.rect(x, y, width, 10, 'F')
            
            # Label text
            self.set_font('Arial', 'B', 9)
            self.set_text_color(0, 0, 0)
            self.set_xy(x + 2, y + 2)
            sanitized_label = sanitize_text_for_pdf(label)
            self.cell(width - 4, 6, sanitized_label, 0, 0, 'L')
            
            # Content area
            self.set_font('Arial', '', 9)
            self.set_xy(x + 2, y + 12)
            sanitized_content = sanitize_text_for_pdf(str(content))
            
            # Word wrap for large content
            words = sanitized_content.split()
            lines = []
            current_line = ""
            chars_per_line = int((width - 4) / 2.5)  # Approximate character width
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if len(test_line) <= chars_per_line:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Print lines with proper spacing
            max_lines = int((height - 15) / 4)  # Available height for lines
            for i, line in enumerate(lines[:max_lines]):
                self.set_xy(x + 2, y + 12 + (i * 4))
                self.cell(width - 4, 4, line, 0, 0, 'L')
                
        except Exception as e:
            print(f"Warning: Failed to draw large text box '{label}': {e}")

    def safe_cell(self, w, h, txt='', border=0, ln=0, align='', fill=False):
        """Safe cell method that sanitizes text before adding to PDF"""
        try:
            sanitized_text = sanitize_text_for_pdf(txt)
            self.cell(w, h, sanitized_text, border, ln, align, fill)
        except Exception as e:
            print(f"Warning: Failed to add cell text: {e}")
            self.cell(w, h, '[Text encoding error]', border, ln, align, fill)

    def safe_multi_cell(self, w, h, txt, border=0, align='L', fill=False):
        """Safe multi_cell method that sanitizes text before adding to PDF"""
        try:
            sanitized_text = sanitize_text_for_pdf(txt)
            self.multi_cell(w, h, sanitized_text, border, align, fill)
        except Exception as e:
            print(f"Warning: Failed to add multi-cell text: {e}")
            self.multi_cell(w, h, '[Text encoding error - content unavailable]', border, align, fill)

def create_referral_pdf(patient_name, doctor, insurance_result, clinical_context, 
                       procedure_codes, diagnosis_codes, specialty, 
                       patient_dob=None, patient_age=None, patient_sex=None, patient_complaint=None):
    """
    Generate a professional medical referral form PDF with comprehensive patient information
    """
    # AI-generated code section begins - GitHub Copilot assisted with robust PDF generation
    
    # Create simple timestamp-based filename to avoid filesystem issues
    timestamp = datetime.now().strftime('%H%M%S')
    filename = f"medical_referral_{timestamp}.pdf"
    
    print(f"📄 Generating Medical Referral Form: {filename}")
    
    # Create PDF instance with error handling
    try:
        pdf = MedicalReferralFormPDF()
        pdf.add_page()
        
        # Reset text color for body content
        pdf.set_text_color(0, 0, 0)
    except Exception as e:
        print(f"❌ PDF initialization error: {e}")
        return None
    
    # FORM GENERATION with error handling
    try:
        # DATE AND REFERENCE NUMBER
        current_date = datetime.now().strftime("%m/%d/%Y")
        ref_number = f"REF-{timestamp}"
        
        # Top row with date and reference
        pdf.draw_form_box(10, 45, 90, 20, "DATE OF REFERRAL", current_date)
        pdf.draw_form_box(110, 45, 90, 20, "REFERENCE NUMBER", ref_number)
        
        # PATIENT INFORMATION SECTION (Row 2)
        pdf.draw_form_box(10, 70, 90, 20, "PATIENT NAME", patient_name or "Not Provided")
        pdf.draw_form_box(110, 70, 40, 20, "AGE", patient_age or "Not Provided")
        pdf.draw_form_box(160, 70, 40, 20, "SEX", patient_sex or "Not Provided")
        
        # Row 3 - DOB and additional info
        pdf.draw_form_box(10, 95, 90, 20, "DATE OF BIRTH", patient_dob or "Not Provided")
        pdf.draw_form_box(110, 95, 90, 20, "INSURANCE PLAN", insurance_result.get('plan', 'Unknown'))
        
        # Row 4 - Network status and copay
        network_status = insurance_result.get('status', 'Unknown')
        copay_info = insurance_result.get('copay', 'N/A')
        pdf.draw_form_box(10, 120, 90, 20, "NETWORK STATUS", network_status)
        pdf.draw_form_box(110, 120, 90, 20, "ESTIMATED COPAY", copay_info)
        
        # PROVIDER INFORMATION SECTION
        pdf.draw_form_box(10, 150, 90, 25, "REFERRING TO SPECIALIST", 
                         f"{doctor.get('name', 'Unknown Provider')}")
        pdf.draw_form_box(110, 150, 90, 25, "SPECIALTY", specialty.title())
        
        # Provider details
        pdf.draw_form_box(10, 180, 60, 20, "NPI NUMBER", doctor.get('npi', 'N/A'))
        pdf.draw_form_box(80, 180, 120, 20, "CLINIC/PRACTICE", doctor.get('clinic', 'Unknown Clinic'))
        
        # CLINICAL INFORMATION SECTION
        # Major complaint
        major_complaint = patient_complaint or clinical_context or "General consultation requested"
        pdf.draw_large_text_box(10, 210, 190, 25, "MAJOR COMPLAINT / PRESENTING SYMPTOMS", major_complaint)
        
        # Clinical context/history
        pdf.draw_large_text_box(10, 240, 190, 30, "CLINICAL CONTEXT / HISTORY", clinical_context or "See complaint section above")
        
        # MEDICAL CODING SECTION
        # Procedure codes
        if procedure_codes and len(procedure_codes) > 0:
            proc_text = ""
            for i, proc in enumerate(procedure_codes[:3]):
                if isinstance(proc, dict) and 'code' in proc:
                    proc_text += f"{proc['code']} - {proc.get('description', 'N/A')} "
                    if i < 2 and i < len(procedure_codes) - 1:
                        proc_text += "; "
        else:
            proc_text = "To be determined during consultation"
        
        pdf.draw_large_text_box(10, 275, 190, 20, "ANTICIPATED CPT CODES", proc_text)
        
        # Diagnosis codes
        if diagnosis_codes and len(diagnosis_codes) > 0:
            diag_text = ""
            for i, diag in enumerate(diagnosis_codes[:3]):
                if isinstance(diag, dict) and 'code' in diag:
                    diag_text += f"{diag['code']} - {diag.get('description', 'N/A')} "
                    if i < 2 and i < len(diagnosis_codes) - 1:
                        diag_text += "; "
        else:
            diag_text = "To be determined after specialist evaluation"
        
        pdf.draw_large_text_box(10, 300, 190, 20, "POTENTIAL ICD-10 CODES", diag_text)
        
        # AUTHORIZATION SECTION
        pdf.draw_form_box(10, 325, 60, 20, "URGENCY LEVEL", "Routine")
        pdf.draw_form_box(80, 325, 60, 20, "AUTHORIZATION", "Pending")
        pdf.draw_form_box(150, 325, 50, 20, "FOLLOW-UP", "Required")
        
    except Exception as e:
        print(f"❌ Error generating form content: {e}")
        # Add fallback content
        pdf.set_font('Arial', '', 12)
        pdf.set_xy(10, 50)
        pdf.safe_cell(0, 10, "Error: Unable to generate form content properly", 0, 1, 'L')
    # FOOTER SIGNATURE SECTION
    try:
        # Add signature area at bottom
        pdf.set_xy(10, 350)
        pdf.set_font('Arial', 'B', 10)
        pdf.safe_cell(0, 8, 'AUTHORIZATION & SIGNATURES', 0, 1, 'L')
        
        # Signature boxes
        pdf.draw_form_box(10, 360, 90, 20, "REFERRING PROVIDER SIGNATURE", "Auto-Generated System")
        pdf.draw_form_box(110, 360, 90, 20, "DATE SIGNED", current_date)
        
        # System info
        pdf.set_xy(10, 385)
        pdf.set_font('Arial', '', 8)
        pdf.safe_cell(0, 5, 'This referral was automatically generated by Healthcare AI Referral System', 0, 1, 'L')
        pdf.safe_cell(0, 5, 'Requires physician review and authorization before processing', 0, 1, 'L')
        
    except Exception as e:
        print(f"❌ Error in signature section: {e}")
    
    # Save PDF with comprehensive error handling
    try:
        print(f"📄 Attempting to save PDF: {filename}")
        pdf.output(filename)
        
        # Verify file was created successfully
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            if file_size > 0:
                print(f"✅ PDF Generated Successfully: {filename} ({file_size} bytes)")
                return filename
            else:
                print(f"❌ PDF file created but is empty: {filename}")
                return None
        else:
            print(f"❌ PDF file was not created: {filename}")
            return None
            
    except UnicodeEncodeError as e:
        print(f"❌ PDF Unicode Encoding Error: {e}")
        print("   This is likely due to special characters in the text content")
        return None
    except PermissionError as e:
        print(f"❌ PDF Permission Error: {e}")
        print("   Check if the file is open in another application")
        return None
    except Exception as e:
        print(f"❌ PDF Generation Error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return None
    
    # AI-generated code section ends

def test_pdf_generation():
    """Test function for PDF generation with comprehensive patient data"""
    # AI-generated code section begins - GitHub Copilot assisted with comprehensive test data
    sample_doctor = {
        'name': 'Dr. Emily Chen',
        'npi': '1457389201',
        'clinic': 'Mercy Heart Institute',
        'address': '1234 Medical Plaza Dr, San Francisco, CA 94115'
    }
    
    sample_insurance = {
        'plan': 'Blue Cross Blue Shield PPO',
        'status': 'IN-NETWORK',
        'copay': '$25.00'
    }
    
    sample_procedures = [
        {'code': '99244', 'description': 'Office consultation for cardiac evaluation', 'cost': '$450'},
        {'code': '93000', 'description': 'Electrocardiogram (ECG/EKG)', 'cost': '$150'}
    ]
    
    sample_diagnoses = [
        {'code': 'I25.10', 'description': 'Atherosclerotic heart disease'},
        {'code': 'I20.9', 'description': 'Angina pectoris, unspecified'}
    ]
    
    filename = create_referral_pdf(
        patient_name="John Smith",
        doctor=sample_doctor,
        insurance_result=sample_insurance,
        clinical_context="Patient presenting with chest pain and shortness of breath. Episodes occur with exertion and resolve with rest. No radiation to arms or jaw. Patient reports increased frequency over past 2 weeks.",
        procedure_codes=sample_procedures,
        diagnosis_codes=sample_diagnoses,
        specialty="cardiology",
        patient_dob="03/15/1975",
        patient_age="48",
        patient_sex="Male",
        patient_complaint="Chest pain with exertion, shortness of breath, palpitations"
    )
    
    return filename
    # AI-generated code section ends

if __name__ == "__main__":
    print("🧪 Testing PDF Generation...")
    test_filename = test_pdf_generation()
    if test_filename:
        print(f"✅ Test PDF created: {test_filename}")
    else:
        print("❌ PDF generation failed")

# AI-generated code section ends
