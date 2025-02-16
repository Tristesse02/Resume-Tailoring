import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv


class ResumeSkillMatcher:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate_system_message(self, resume_data):
        return f"""
        You are a helpful assistant that enhances my resume by identifying and adding relevant technical skills to maximize the technical skills match with job descriptions.
        
        You will be given `resume_data`, a dictionary where:
        - Keys are job titles (do not modify these).
        - Values are lists of technical skills.

        In the user message, you will receive a job description that contains important technical skills.

        ### Your task:
        1. Extract key technical skills from the job description.
        2. Prioritize the most important skills (frequent or critical to the role).
        3. Add up to **4-5** new skills per experience/project.
        4. Append new skills to the array only if:
            - The skill is relevant based on the `description` field.
            - A related skill already exists in the array.
        5. Avoid duplicates and ensure logical relevance. Example mappings:
            - ChatGPT → Claude, DeepSeek
            - Java → Kotlin
            - Flask → FastAPI, Django
            - React → React Native, Vue.js, AngularJS
            - PostgreSQL → MySQL, SQL Server
            - AWS → Azure, GCP
            - Docker → Kubernetes
            - TensorFlow → PyTorch
            - NLP → Hugging Face, spaCy
        
        ### Output:
        Return the updated `resume_data` as a JSON object while preserving its structure.
        
        ### Provided Resume Data:
        {resume_data}
        """

    def match_skills(self, resume_data, job_description):
        system_message = self.generate_system_message(resume_data)
        user_message = f"Job Description:\n{job_description}"

        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            model="gpt-4o",
        )

        output_content = chat_completion.choices[0].message.content.strip()
        # print(output_content)
        return self.extract_json(output_content)

    @staticmethod
    def extract_json(text):
        """Extracts valid JSON from an OpenAI response (handles markdown and extra text)."""
        match = re.search(r"```json\s*([\s\S]+?)\s*```", text)
        json_str = match.group(1) if match else text
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Error: Invalid JSON output:", e)
            return None


# Example usage:
if __name__ == "__main__":
    matcher = ResumeSkillMatcher()

    resume_data = {
        "CloudCueAI": {
            "tech_skills": [
                "AWS Lambda",
                "API Gateway",
                "S3",
                "Transcribe",
                "CloudWatch",
                "SAM Cli",
                "ExpressJS",
                "Flask",
                "React-D3-Cloud",
            ],
            "description": "Noticing that many people, especially international students struggle in finding the word or phrase to describe a situation during interview, I created a tools that suggest word in real time. All we have to do is that speaking into the mic, the live transcribe by Amazon will help transcribe those voice data and send back to us. Then I use a Facebook OPT-1.3b model to find the next highest chance occuring word so that it would act as the word suggestion based on the context is what we were saying. And those suggested word will be display in terms of word cloud with its size correspond to the weight. Later, all of the transcribe is saved under S3 storage",
        },
        "Beatcode": {
            "tech_skills": [
                "FastAPI",
                "RestfulAPI",
                "Docker",
                "WebSocket",
                "PostgreSQL",
                "PassLib",
                "SQLAlchemy",
                "CORS",
            ],
            "description": "Beatcode is the coding game that got its original idea from Tetris and Leetcode, where we will now live dual battle leetcode 1v1 versus another person from internet. My main duties were creating backend APIs, Websocket, setting up the Docker environment so that player could submit their code. I use PostGreSQL to store everything from players data, performance metrics, etc. Also I built OAuth so that everyone can login smoothly. Moreover, I doing a bit of frontend where I play around with Svelte and do the testing thing with PlayWright",
        },
        "FPT Software": {
            "tech_skills": ["AngularJS", "TypeScript", "JavaScript", "Observer"],
            "description": "Creating a functional webpage for Japanese Pharmacists Association. My tasks was to refined company's JavaScript SDK, to ensure it works with UI through multiple webpage and modals. I also create observer pattern that helps automate the 20,000 data binding from frontend to backend and vice versa, with high accuracy and consuming less time of coding. I also managed tasks and schedules in fast-paced environment, improving communication and collaboration using Agile-Scrum method",
        },
        "Avocademy (YC W22)": {
            "tech_skills": [
                "React",
                "SpringBoot",
                "OpenAI API",
                "Fire Crawler",
                "PuppeteerJS",
                "PlayWright",
                "SupaBase",
                "MongoDB",
                "Github",
                "CI/CD",
                "A/B Testing",
                "E2E testing",
                "Vercel",
            ],
            "description": "Developing an automated tailoring job application where student just has to pre-fill in information and everyday, the system will automatically apply to desired job for them. Jobs will be crawl on daily basis and user can pick their desired job that they want to apply then system will autofill and apply to the job. We also use openai api to help extract necessary information to display to user.",
        },
        "Viettel AI": {
            "tech_skills": [
                "Solr",
                "SBERT",
                "NLP",
                "Machine Learning",
                "Microsoft Graph RAG",
                "BM25",
            ],
            "description": "At Viettel AI, my main tasks were to doing research on how to develop a fully functional chatbot for Vietnamese people like the one that openAI has done with the world (chatgpt). I was working on creating the pipeline for searching system (first do fulltext search, after receiving the data, we could augmenting it by applying semantic search). After that, I was assigned to looking into the way to store and retrieve data using Microsoft Graph RAG",
        },
    }

    job_description = """
    3. Machine Learning Engineer (AI & Search Systems)
    Location: Remote / Hybrid
    Job Type: Full-time

    About the Role:
    We are hiring a Machine Learning Engineer to develop and optimize AI-driven solutions, including search retrieval systems and transformer-based models. You will work on RAG pipelines, NLP, and vector search optimization.

    Responsibilities:
    Build and fine-tune transformer-based models (BERT, GPT, T5) for AI applications.
    Develop search and retrieval pipelines using Elasticsearch, Meilisearch, Pinecone, and FAISS.
    Implement BM25 and hybrid search approaches for NLP applications.
    Optimize ML model performance and integrate with production environments.
    Preferred Qualifications:
    Experience with Hugging Face, spaCy, and knowledge graphs.
    Exposure to distributed processing using Kafka or RabbitMQ.
    Hands-on experience with multi-modal AI applications.
    """

    updated_resume = matcher.match_skills(resume_data, job_description)
    print(updated_resume)
