import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Resume excerpt and job description
resume_excerpt = "Managed 70,000+ database entries to efficiently monitor job postings and platform activity using MongoDB."
job_description = "Looking for a candidate who can design and maintain database systems to track millions of records."

# Tailoring prompt
prompt = f"""
Here is a resume excerpt:
"{resume_excerpt}"

And here is a job description:
"{job_description}"

Suggest a tailored revision of the resume excerpt to match the job description.
"""

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Generate chat completion
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that tailors resumes to match job descriptions.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ],
    model="gpt-4o",
)

# Print the tailored result
print(chat_completion.choices[0].message.content)
