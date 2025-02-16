import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv


class DeepResumeTailor:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        # self.tailor = ResumeTailor("temp_personal_info.json")

    # If you found out a line is longer than 132 characters, try to break it down into two lines, and make sure both lines follow the above rules.

    def generate_system_message(self, resume_data):
        return f"""
        You are a helpful assistant that helps me tailor my resume so that it could fit the job description as much as possible.
        Below are guidelines to follow:

        1. You will receive a my resume_data on work experience, personal projects, and skills in form of JSON format in this system prompt.
        I will provide you the job description in the user prompt. And your task is try to create bullet points for the resume that maximize the technical skills and soft skills that are presented in the job description.
        2. Your task is to replace the string in the "description" field in provided JSON data as the array containing bullet points for each work experience and personal project.
        3. For each job description, the number of bullet points will be stated in the "description" field.
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
            4.3 Try to make every line contains around 17 words to avoid getting to the new line unnecessarily. 
            4.4 For the soft skills, try to naturally incorporate them into bullet points.
        5. Make sure that you must return the updated resume_data as a JSON object while preserving its structure.


        ### Provided resume data:
        {resume_data}
        """

    def tailor_resume(self, input_data):
        try:
            resume_data = input_data.get("resume_data", {})
            job_description = input_data.get("job_description", "")

            # print("minhdz", resume_data, job_description, flush=True)

            # More error handling
            if not resume_data or not job_description:
                raise ValueError(
                    "Missing required fields: resume_data or job_description."
                )

            system_message = self.generate_system_message(resume_data)
            user_message = f"Job Description:\n{job_description}"

            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    model="gpt-4o",
                )

                # TODO: Error handling: We are largely assuming that output_content has ```json``` block so that .extract_json() can work
                output_content = chat_completion.choices[0].message.content.strip()
                # print("ducdz", output_content, flush=True)
                return self.extract_json(output_content)
            except Exception as e:
                print("Error during OpenAI processing:", str(e))
                return None
        except Exception as e:
            print(
                "Error due to fail of extraction of resume_data or job_description",
                str(e),
            )
            return None

    @staticmethod
    def extract_json(text):
        # TODO: Recheck why the result giving back from gpt is so sus and extraction of json
        """Extracts valid JSON from an OpenAI response (handles markdown and extra text)."""
        match = re.search(r"```json\s*([\s\S]+?)\s*```", text)
        json_str = match.group(1) if match else text
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Error: Invalid JSON output:", e)
            return None
