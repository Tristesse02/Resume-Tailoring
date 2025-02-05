import os
import re
import sys
import json
import signal
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file

print("Debugging prints will now appear instantly!", flush=True)
sys.stdout.reconfigure(line_buffering=True)

# Import ResumeTailor class
from handle_data_gpt import ResumeTailor

app = Flask(__name__)
CORS(app)  # Allow frontend to call the backend

TEMPLATE_JSON = "temp_personal_info.json"
LATEX_TEMPLATE = "templateResume.j2"
OUTPUT_LATEX = "output/output.tex"
OUTPUT_PDF = "output/output.pdf"


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

        if not tailored_resume:
            return (
                jsonify({"error": "Invalid JSON response from deep_tailoring.py", "data": output_text}),
                500,
            )

        print("you got to this point lol?", flush=True)
        # Process tailored resume using Resume Tailor
        tailor = ResumeTailor(TEMPLATE_JSON)
        tailor.update_template(tailored_resume)

        tailor.generate_latex(LATEX_TEMPLATE, OUTPUT_LATEX)

        print("till this point", flush=True)
        compile_latex_to_pdf(OUTPUT_LATEX, OUTPUT_PDF)

        return jsonify(
            {"message": "PDF generated successfully!", "data": tailored_resume}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download-pdf", methods=["GET"])
def download_pdf():
    """Send the generated PDF to frontend."""
    if os.path.exists(OUTPUT_PDF):
        return send_file(OUTPUT_PDF, as_attachment=True)
    return jsonify({"error": "PDF file not found"}), 404


def compile_latex_to_pdf(latex_file, output_pdf):
    """Compiles the LaTeX file into a PDF using `pdflatex`."""
    output_dir = os.path.dirname(output_pdf)
    try:
        result = subprocess.run(
            ["where", "pdflatex"],  # This will print the pdflatex path
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"pdflatex Path: {result.stdout.decode().strip()}")  # Debugging output

        subprocess.run(
            ["pdflatex", "-output-directory", output_dir, latex_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("PDF generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error in LaTeX compilation: {e.stderr.decode()}")


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
        app.run(port=5000, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("Backend stopped...")
