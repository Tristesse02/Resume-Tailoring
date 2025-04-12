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

        ## Start of DEBUGGING FOR RESUME TAILORING

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

        ## End of DEBUGGING FOR RESUME TAILORING

        print("FROM HERE", flush=True)
        print("tailored_resume", tailored_resume, flush=True)
        print("profile_data", profile_data, flush=True)
        print("resume_data", resume_data, flush=True)
        print("university_data", university_data, flush=True)
        print("augmented_skills_data_raw", augmented_skills_data_raw, flush=True)
        print("jobs_no_need_tailor", jobs_no_need_tailor, flush=True)
        print("projects_no_need_tailor", projects_no_need_tailor, flush=True)
        print("TO HERE", flush=True)

        # tailored_resume = {
        #     "work_experiences": [
        #         {
        #             "title": "Avocademy (YC W22)",
        #             "description": [
        #                 "Engineered an automated job application system using React and OpenAI API, processing 750+ daily applications.",
        #                 "Streamlined job data extraction using Fire Crawler, PuppeteerJS, and Playwright, enhancing data processing efficiency.",
        #                 "Managed 70,000+ database entries to efficiently track job postings and user information using MongoDB and Supabase.",
        #                 "Implemented A/B testing and end-to-end testing to optimize system performance, increasing user satisfaction by 25%.",
        #                 "Collaborated on GitHub and deployed with Vercel CI/CD pipelines, reducing deployment time by 30%.",
        #             ],
        #         },
        #         {
        #             "title": "FPT Software",
        #             "description": [
        #                 "Led an AngularJS-TypeScript website for Japan Pharmacists Association, serving 500-1000 daily users.",
        #                 "Refined JavaScript SDK for seamless UI integration across 350+ web pages and modals, improving UX by 40%.",
        #                 "Automated 20,000+ frontend-backend data entries with Observer pattern, enhancing accuracy and reducing coding time.",
        #                 "Managed agile-scrum tasks to improve team collaboration and project delivery speed in a fast-paced environment.",
        #             ],
        #         },
        #         {
        #             "title": "Viettel AI",
        #             "description": [
        #                 "Developed a NLP pipeline using Solr and SBERT for chatbot enhancement, improving search precision by 25%.",
        #                 "Researched and implemented Microsoft Graph RAG for effective data retrieval and storage, boosting query speed by 40%.",
        #             ],
        #         },
        #     ],
        #     "personal_projects": [
        #         {
        #             "title": "CloudCueAI",
        #             "description": [
        #                 "Created a serverless word suggestion tool using AWS Lambda, API Gateway, boosting interview prep speed by 30%.",
        #                 "Automated real-time transcription and storage using AWS Transcribe and S3, improving speech-to-text accuracy by 15%.",
        #                 "Implemented OAuth and JWT for secure user authentication and authorization, enhancing security compliance by 35%.",
        #                 "Leveraged CloudWatch for monitoring system performance and logging, reducing downtime and improving reliability.",
        #             ],
        #         },
        #         {
        #             "title": "Beatcode",
        #             "description": [
        #                 "Developed FastAPI backend with PostgreSQL for scalable player data management, supporting 1000+ concurrent users.",
        #                 "Engineered a Dockerized environment for seamless code submission and execution, improving system efficiency by 20%.",
        #                 "Built OAuth and CORS for secure API interactions, enhancing user login security and cross-domain access control.",
        #                 "Implemented WebSocket for real-time gameplay experience, reducing latency and increasing user engagement significantly.",
        #             ],
        #         },
        #     ],
        # }
        # resume_data = {
        #     "work_experiences": [
        #         {
        #             "order": 0,
        #             "title": "Avocademy (YC W22)",
        #             "type": "Job",
        #             "techStack": [
        #                 "React",
        #                 "SpringBoot",
        #                 "OpenAI API",
        #                 "Fire Crawler",
        #                 "PuppeteerJS",
        #                 "PlayWright",
        #                 "SupaBase",
        #                 "MongoDB",
        #                 "Github",
        #                 "CI/CD",
        #                 "A/B Testing",
        #                 "E2E testing",
        #                 "Vercel",
        #                 "Claude",
        #             ],
        #             "description": "Developing an automated tailoring job application where student just has to pre-fill in information and everyday, the system will automatically apply to desired job for them. Jobs will be crawl on daily basis and user can pick their desired job that they want to apply then system will autofill and apply to the job. We also use openai api to help extract necessary information to display to user.",
        #             "bulletDescription": "",
        #             "isBulletDescription": True,
        #             "quantifiableMetrics": "750+ daily job postings; 70000+ entries in database",
        #             "bulletPoints": "5",
        #             "duration": "Jun 2024 -- Sep 2024",
        #             "position": "Software Engineer Intern",
        #             "location": "Remote, US",
        #         },
        #         {
        #             "order": 1,
        #             "title": "FPT Software",
        #             "type": "Job",
        #             "techStack": ["AngularJS", "TypeScript", "JavaScript", "Observer"],
        #             "description": "Creating a functional webpage for Japanese Pharmacists Association. My tasks was to refined company's JavaScript SDK, to ensure it works with UI through multiple webpage and modals. I also create observer pattern that helps automate the 20,000 data binding from frontend to backend and vice versa, with high accuracy and consuming less time of coding. I also managed tasks and schedules in fast-paced environment, improving communication and collaboration using Agile-Scrum method",
        #             "bulletDescription": "",
        #             "isBulletDescription": True,
        #             "quantifiableMetrics": "500-1000 daily visits webpage, 350+ UIs and modals, 20,000 data entries",
        #             "bulletPoints": "4",
        #             "duration": "Jun 2023 -- Aug 2023",
        #             "position": "Software Engineer Intern",
        #             "location": "Hanoi, Vietnam",
        #         },
        #         {
        #             "order": 2,
        #             "title": "Viettel AI",
        #             "type": "Job",
        #             "techStack": [
        #                 "Solr",
        #                 "SBERT",
        #                 "NLP",
        #                 "Machine Learning",
        #                 "Microsoft Graph RAG",
        #                 "BM25",
        #             ],
        #             "description": "At Viettel AI, my main tasks were to doing research on how to develop a fully functional chatbot for Vietnamese people like the one that openAI has done with the world (chatgpt). I was working on creating the pipeline for searching system (first do fulltext search, after receiving the data, we could augmenting it by applying semantic search). After that, I was assigned to looking into the way to store and retrieve data using Microsoft Graph RAG",
        #             "bulletDescription": "",
        #             "isBulletDescription": True,
        #             "quantifiableMetrics": "",
        #             "bulletPoints": "2",
        #             "duration": "Jun 2024 -- Aug 2024",
        #             "position": "Machine Learning Engineer Intern",
        #             "location": "Hanoi, Vietnam",
        #         },
        #         {
        #             "order": 3,
        #             "title": "University of Massachusetts Amherst",
        #             "type": "Job",
        #             "techStack": [""],
        #             "description": "",
        #             "bulletDescription": "• Functioned as a teaching assistant for 1,500+ students across 6 consecutive semesters\n• Led instruction in DSA, Web Programming, Programming Methodology, Discrete Mathematics, and Machine Learning class",
        #             "isBulletDescription": False,
        #             "quantifiableMetrics": "",
        #             "bulletPoints": "",
        #             "duration": "Sep 2022 -- Current",
        #             "position": "Teaching Assistance",
        #             "location": "Amherst, MA",
        #         },
        #     ],
        #     "personal_projects": [
        #         {
        #             "order": 4,
        #             "title": "CloudCueAI",
        #             "type": "Project",
        #             "techStack": [
        #                 "AWS Lambda",
        #                 "API Gateway",
        #                 "S3",
        #                 "Transcribe",
        #                 "CloudWatch",
        #                 "SAM Cli",
        #                 "ExpressJS",
        #                 "Flask",
        #                 "React-D3-Cloud",
        #                 "DynamoDB",
        #                 "Cognito",
        #                 "IAM policies",
        #                 "JWT",
        #                 "OAuth",
        #                 "Terraform",
        #                 "GitHub Actions",
        #             ],
        #             "description": "Noticing that many people, especially international students struggle in finding the word or phrase to describe a situation during interview, I created a tools that suggest word in real time. All we have to do is that speaking into the mic, the live transcribe by Amazon will help transcribe those voice data and send back to us. Then I use a Facebook OPT-1.3b model to find the next highest chance occuring word so that it would act as the word suggestion based on the context is what we were saying. And those suggested word will be display in terms of word cloud with its size correspond to the weight. Later, all of the transcribe is saved under S3 storage",
        #             "bulletDescription": "",
        #             "isBulletDescription": True,
        #             "quantifiableMetrics": "500-1000 daily visits webpage, 350+ UIs and modals, 20,000 data entries",
        #             "bulletPoints": "4",
        #         },
        #         {
        #             "order": 5,
        #             "title": "Beatcode",
        #             "type": "Project",
        #             "techStack": [
        #                 "FastAPI",
        #                 "RestfulAPI",
        #                 "Docker",
        #                 "WebSocket",
        #                 "PostgreSQL",
        #                 "PassLib",
        #                 "SQLAlchemy",
        #                 "CORS",
        #                 "OAuth",
        #                 "Kubernetes",
        #                 "JWT",
        #             ],
        #             "description": "Beatcode is the coding game that got its original idea from Tetris and Leetcode, where we will now live dual battle leetcode 1v1 versus another person from internet. My main duties were creating backend APIs, Websocket, setting up the Docker environment so that player could submit their code. I use PostGreSQL to store everything from players data, performance metrics, etc. Also I built OAuth so that everyone can login smoothly. Moreover, I doing a bit of frontend where I play around with Svelte and do the testing thing with PlayWright",
        #             "bulletDescription": "",
        #             "isBulletDescription": True,
        #             "quantifiableMetrics": "500+ players during beta, 1,000+ concurrent users, 300 unique account created in first 12 hours",
        #             "bulletPoints": "4",
        #         },
        #         {
        #             "order": 6,
        #             "title": "OhEss",
        #             "type": "Project",
        #             "techStack": [
        #                 "Google Lighthouse",
        #                 "React",
        #                 "Linux",
        #                 "Kolibri",
        #                 "NextJS",
        #                 "Vercel",
        #             ],
        #             "description": "",
        #             "bulletDescription": "• Engineered a web-based Windows 10 operating system replica with TypeScript and React, achieving a 100% Google Lighthouse SEO score for seamless UI interaction\n• Integrated Kolibri and Linux programs into a NextJS interface on Vercel, enabling in-browser files hosting for 200+ users",
        #             "isBulletDescription": False,
        #             "quantifiableMetrics": "",
        #             "bulletPoints": "",
        #         },
        #         {
        #             "order": 7,
        #             "title": "Sculpt AI",
        #             "type": "Project",
        #             "techStack": ["Tensorflow", "OpenCV", "SAM model", "MediaPipe"],
        #             "description": "",
        #             "bulletDescription": "• Pioneered 3D solution for Metaverse platforms, using AI-based image cropping and Blender modeling, cutting manual effort by 30%\n• Implement body pose tracking and measurement with MediaPipe, achieving a prototype success rate of 85% during the hackathon",
        #             "isBulletDescription": False,
        #             "quantifiableMetrics": "",
        #             "bulletPoints": "",
        #         },
        #     ],
        # }
        # university_data = {
        #     "university": "UMass Emherrssstt",
        #     "degree": "Bachelor of Mestar",
        #     "gpa": "4.7",
        #     "graduate": "Mei 2026",
        #     "location": "Amherst, MAAA",
        #     "courses": "Algorithm for Data Science, Discrete Mathematics, Algorithm Design, Search Engine, Computer Systems, Advance Linear Algebra, Programming Methodology, Machine Learning, Operating System, Computer Architecture, I don't study LOL",
        # }
        # augmented_skills_data_raw = {
        #     "profile_data": {
        #         "name": "Minh Vu",
        #         "email": "quackqueck@gmail.com",
        #         "phone": "123456789",
        #         "linkedin": "https://www.linkedin.com/in/minhvu02/",
        #         "github": "https://github.com/Tristesse02",
        #         "languages": "Java, Python, JavaScript, Typescript, HTML, CSS, C/C++, C#, Go, Rust, Swift, Kotlin",
        #         "frameworks": "MongoDB, ExpressJS, ReactJS, NodeJS, AngularJS, SpringBoot, Docker, SQL, Supabase, PouchDB",
        #     },
        #     "university_data": {
        #         "university": "UMass Emherrssstt",
        #         "degree": "Bachelor of Mestar",
        #         "gpa": "4.7",
        #         "graduate": "Mei 2026",
        #         "location": "Amherst, MAAA",
        #         "courses": "Algorithm for Data Science, Discrete Mathematics, Algorithm Design, Search Engine, Computer Systems, Advance Linear Algebra, Programming Methodology, Machine Learning, Operating System, Computer Architecture, I don't study LOL",
        #     },
        #     "resume_data": {
        #         "work_experiences": [
        #             {
        #                 "order": 0,
        #                 "title": "Avocademy (YC W22)",
        #                 "type": "Job",
        #                 "techStack": [
        #                     "React",
        #                     "SpringBoot",
        #                     "OpenAI API",
        #                     "Fire Crawler",
        #                     "PuppeteerJS",
        #                     "PlayWright",
        #                     "SupaBase",
        #                     "MongoDB",
        #                     "Github",
        #                     "CI/CD",
        #                     "A/B Testing",
        #                     "E2E testing",
        #                     "Vercel",
        #                     "Claude",
        #                 ],
        #                 "description": "Developing an automated tailoring job application where student just has to pre-fill in information and everyday, the system will automatically apply to desired job for them. Jobs will be crawl on daily basis and user can pick their desired job that they want to apply then system will autofill and apply to the job. We also use openai api to help extract necessary information to display to user.",
        #                 "bulletDescription": "",
        #                 "isBulletDescription": True,
        #                 "quantifiableMetrics": "750+ daily job postings; 70000+ entries in database",
        #                 "bulletPoints": "5",
        #                 "duration": "Jun 2024 -- Sep 2024",
        #                 "position": "Software Engineer Intern",
        #                 "location": "Remote, US",
        #             },
        #             {
        #                 "order": 1,
        #                 "title": "FPT Software",
        #                 "type": "Job",
        #                 "techStack": [
        #                     "AngularJS",
        #                     "TypeScript",
        #                     "JavaScript",
        #                     "Observer",
        #                 ],
        #                 "description": "Creating a functional webpage for Japanese Pharmacists Association. My tasks was to refined company's JavaScript SDK, to ensure it works with UI through multiple webpage and modals. I also create observer pattern that helps automate the 20,000 data binding from frontend to backend and vice versa, with high accuracy and consuming less time of coding. I also managed tasks and schedules in fast-paced environment, improving communication and collaboration using Agile-Scrum method",
        #                 "bulletDescription": "",
        #                 "isBulletDescription": True,
        #                 "quantifiableMetrics": "500-1000 daily visits webpage, 350+ UIs and modals, 20,000 data entries",
        #                 "bulletPoints": "4",
        #                 "duration": "Jun 2023 -- Aug 2023",
        #                 "position": "Software Engineer Intern",
        #                 "location": "Hanoi, Vietnam",
        #             },
        #             {
        #                 "order": 2,
        #                 "title": "Viettel AI",
        #                 "type": "Job",
        #                 "techStack": [
        #                     "Solr",
        #                     "SBERT",
        #                     "NLP",
        #                     "Machine Learning",
        #                     "Microsoft Graph RAG",
        #                     "BM25",
        #                 ],
        #                 "description": "At Viettel AI, my main tasks were to doing research on how to develop a fully functional chatbot for Vietnamese people like the one that openAI has done with the world (chatgpt). I was working on creating the pipeline for searching system (first do fulltext search, after receiving the data, we could augmenting it by applying semantic search). After that, I was assigned to looking into the way to store and retrieve data using Microsoft Graph RAG",
        #                 "bulletDescription": "",
        #                 "isBulletDescription": True,
        #                 "quantifiableMetrics": "",
        #                 "bulletPoints": "2",
        #                 "duration": "Jun 2024 -- Aug 2024",
        #                 "position": "Machine Learning Engineer Intern",
        #                 "location": "Hanoi, Vietnam",
        #             },
        #         ],
        #         "personal_projects": [
        #             {
        #                 "order": 4,
        #                 "title": "CloudCueAI",
        #                 "type": "Project",
        #                 "techStack": [
        #                     "AWS Lambda",
        #                     "API Gateway",
        #                     "S3",
        #                     "Transcribe",
        #                     "CloudWatch",
        #                     "SAM Cli",
        #                     "ExpressJS",
        #                     "Flask",
        #                     "React-D3-Cloud",
        #                     "DynamoDB",
        #                     "Cognito",
        #                     "IAM policies",
        #                     "GitHub Actions",
        #                     "Terraform",
        #                     "OAuth",
        #                     "JWT",
        #                 ],
        #                 "description": "Noticing that many people, especially international students struggle in finding the word or phrase to describe a situation during interview, I created a tools that suggest word in real time. All we have to do is that speaking into the mic, the live transcribe by Amazon will help transcribe those voice data and send back to us. Then I use a Facebook OPT-1.3b model to find the next highest chance occuring word so that it would act as the word suggestion based on the context is what we were saying. And those suggested word will be display in terms of word cloud with its size correspond to the weight. Later, all of the transcribe is saved under S3 storage",
        #                 "bulletDescription": "",
        #                 "isBulletDescription": True,
        #                 "quantifiableMetrics": "500-1000 daily visits webpage, 350+ UIs and modals, 20,000 data entries",
        #                 "bulletPoints": "4",
        #             },
        #             {
        #                 "order": 5,
        #                 "title": "Beatcode",
        #                 "type": "Project",
        #                 "techStack": [
        #                     "FastAPI",
        #                     "RestfulAPI",
        #                     "Docker",
        #                     "WebSocket",
        #                     "PostgreSQL",
        #                     "PassLib",
        #                     "SQLAlchemy",
        #                     "CORS",
        #                     "OAuth",
        #                     "Kubernetes",
        #                     "JWT",
        #                 ],
        #                 "description": "Beatcode is the coding game that got its original idea from Tetris and Leetcode, where we will now live dual battle leetcode 1v1 versus another person from internet. My main duties were creating backend APIs, Websocket, setting up the Docker environment so that player could submit their code. I use PostGreSQL to store everything from players data, performance metrics, etc. Also I built OAuth so that everyone can login smoothly. Moreover, I doing a bit of frontend where I play around with Svelte and do the testing thing with PlayWright",
        #                 "bulletDescription": "",
        #                 "isBulletDescription": True,
        #                 "quantifiableMetrics": "500+ players during beta, 1,000+ concurrent users, 300 unique account created in first 12 hours",
        #                 "bulletPoints": "4",
        #             },
        #         ],
        #     },
        #     "job_description": "1. Cloud Engineer (Serverless & DevOps)\nLocation: Remote / Hybrid\nJob Type: Full-time\n\nAbout the Role:\nWe are seeking a Cloud Engineer specializing in serverless architectures and DevOps automation. You will design and maintain scalable cloud infrastructure, optimize deployments, and enhance system reliability through automation and CI/CD best practices.\n\nResponsibilities:\nDesign and maintain serverless applications using AWS Lambda, API Gateway, S3, DynamoDB, and Cognito.\nAutomate infrastructure management using Terraform, AWS SAM, and Kubernetes.\nOptimize CI/CD pipelines with GitHub Actions, GitLab CI, and Jenkins.\nEnhance security and authentication using JWT, OAuth, and IAM policies.\nImplement monitoring and observability with CloudWatch and logging solutions.\nPreferred Qualifications:\nExperience with multi-cloud environments (AWS, GCP, Azure).\nStrong knowledge of containerized deployments and orchestration.\nExposure to CDN optimization and edge computing.",
        # }
        # jobs_no_need_tailor = {
        #     "University of Massachusetts Amherst": [
        #         "Functioned as a teaching assistant for 1,500+ students across 6 consecutive semesters",
        #         "Led instruction in DSA, Web Programming, Programming Methodology, Discrete Mathematics, and Machine Learning class",
        #     ]
        # }
        # projects_no_need_tailor = {
        #     "OhEss": [
        #         "Engineered a web-based Windows 10 operating system replica with TypeScript and React, achieving a 100% Google Lighthouse SEO score for seamless UI interaction",
        #         "Integrated Kolibri and Linux programs into a NextJS interface on Vercel, enabling in-browser files hosting for 200+ users",
        #     ],
        #     "Sculpt AI": [
        #         "Pioneered 3D solution for Metaverse platforms, using AI-based image cropping and Blender modeling, cutting manual effort by 30%",
        #         "Implement body pose tracking and measurement with MediaPipe, achieving a prototype success rate of 85% during the hackathon",
        #     ],
        # }
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


## [Docker version], consider for later updates:
# @app.route("/download-pdf", methods=["GET"])
# def download_pdf():
#     """Send the generated PDF to frontend."""
#     if os.path.exists(OUTPUT_PDF):
#         response = send_file(OUTPUT_PDF, as_attachment=True)

#         # Optional cleanup after sending
#         try:
#             os.remove(OUTPUT_PDF)
#             os.remove(OUTPUT_LATEX)
#         except Exception as e:
#             print(f"Cleanup failed: {e}")

#         return response
#     return jsonify({"error": "PDF file not found"}), 404
## End of [Docker version]


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


# def compile_latex_to_pdf(latex_file, output_pdf):
#     """Compiles the LaTeX file into a PDF using `pdflatex`."""
#     output_dir = os.path.dirname(output_pdf)
#     try:
#         result = subprocess.run(
#             ["which", "pdflatex"],  # This will print the pdflatex path
#             check=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         print(f"pdflatex Path: {result.stdout.decode().strip()}")  # Debugging output

#         subprocess.run(
#             ["pdflatex", "-output-directory", output_dir, latex_file],
#             check=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         print("PDF generated successfully!")
#     except subprocess.CalledProcessError as e:
#         print(f"Error in LaTeX compilation: {e.stderr.decode()}")


if __name__ == "__main__":
    try:
        # app.run(port=5000, debug=True, use_reloader=True)
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
