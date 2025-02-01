import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

with open("data_to_parse.txt", "r") as file:
    resume_data = file.read()

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

# Optional system message to provide additional context to the model
# 5. While maximizing the technical and soft skills, ensure that you do not introduce skills that are completely unrelated or far removed from those provided in the resume data.

system_message = f"""
You are a helpful assistant that tailors resumes to match job descriptions while following top-tier resume writing practices as defined by industry experts. Your writing style should be consistent with these proven trends.

Guidelines:
1. I will supply you with my complete resume data (see resume_data below) which includes past work experiences, personal projects, technical skills, and more.
2. When given a job description, produce between 1 to 5 bullet points per work experience that maximize both technical and soft skills required by the job.
3. Each bullet point must follow the STAR method:
   - The **first line** of each bullet point must strictly adhere to this style: it should begin with an action verb immediately followed by the most important technical skills that the company is seeking. This ensures that recruiters see that keyword first.
   - For example, instead of writing:
       - "Adapted to fast-paced development by managing application for 500-1000 daily users using AngularJS and TypeScript."
       - "Developed an automated job application system with serverless and microservices architecture using React and SpringBoot."
     Write it like:
       - "Led an AngularJS-TypeScript website for managing prescriptions, serving Japan Pharmacists Association with 500-100 daily visits."
       - "Leveraged OpenAI API to engineer a job classification system, boosting job relevance by 50%."
   - For any additional lines in the bullet point, follow the STAR method more flexibly by describing what was done, how it was done, and include a quantifiable result (e.g., "[quantifiable metric]").
4. Emphasize buzzwords and highly demanded technical skills (e.g., OpenAI, React, SpringBoot, AngularJS, TypeScript, Python, AWS, Azure, etc.) to catch recruiters' attention. Do not hesitate to incorporate additional skills from the job description that can pair with or enhance the existing skills from the resume data—even if those skills are not explicitly mentioned.
5. Ensure that each bullet point is concise. Aim for less than 132 characters to avoid unnecessary line breaks; however, if needed, a bullet point can extend into two lines (but should remain under 264 characters).
6. Finally, output the tailored bullet points as a JSON array. Replace the entire content inside the triple quotes in resume_data with the newly generated bullet points, ensuring each bullet point aligns with an element in the array.

Here is the resume_data you need to work with:
{resume_data}
"""

user_message = f"""
Here is job description:
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

# Extract the output content
output_content = chat_completion.choices[0].message.content.strip()
# TODO: separate the input text for expertise and project description for easier modification and parsing 

# Option 1: If you trust that the output is valid JSON, you can directly write it to a file.
with open("tailored_resume_bullet_points.json", "w") as json_file:
    json_file.write(output_content)

# Option 2: Alternatively, you can parse it into a Python object to verify its validity before saving.
try:
    bullet_points = json.loads(output_content)
    with open("tailored_resume_bullet_points.json", "w") as json_file:
        json.dump(bullet_points, json_file, indent=2)
    print("JSON file saved successfully.")
except json.JSONDecodeError as e:
    print("Failed to parse the output as JSON:", e)
