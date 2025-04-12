import os
import sys
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

        auth_header = request.headers.get("Authorization", "")
        api_key = auth_header.replace("Bearer ", "").strip()

        # Optional: Validate
        if not api_key.startswith("sk-"):
            return jsonify({"error": "Invalid or missing API key"}), 401

        # Set API key for OpenAI client
        resume_skill_matcher.set_api_key(api_key)
        deep_tailor.set_api_key(api_key)

        # Format json data before passing in to gpt
        # data: containing "resume_data" and "job_description" fields
        formatted_json = FormattingJSON(data)

        # Step trivial: Extracting job description and resume data
        resume_data = formatted_json.get_resume_data()
        profile_data = formatted_json.get_profile_data()
        job_description = formatted_json.get_job_description()
        university_data = formatted_json.get_university_data()

        # Step trivial: Extract data that we want to pass to gpt (be tailored later)
        no_need_tailor_fn = formatted_json.extract_fields_need_tailoring()
        jobs_no_need_tailor = no_need_tailor_fn("jobs")
        projects_no_need_tailor = no_need_tailor_fn("projects")

        # print(jobs_no_need_tailor, flush=True)
        # print(projects_no_need_tailor, flush=True)

        ## [Debugging Purpose] START HERE
        # Step 1: Augmenting the technical skills in the resume
        # [Note 2.0]: GPT is being used HERE
        formatted_augment_skills = formatted_json.format_augment_skill()
        augmented_skills_json = resume_skill_matcher.match_skills(
            formatted_augment_skills, job_description
        )

        # Step 2: Updating the technical skills in resume:
        # [Note 1.1]: Although we don't tailor the bullet point, we still want to augment the skills
        formatted_json.augment_skill_to_input_json(augmented_skills_json)

        # Step 3: Formatting the resume data for deep tailoring
        formatted_json.format_resume_data()
        data = formatted_json.get_formatted_json()

        # [Note 2.1]: GPT is being used HERE
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

        ## END HERE

        # [Testing Purpose - Sample Tailored Output from GPT]
        # tailored_resume = {
        #     "personal_projects": [
        #         {
        #             "title": "CloudCueAI",
        #             "description": [
        #                 "Engineered a serverless application using AWS Lambda and API Gateway to develop a real-time interview tool, attracting 500-1000 daily visits.",
        #                 "Implemented infrastructure automation with Terraform and AWS SAM, improving deployment speed and reliability by 30%.",
        #                 "Developed comprehensive monitoring and observability using CloudWatch, ensuring system uptime and performance for 20,000 data entries.",
        #                 "Enhanced authentication with IAM and JWT, strengthening security and compliance.",
        #             ],
        #         },
        #         {
        #             "title": "Beatcode",
        #             "description": [
        #                 "Developed WebSocket APIs using FastAPI for real-time coding battles, supporting 1,000+ concurrent users.",
        #                 "Managed PostgreSQL databases to reliably store player data and performance metrics for 500+ players during beta.",
        #                 "Established a robust CI/CD pipeline using Docker and GitHub Actions, accelerating deployment processes by 40%.",
        #                 "Implemented OAuth and CORS for seamless user authentication, enhancing system security and user access.",
        #             ],
        #         },
        #     ],
        #     "work_experiences": [
        #         {
        #             "title": "FPT Software",
        #             "description": [
        #                 "Led an AngularJS-TypeScript website for managing prescriptions, serving Japan Pharmacists Association with 500-1000 daily visits.",
        #                 "Refined an Observer pattern to automate 20,000 data bindings, increasing efficiency and code accuracy by 50%.",
        #                 "Enhanced collaborative development using Agile-Scrum, improving team productivity and communication in a fast-paced environment.",
        #                 "Integrated JavaScript SDK across multiple web pages and modals, ensuring seamless interaction with frontend UI.",
        #             ],
        #         },
        #         {
        #             "title": "Avocademy (YC W22)",
        #             "description": [
        #                 "Leveraged OpenAI API to engineer a job classification system, boosting job relevance by 50%.",
        #                 "Streamlined the extraction of 750+ daily job postings and automated applications using Fire Crawler, PuppeteerJS, and Playwright.",
        #                 "Managed 70,000+ database entries to efficiently monitor job posting, user data, and platform activity using MongoDB and Supabase.",
        #                 "Automated deployments and enhanced system reliability with Vercel, GitHub CI/CD, and A/B testing.",
        #                 "Developed secure cloud interactions by integrating OAuth and IAM policies, improving security compliance by 40%.",
        #             ],
        #         },
        #         {
        #             "title": "Viettel AI",
        #             "description": [
        #                 "Pioneered a semantic search pipeline with Solr and SBERT, enhancing text search relevance by 25%.",
        #                 "Implemented data storage and retrieval systems using Microsoft Graph RAG, optimizing data access and management.",
        #             ],
        #         },
        #     ],
        # }
        # [End Testing Purpose]

        print(tailored_resume, flush=True)

        # "augmented_skill_data_raw" is just like "data", but will skills got augmented
        augmented_skills_data_raw = formatted_json.get_augmented_skill_input_json()

        print("till this point", flush=True)
        # Process tailored resume using Resume Tailor
        tailor = LatexResumeBuilder(TEMPLATE_JSON)

        ## Testing purpose
        # print("FROM HERE", flush=True)
        # print("tailored_resume", tailored_resume, flush=True)
        # print("profile_data", profile_data, flush=True)
        # print("resume_data", resume_data, flush=True)
        # print("university_data", university_data, flush=True)
        # print("augmented_skills_data_raw", augmented_skills_data_raw, flush=True)
        # print("jobs_no_need_tailor", jobs_no_need_tailor, flush=True)
        # print("projects_no_need_tailor", projects_no_need_tailor, flush=True)
        # print("TO HERE", flush=True)

        tailor.update_template(
            tailored_resume,
            profile_data,
            resume_data,
            university_data,
            skill_augmented_resume_data=augmented_skills_data_raw,
            untailored_jobs=jobs_no_need_tailor,
            untailored_projects=projects_no_need_tailor,
        )  # TODO: We are about to pass two ugly looking data. Please fix it

        tailor.generate_latex(LATEX_TEMPLATE, OUTPUT_LATEX)

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
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Optional: Confirm pdflatex is in path
        result = subprocess.run(
            ["which", "pdflatex"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"pdflatex Path: {result.stdout.decode().strip()}")

        # Try to compile LaTeX
        compile_result = subprocess.run(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-output-directory",
                output_dir,
                latex_file,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if compile_result.returncode != 0:
            print("LaTeX compilation failed:")
            print(compile_result.stdout.decode())
            print(compile_result.stderr.decode())
        else:
            print("PDF generated successfully!")

    except FileNotFoundError:
        print("pdflatex not found in the container.")
    except subprocess.CalledProcessError as e:
        print("LaTeX command error:")
        print(e.stderr.decode())


if __name__ == "__main__":
    try:
        # app.run(port=5050, debug=True, use_reloader=True)
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("Backend stopped...")

        # Sample data to avoid gpt call
        tailored_resume = {
            "personal_projects": [
                {
                    "title": "CloudCueAI",
                    "description": [
                        "Engineered a serverless application using AWS Lambda and API Gateway to develop a real-time interview tool, attracting 500-1000 daily visits.",
                        "Implemented infrastructure automation with Terraform and AWS SAM, improving deployment speed and reliability by 30%.",
                        "Developed comprehensive monitoring and observability using CloudWatch, ensuring system uptime and performance for 20,000 data entries.",
                        "Enhanced authentication with IAM and JWT, strengthening security and compliance.",
                    ],
                },
                {
                    "title": "Beatcode",
                    "description": [
                        "Developed WebSocket APIs using FastAPI for real-time coding battles, supporting 1,000+ concurrent users.",
                        "Managed PostgreSQL databases to reliably store player data and performance metrics for 500+ players during beta.",
                        "Established a robust CI/CD pipeline using Docker and GitHub Actions, accelerating deployment processes by 40%.",
                        "Implemented OAuth and CORS for seamless user authentication, enhancing system security and user access.",
                    ],
                },
            ],
            "work_experiences": [
                {
                    "title": "FPT Software",
                    "description": [
                        "Led an AngularJS-TypeScript website for managing prescriptions, serving Japan Pharmacists Association with 500-1000 daily visits.",
                        "Refined an Observer pattern to automate 20,000 data bindings, increasing efficiency and code accuracy by 50%.",
                        "Enhanced collaborative development using Agile-Scrum, improving team productivity and communication in a fast-paced environment.",
                        "Integrated JavaScript SDK across multiple web pages and modals, ensuring seamless interaction with frontend UI.",
                    ],
                },
                {
                    "title": "Avocademy (YC W22)",
                    "description": [
                        "Leveraged OpenAI API to engineer a job classification system, boosting job relevance by 50%.",
                        "Streamlined the extraction of 750+ daily job postings and automated applications using Fire Crawler, PuppeteerJS, and Playwright.",
                        "Managed 70,000+ database entries to efficiently monitor job posting, user data, and platform activity using MongoDB and Supabase.",
                        "Automated deployments and enhanced system reliability with Vercel, GitHub CI/CD, and A/B testing.",
                        "Developed secure cloud interactions by integrating OAuth and IAM policies, improving security compliance by 40%.",
                    ],
                },
                {
                    "title": "Viettel AI",
                    "description": [
                        "Pioneered a semantic search pipeline with Solr and SBERT, enhancing text search relevance by 25%.",
                        "Implemented data storage and retrieval systems using Microsoft Graph RAG, optimizing data access and management.",
                    ],
                },
            ],
        }
