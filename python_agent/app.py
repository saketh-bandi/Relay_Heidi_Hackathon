from flask import Flask, request, jsonify
from flask_cors import CORS
from router import analyze_transcript

app = Flask(__name__)
CORS(app) # Allows the frontend to talk to this backend

@app.route('/process-transcript', methods=['POST'])
def process():
    data = request.json
    transcript_text = data.get('transcript', '')
    
    print(f"\n📥 Received from Frontend: {transcript_text}")

    if not transcript_text:
        return jsonify({"status": "error", "message": "No text sent"}), 400

    # Run the logic from router.py
    result = analyze_transcript(transcript_text)

    if result:
        return jsonify({
            "status": "success", 
            "message": "Referral processed and email sent."
        })
    else:
        return jsonify({
            "status": "ignored", 
            "message": "No actionable medical intent found."
        })

if __name__ == '__main__':
    print("🚀 Intelligence Server running on port 5000")
    app.run(port=5000, debug=True)