# import re
# import os
# import sys
# import json
# from openai import OpenAI
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # OpenAI API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Read JSON input from Flask
# json_data = sys.stdin.read()

# try:
#     input_data = json.loads(json_data)
#     resume_data = input_data.get("resume_data", {})
#     job_description = input_data.get("job_description", "")
# except json.JSONDecodeError:
#     print("Error: Invalid JSON input.")
#     sys.exit(1)

# with open("sample_data/resume_data.json", "r") as file:
#     resume_data = json.load(file)

# # **System message**
# system_message = f"""
# You are a helpful assistant that helps me tailor my resume so that it could fit the job description as much as possible.
# Below are guidelines to follow:

# 1. You will receive a my resume_data on work experience, personal projects, and skills in form of JSON format in this system prompt.
# I will provide you the job description in the user prompt. And your task is try to create bullet points for the resume that maximize the technical skills and soft skills that are presented in the job description.
# 2. Your task is to replace the string in the "description" field in provided JSON data as the array containing bullet points for each work experience and personal project.
# 3. For each job description, you should create a maximum of 5 bullet points and a minimum of 2 bullet points.
# 4. Each bullet point should follow the following method:
#     4.1 For the first bullet point of each job description and personal project, you should strictly follow this writing style:
#         - "[Action Verb] + [Important Technical Skill] + "to [do something (briefly intro to project if it is Personal Project)]" + , [a quantifiable result (give a justifiable percentage or number)]"
#         - For example:
#             You should write:
#                 - "Led an AngularJS-TypeScript website for managing prescriptions, serving Japan Pharmacists Association with 500-100 daily visits."
#                 - "Leveraged OpenAI API to engineer a job classification system, boosting job relevance by 50%."
#             Don't write:
#                 - "Adapted to fast-paced development by managing application for 500-1000 daily users using AngularJS and TypeScript."
#                 - "Developed an automated job application system with serverless and microservices architecture using React and SpringBoot."
#         - The [Important Technical Skills] should be buzzwords (tech skills that are highly demand in the fields or highly required in the job description) like OpenAI, React, Springboot, AngularJS, Typescript, Python, Microsoft, Meta, Google, Amazon, AWS, Azure, etc.
#     4.2 For the rest of the bullet points, you can follow the rule listed in 4.1 or you can write in a more general way but MUST have these components:
#         - Start with an action verb
#         - Include Important Technical Skills
#         - Mention what is being done
#         - Include a quantifiable result (e.g., percentage improvement, number of users, etc.)
#         - For example:
#             - "Managed 70,000+ database entries to efficiently monitor job posting, user data, and platform activity using MongoDB and Supabase"
#             - "Streamlined the extraction of 750+ daily job postings and automated applications using Fire Crawler, PuppeteerJS, and Playwright
#             - "Built OAuth, session management with Passlib, and CORS support client-server interaction, improving security compliance by 40%"
#             - "Enhanced employee property search using Solr for text and SBERT for semantic search, boosting mean average precision by 25%"
#             - "Pioneered 3D solution for Metaverse platforms, using AI-based image cropping and Blender modeling, cutting manual effort by 30%"
#     4.3 Try to make every line contains only 132 characters to avoid getting to the new line unnecessarily. If needed, bullet points may extend up to 264 characters, but keep them clear and impactful.
#     4.4 For the soft skills, try to naturally incorporate them into bullet points.
# 5. Noticed!
#     5.1 For Important Technical Skills, if the technical skills not listed in the resume_data "description" field but listed in the job description, you can add incorporate them i:
#         - If the resume has **React.js** and the job description requires **React Native**, you can add **React Native**.
#         - If the job mentions **DynamoDB** and the resume has **MongoDB**, add **DynamoDB** since they are both NoSQL databases.
#         - If the job requires **Golang** and the resume lists **Go**, replace **Go** with **Golang**.
#         - If the job lists **SQL databases** and the resume only has **MongoDB**, add **PostgreSQL** or another SQL-based database.
#         - If the job requires **Redis** and the resume has **MongoDB**, it is acceptable to add Redis since it serves a complementary function.
#     5.2 However, if the technology is completely unrelated, do not add it.
#         - If the resume has **Python**, do NOT add **AWS** or **Azure** unless explicitly mentioned in "description" field

# ### Provided resume data:
# {resume_data}
# """

# user_message = f"Job Description:\n{job_description}"

# # Initialize OpenAI client
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# # Generate chat completion
# chat_completion = client.chat.completions.create(
#     messages=[
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": user_message},
#     ],
#     model="gpt-4o",
# )

# # Get GPT response
# output_content = chat_completion.choices[0].message.content.strip()
# print(output_content)  # TODO: debugging purpose


# # **Step 1: Extract JSON from Response**
# def extract_json(text):
#     """Extracts valid JSON from an OpenAI response (handles markdown and extra text)."""
#     match = re.search(r"```json\s*([\s\S]+?)\s*```", text)  # Look for JSON code block
#     json_str = match.group(1) if match else text  # If no markdown, assume pure JSON

#     try:
#         return json.loads(json_str)  # Validate JSON
#     except json.JSONDecodeError as e:
#         print("Error: Invalid JSON output:", e)
#         return None  # Handle error case


# # **Step 2: Parse the JSON Output**
# parsed_json = extract_json(output_content)

# # **Step 3: Write JSON to a File If Valid**
# if parsed_json:
#     print(json.dumps(parsed_json, indent=2))  # Output JSON to stdout
# else:
#     print(json.dumps({"error": "Invalid JSON response from OpenAI"}))

import sys
import json

# Read JSON input from Flask
json_data = sys.stdin.read()

try:
    input_data = json.loads(json_data)
    resume_data = input_data.get("resume_data", {})
    job_description = input_data.get("job_description", "")
except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON input"}))
    sys.exit(1)

# 🚀 Instead of calling OpenAI API, return a fixed JSON response
test_response = {
    "message": "Test successful! Backend received data from frontend.",
    "resume_data": resume_data,
    "job_description": job_description,
    "generated_bullet_points": [
        "Developed a resume-tailoring backend using Flask and React.",
        "Implemented JSON-based communication between frontend and backend.",
        "Tested backend response without OpenAI API calls.",
    ],
}

# Print response to be sent back to frontend
print(json.dumps(test_response, indent=2))
