import os
import re
import sys
import json
import signal
import subprocess
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file

from formatting_json import FormattingJSON
from deep_tailoring import DeepResumeTailor
from resume_skill_matcher import ResumeSkillMatcher
from latex_resume_builder import LatexResumeBuilder

print("Debugging prints will now appear instantly!", flush=True)
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)
CORS(app)  # Allow frontend to call the backend

OUTPUT_PDF = "output/output.pdf"
OUTPUT_LATEX = "output/output.tex"
LATEX_TEMPLATE = "templateResume.j2"
TEMPLATE_JSON = "temp_personal_info.json"

# Initialize DeepResumeTailor
deep_tailor = DeepResumeTailor()
resume_skill_matcher = ResumeSkillMatcher()


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

        # Validate input data
        if not data:
            return jsonify({"error": "Invalid input data"}), 400

        # Format json data before passing in to gpt
        # data: containing "resume_data" and "job_description" fields
        formatted_json = FormattingJSON(data)

        # Step trivial: Extracting job description and resume data
        job_description = formatted_json.get_job_description()

        # Step 1: Augmenting the technical skills in the resume
        formatted_augment_skills = formatted_json.format_augment_skill()
        augmented_skills_json = resume_skill_matcher.match_skills(
            formatted_augment_skills, job_description
        )

        # Step 2: Updating the technical skills in resume:
        formatted_json.augment_skill_to_input_json(augmented_skills_json)

        # Step 3: Formatting the resume data for deep tailoring
        formatted_json.format_resume_data()
        data = formatted_json.get_formatted_json()

        print("ditconmedzvlon", data, flush=True)
        tailored_resume = deep_tailor.tailor_resume(data)

        if not tailored_resume:
            return (
                jsonify(
                    {
                        "error": "Invalid JSON response from deep_tailoring.py",
                        "data": tailored_resume,
                    }
                ),
                500,
            )

        print("you got to this point lol?", flush=True)
        # print(tailored_resume, flush=True)
        # Process tailored resume using Resume Tailor
        tailor = LatexResumeBuilder(TEMPLATE_JSON)
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
