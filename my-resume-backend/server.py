import re
import sys
import json
import signal
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # Allow frontend to call the backend


def shutdown_server(signal, frame):
    print("Shutting down server...")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_server)
signal.signal(signal.SIGTERM, shutdown_server)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask backend is running!"})


@app.route("/tailor-resume", methods=["POST"])
def tailor_resume():
    try:
        # Get JSON data from frontend
        data = request.get_json()
        json_data = json.dumps(data)

        # Run script.py with JSON data as input
        result = subprocess.run(
            ["python", "deep_tailoring.py"],
            input=json_data,
            text=True,
            capture_output=True,
        )

        # Extract JSON response
        output_text = result.stdout.strip()
        tailored_resume = extract_json(output_text)

        if tailored_resume:
            return jsonify(
                {"message": "Resume tailored successfully!", "data": tailored_resume}
            )
        else:
            return jsonify({"error": "Invalid JSON response from deep_tailoring.py"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def extract_json(text):
    """Extract JSON from OpenAI response"""
    match = re.search(r"```json\s*([\s\S]+?)\s*```", text)
    json_str = match.group(1) if match else text

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


if __name__ == "__main__":
    try:
        app.run(port=5000, debug=True)
    except KeyboardInterrupt:
        print("Backend stopped...")
