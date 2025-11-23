from flask import Flask, request, jsonify
from flask_cors import CORS
from router import analyze_transcript
import logging
from datetime import datetime

# AI-generated code section begins - GitHub Copilot assisted with creating comprehensive Flask healthcare API
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/process-transcript', methods=['POST'])
def process_transcript():
    """
    Main endpoint for processing medical transcripts
    Accepts JSON payload with transcript text and returns processing results
    """
    try:
        # Validate request data
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must be JSON",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        data = request.json
        transcript_text = data.get('transcript', '').strip()
        
        # Log incoming request
        logger.info(f"📥 Processing transcript request: '{transcript_text[:100]}...'")
        
        # Validate transcript content
        if not transcript_text:
            return jsonify({
                "status": "error",
                "message": "Transcript text is required",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        if len(transcript_text) < 3:
            return jsonify({
                "status": "error",
                "message": "Transcript text too short",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Process the transcript through the router
        processing_result = analyze_transcript(transcript_text)
        
        # Return appropriate response based on processing result
        if processing_result:
            logger.info("✅ Transcript processing successful")
            return jsonify({
                "status": "success",
                "message": "Medical referral processed successfully",
                "description": "Referral has been routed to the appropriate specialist, PDF generated, and notifications sent",
                "features": {
                    "email_sent": True,
                    "pdf_generated": True,
                    "clinical_analysis": True,
                    "insurance_verified": True
                },
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            logger.info("ℹ️ No medical intent detected in transcript")
            return jsonify({
                "status": "ignored",
                "message": "No actionable medical intent detected",
                "description": "The transcript appears to be casual conversation rather than a medical referral",
                "timestamp": datetime.now().isoformat()
            }), 200
            
    except Exception as e:
        logger.error(f"❌ Error processing transcript: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error during transcript processing",
            "error_details": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring system status
    """
    return jsonify({
        "status": "healthy",
        "service": "Healthcare Transcript Processing API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/info', methods=['GET'])
def api_info():
    """
    API information endpoint showing available specialties and capabilities
    """
    from mock_db import SPECIALIST_REGISTRY, INSURANCE_PLANS
    
    return jsonify({
        "service_name": "Healthcare Referral Processing System",
        "description": "AI-powered medical transcript analysis for automated specialist referrals",
        "capabilities": {
            "patient_name_extraction": "Regex-based name detection from transcript",
            "specialty_detection": "Dynamic specialty matching with synonym support",
            "doctor_matching": "Automated specialist selection with rating optimization",
            "insurance_verification": "Real-time coverage checking and copay calculation",
            "medical_coding": "CPT and ICD-10 code assignment",
            "workflow_integration": "n8n webhook automation for notifications"
        },
        "supported_specialties": list(SPECIALIST_REGISTRY.keys()),
        "supported_insurance": list(INSURANCE_PLANS.keys()),
        "endpoints": {
            "/process-transcript": "POST - Main transcript processing endpoint",
            "/health": "GET - System health check",
            "/api/info": "GET - API information and capabilities"
        },
        "timestamp": datetime.now().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with helpful message"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": ["/process-transcript", "/health", "/api/info"],
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors"""
    return jsonify({
        "status": "error",
        "message": "Method not allowed for this endpoint",
        "timestamp": datetime.now().isoformat()
    }), 405

if __name__ == '__main__':
    print("🏥 Healthcare Transcript Processing API")
    print("=" * 50)
    print("🚀 Server starting on http://localhost:5000")
    print("📋 Available endpoints:")
    print("   POST /process-transcript - Process medical transcripts")
    print("   GET  /health           - Health check")
    print("   GET  /api/info         - API information")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5001,
        debug=True,
        threaded=True  # Handle multiple requests
    )
# AI-generated code section ends