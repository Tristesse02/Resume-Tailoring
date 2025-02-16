import re
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# with open("data_to_parse.txt", "r") as file:
#     resume_data = file.read()

with open("sample_data/resume_data.json", "r") as file:
    resume_data = json.load(file)

# Tailoring prompt
job_description = """
Full Stack Developer
About the Role  
We are looking for a highly skilled Full Stack Developer to join our team. You will be responsible for designing, developing, and maintaining scalable web applications, working across both frontend and backend technologies. If you thrive in an agile environment and enjoy building high-performance, user-friendly applications, we'd love to hear from you!  

Responsibilities  
- Develop and maintain scalable web applications using modern frontend and backend technologies.  
- Design and implement responsive and interactive user interfaces using frameworks like React, Vue.js, or Angular.  
- Build and maintain RESTful APIs and GraphQL endpoints to support frontend applications.  
- Work with databases (SQL and NoSQL) to manage application data efficiently.  
- Ensure applications are optimized for speed, scalability, and security.  
- Implement authentication and authorization mechanisms using OAuth, JWT, or session-based authentication.  
- Collaborate with UI/UX designers, product managers, and other developers to ensure a seamless user experience.  
- Write clean, maintainable, and well-documented code, following best practices.  
- Conduct code reviews, implement testing strategies, and improve application performance.  
- Deploy, monitor, and troubleshoot applications in cloud environments (AWS, GCP, or Azure).  

Required Skills & Qualifications  
- Strong proficiency in JavaScript, TypeScript, or Python.  
- Experience with frontend frameworks such as React, Vue.js, or Angular.  
- Knowledge of backend frameworks like Node.js (Express, Nest.js), Django, Flask, or Spring Boot.  
- Expertise in database management using PostgreSQL, MySQL, MongoDB, or Firebase.  
- Hands-on experience with RESTful APIs, GraphQL, WebSockets, and microservices architecture.  
- Familiarity with CI/CD pipelines (GitHub Actions, GitLab CI, or Jenkins).  
- Experience working with Docker, Kubernetes, and cloud platforms (AWS/GCP/Azure).  
- Strong understanding of version control (Git) and agile development methodologies.  
- Knowledge of testing frameworks like Jest, Cypress, or Mocha.  
- Experience with serverless architecture (AWS Lambda, Firebase Functions) is a plus.  

Preferred Qualifications  
- Experience in DevOps practices and infrastructure as code (Terraform, Ansible).  
- Understanding of performance optimization techniques for web applications.  
- Knowledge of WebAssembly (WASM), Edge Computing, or WebRTC is a plus.  
- Familiarity with machine learning APIs or AI-powered applications is a bonus.  

Why Join Us?  
- Competitive salary and performance-based bonuses.  
- Flexible work arrangements (remote/hybrid).  
- Opportunities for professional growth and learning.  
- A dynamic, fast-paced work environment with a passionate team.  
- Health, wellness, and development benefits.  

How to Apply:
Send your resume and portfolio (GitHub/LinkedIn) to [Your Email/Job Portal Link]. We look forward to hearing from you!  
"""
    # 5.2 However, if the technology is completely unrelated, do not add it.
    #     - If the resume has **Python**, do NOT add **AWS** or **Azure** unless explicitly mentioned in "description" field

system_message = f"""
You are a helpful assistant that helps me tailor my resume so that it could fit the job description as much as possible.
Below are guidelines to follow:

1. You will receive a my resume_data on work experience, personal projects, and skills in form of JSON format in this system prompt.
I will provide you the job description in the user prompt. And your task is try to create bullet points for the resume that maximize the technical skills and soft skills that are presented in the job description.
2. Your task is to replace the string in the "description" field in provided JSON data as the array containing bullet points for each work experience and personal project.
3. For each job description, you should create a maximum of 5 bullet points and a minimum of 2 bullet points.
4. Each bullet point should follow the following method:
    4.1 For the first bullet point of each job description and personal project, you should strictly follow this writing style:
        - "[Action Verb] + [Important Technical Skill] + "to [do something (briefly intro to project if it is Personal Project)]" + , [a quantifiable result (give a justifiable percentage or number)]"
        - For example:
            You should write:
                - "Led an AngularJS-TypeScript website for managing prescriptions, serving Japan Pharmacists Association with 500-100 daily visits."
                - "Leveraged OpenAI API to engineer a job classification system, boosting job relevance by 50%."
            Don't write:
                - "Adapted to fast-paced development by managing application for 500-1000 daily users using AngularJS and TypeScript."
                - "Developed an automated job application system with serverless and microservices architecture using React and SpringBoot."
        - The [Important Technical Skills] should be buzzwords (tech skills that are highly demand in the fields or highly required in the job description) like OpenAI, React, Springboot, AngularJS, Typescript, Python, Microsoft, Meta, Google, Amazon, AWS, Azure, etc.
    4.2 For the rest of the bullet points, you can follow the rule listed in 4.1 or you can write in a more general way but MUST have these components:
        - Start with an action verb
        - Include Important Technical Skills
        - Mention what is being done
        - Include a quantifiable result (e.g., percentage improvement, number of users, etc.)
        - For example:
            - "Managed 70,000+ database entries to efficiently monitor job posting, user data, and platform activity using MongoDB and Supabase"
            - "Streamlined the extraction of 750+ daily job postings and automated applications using Fire Crawler, PuppeteerJS, and Playwright
            - "Built OAuth, session management with Passlib, and CORS support client-server interaction, improving security compliance by 40%"
            - "Enhanced employee property search using Solr for text and SBERT for semantic search, boosting mean average precision by 25%"
            - "Pioneered 3D solution for Metaverse platforms, using AI-based image cropping and Blender modeling, cutting manual effort by 30%"
    4.3 Try to make every line contains only 132 characters to avoid getting to the new line unnecessarily. If you found out a line is longer than 132 characters, try to break it down into two lines, and make sure both lines follow the above rules.
    4.4 For the soft skills, try to naturally incorporate them into bullet points.
5. Noticed!
    5.1 For Important Technical Skills, if the technical skills not listed in the resume_data "description" field but listed in the job description, don't hesitate to incorporate them into bullet point if they are related (since we are trying to maximize the technical skills in the job description).


### Provided resume data:
{resume_data}
"""

user_message = f"""
Job Description:
"{job_description}"
"""

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Generate chat completion
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ],
    model="gpt-4o",
)

# Get GPT response
output_content = chat_completion.choices[0].message.content.strip()
print(output_content)


# **Step 1: Extract JSON from Response**
def extract_json(text):
    """Extracts valid JSON from an OpenAI response (handles markdown and extra text)."""
    match = re.search(r"```json\s*([\s\S]+?)\s*```", text)  # Look for JSON code block
    json_str = match.group(1) if match else text  # If no markdown, assume pure JSON

    try:
        return json.loads(json_str)  # Validate JSON
    except json.JSONDecodeError as e:
        print("Error: Invalid JSON output:", e)
        return None  # Handle error case


# **Step 2: Parse the JSON Output**
parsed_json = extract_json(output_content)

# **Step 3: Write JSON to a File If Valid**
if parsed_json:
    with open("tailored_bullet_points.json", "w") as json_file:
        json.dump(parsed_json, json_file, indent=2)
    print("JSON file saved successfully.")
else:
    print("Failed to extract valid JSON.")