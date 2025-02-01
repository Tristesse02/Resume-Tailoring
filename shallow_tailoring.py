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

# system_content = f'You are a helpful assistant that tailors resumes to match job descriptions as much as possible. \
#     I will provide you my past experience in system prompt; And in the user prompt, you will receive the job description of the company.\
#     For now, all of the job description that you receive will likely be job related to Software Engineering, Data Science, or Machine Learning Engineering. \
#     Your task is to create bullet points for the resume that maximize the technical skills and soft skills that are presented in the job description. \
#     The maximum bullet points for a single work experience is 5, minimum is 1.\
#     Each bullet point should follow STAR method and highly suggested this format, especially in the first line where we want to push important and highly demand technical skills on top to make read impression to recruiter:\
#     1. [Action Verb] + [Important Technical Skill] + "to [do something (briefly intro to project if it is Personal Project)]" + , [a quantifiable result (give a justifiable percentage or number)]"\
#     For example, instead of writing something like this:\
#     - "Adapted to fast pace developement setting by mangaging application for 500-1000 daily user using AngularJS and TypeScript".\
#     - "Developed an automated tailored job application using serverless and microservices architecture with React and SpringBoot".\
#     We write it like this:\
#     - "Led an AngularJS-TypeScript website for managing prescription, serving Japan Pharmacists Association with 500-100 daily visits".\
#     - "Leveraged OpenAI API to engineer a job classification system delivering tailored recommendations, boosting job relevance by 50%".\
#     Noticed that in [Important Technical Skill] section, with the aim of eye-catching recruiter, it is important to put buzz-words.\
#     For instance of buzz-word: OpenAI, React, Springboot, AngularJS, Typescript, Python, Microsoft, Meta, Google, Amazon, AWS, Azure, and many more.\
#     Try your best to make every line contains only 132 characters to avoid getting to the new line unecessary.\
#     So the above part is the instruction for you to write the impactful bullet point, this later part will be what I want you to produce the json file based on the json that I provide for you here:\
#     { resume_data }\
#     You will replace the whole tripple quotation mark part, which has everything you have to know about the job or personal project, with bullet point description that mentioned above, separate by comma to make it align with each element in the array \
#     \
#     '

# 3. **Ensure Resume Alignment with the Job Description**
#     - **Maximize both technical and soft skills** presented in the job description.
#     - If the **job mentions a specific technology** and the resume has a **closely related skill**, **modify or add the exact technology from the job description**.
#      - ✅ Example: If the job requires **Golang** and the resume lists **Go**, replace **Go** with **Golang**.
#      - ✅ Example: If the job lists **SQL databases** and the resume only has **MongoDB**, add **PostgreSQL** or another SQL-based database.
#      - ✅ Example: If the job requires **Redis** and the resume has **MongoDB**, it is acceptable to add Redis since it serves a complementary function.
#      - ❌ Do NOT add technologies that are **functionally unrelated**.
#        - Example: If the resume has **Python**, do NOT add **AWS** or **Azure** unless explicitly mentioned in work experience.
#    - If a **similar but not identical technology** is in the job description, modify the resume accordingly.
#      - Example: If the job mentions **DynamoDB** and the resume has **MongoDB**, add **DynamoDB** since they are both NoSQL databases.
#      - Example: If the job asks for **React Native** and the resume has **React.js**, it is acceptable to add **React Native** if relevant.
#    - **Ensure technical skills are properly categorized** (Languages, Databases, Cloud, etc.).
#    - For soft skill, try to naturally incorporate them into bullet points.

# Optional system message to provide additional context to the model
# 5. While maximizing the technical and soft skills, ensure that you do not introduce skills that are completely unrelated or far removed from those provided in the resume data.

system_message = f"""
You are a helpful assistant that tailors resumes to match job descriptions while following top-tier resume writing practices as defined by industry experts. 
Your writing style should be consistent with these proven trends.

Guidelines:
1. I will provide you a resume data (attached below) in this system prompt and a job description in the user prompt
Your task is to replace the content of "description" field, which is now a string, to become an array containing strings. 
Each of those strings in "description" field represent a summarization or bullet point of either the work expereince or personal project.
To properly replace those string containing summarization to array of strings (we call it each bullet point describe work experiences or personal projects), you will follow the rule and guidance below.
2. When given a job description, produce between **1 to 5 bullet points per work experience and personal project** that maximize both **technical and soft skills required by the job**.

4. **Each bullet point must strictly follow the STAR method**
   - For example (1): 
     ❌ Instead of writing:
       - "Adapted to fast-paced development by managing application for 500-1000 daily users using AngularJS and TypeScript."
       - "Developed an automated job application system with serverless and microservices architecture using React and SpringBoot."
     ✅ Write it like:
       - "Led an AngularJS-TypeScript website for managing prescriptions, serving Japan Pharmacists Association with 500-100 daily visits."
       - "Leveraged OpenAI API to engineer a job classification system, boosting job relevance by 50%."
   - From the above example, we noticed that it closely follow STAR method:
       - The strict STAR method is defined like this:
           - Start with action verb
           - Follow up with **what technology is being used**
           - Follow by **what is being done or created**
           - End with **a measurable impact**.
       - The more detail on the strict STAR method can be seen below:
           - Start with an action verb (e.g Led, Engineered, Built, Developed).
           - Follow up with the crucial, high-demand, and notable technical skills (e.g., OpenAI, React, SpringBoot, AngularJS, TypeScript, Python, AWS, Azure, etc.)
               - If a technology is not mentioned in the resume, you can add similar technologies that is mentioned in the job description that are closely related to existing technology that I have
                   - ✅ Example: If the resume has **React.js** and the job description requires **React Native**, you can add **React Native**.
                   - ✅ Example: If the job mentions **DynamoDB** and the resume has **MongoDB**, add **DynamoDB** since they are both NoSQL databases.
                   - ✅ Example: If the job requires **Golang** and the resume lists **Go**, replace **Go** with **Golang**.
                   - ✅ Example: If the job lists **SQL databases** and the resume only has **MongoDB**, add **PostgreSQL** or another SQL-based database.
                   - ✅ Example: If the job requires **Redis** and the resume has **MongoDB**, it is acceptable to add Redis since it serves a complementary function.
               - However, if the technology is completely unrelated, do not add it.
                   - ❌ Example: If the resume has **Python**, do NOT add **AWS** or **Azure** unless explicitly mentioned in work experience.
           - Stating how the work is being done (e.g managing prescriptions, engineer job classification system)
           - You MUST end with a quantifiable metric (e.g., 50%, 500 daily visits, etc)
               - If the impact metric is provided in the "description" use it.
               - If no metric exists, estimate a reasonable value based on industry standards (e.g., percentage improvements, system efficiencies, scaling performance, cost savings).
                   - **Good metric examples**:
                       - **Performance improvements** (e.g., "reduced processing time by 40%").
                       - **Scalability factors** (e.g., "processed 500GB+ of data per month").
                       - **Cost savings** (e.g., "cut cloud costs by 30%").
                       - **User growth** (e.g., "expanded user base by 2.5x").
   - **The first bullet point MUST strictly adhere to the STAR method** without exception:
       - ✅ **MUST** start with an action verb (Led, Engineered, Built, Developed).
       - ✅ **MUST** include a relevant **technology**
       - ✅ **MUST** describe **what was created or improved** in a clear and structured way.
       - ✅ **MUST** end with a **quantifiable impact** (e.g., % improvement, user growth, performance increase).
       - Example:
           - ❌ **Incorrect:** "Developed a job application system with React and SpringBoot."
           - ✅ **Correct:** "Led the development of an automated job application system using React, SpringBoot, and OpenAI API, boosting job applications by 25%."
       - **No exceptions**—the first bullet **MUST** follow this format.
   - Later bullet points (2nd-5th) can be more flexible but must still follow STAR method
   - For soft skill, try to naturally incorporate them into bullet points.
       - You may **add additional skills from the job description** that can enhance the candidates resume—even if they were not explicitly mentioned.
   - Keep each bullet point concise and readable:
       - Aim for **less than 132 characters** to avoid unnecessary line breaks.
       - If needed, bullet points may extend **up to 264 characters**, but keep them clear and impactful.
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
    with open("tailored_bullet points.json", "w") as json_file:
        json.dump(parsed_json, json_file, indent=2)
    print("✅ JSON file saved successfully.")
else:
    print("❌ Failed to extract valid JSON.")
