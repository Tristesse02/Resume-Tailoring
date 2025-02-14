import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
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
        "description": "",
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
        "description": "",
    },
    "FPT Software": {
        "tech_skills": ["AngularJS", "TypeScript", "JavaScript", "Observer"],
        "description": "",
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
            "Claude",
        ],
        "description": "",
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
        "description": "",
    },
}

systemMessage = f"""
You are a helpful assistant that enhances my resume by identifying and adding relevant technical skills.

You will be given `resume_data`, a dictionary where:
- Keys are job titles (do not modify these).
- Values are lists of technical skills.

In the user message, you will receive a job description that contains important technical skill.

### Your task:
1. Extract key technical skills from the job description.
2. Prioritize the most important skills (frequent or critical to the role).
3. Add up to **4-5** new skills per experience/project.
4. Append new skills only if a related skill already exists in an array.
5. Avoid duplicates and ensure logical relevance. Example mappings:
	- ChatGPT → Claude, DeepSeek
   	- Java → Kotlin
   	- Python → Flask, FastAPI, Django
   	- React → React Native, Vue.js, AngularJS
   	- PostgreSQL → MySQL, SQL Server
   	- AWS → Azure, GCP
   	- Docker → Kubernetes
   	- TensorFlow → PyTorch
   	- NLP → Hugging Face, spaCy
    
### Output:
Return the updated `resume_data` as a JSON object while preserving its structure.
Please also explain why you choose to add these skills briefly.

### Provided Resume Data:
{resume_data}
"""

job_description = """
Job Title: Full-Stack Engineer (AI & Cloud Services)

Location: Remote / Hybrid
Job Type: Full-time

About the Role:
We are looking for a Full-Stack Engineer with experience in building scalable web applications, cloud-based services, and AI-driven solutions. You will work across the stack, leveraging modern frameworks and cloud infrastructure to build robust and efficient systems. This role involves designing APIs, optimizing databases, integrating machine learning models, and ensuring high performance through CI/CD pipelines and testing automation.

Responsibilities:
Develop and maintain serverless applications using AWS services (Lambda, API Gateway, S3, DynamoDB, Cognito).
Design and implement RESTful APIs with frameworks such as FastAPI, Flask, or Express.js.
Work with real-time data processing using WebSockets and event-driven architectures.
Build interactive front-end applications using modern JavaScript frameworks like React, Next.js, and D3.js for data visualization.
Optimize full-stack applications with GraphQL, gRPC, and efficient database indexing techniques (PostgreSQL, NoSQL, Redis).
Implement search and retrieval solutions using tools like Elasticsearch, Meilisearch, and Vector DBs (Pinecone, FAISS).
Integrate machine learning solutions with transformer-based models (BERT, GPT, T5) and fine-tune retrieval models.
Automate deployments with Docker, Kubernetes, Terraform, and AWS SAM.
Conduct unit, integration, and end-to-end testing (Jest, Cypress, Playwright) to ensure reliability.
Utilize CI/CD tools (GitHub Actions, GitLab CI, Jenkins) to streamline software delivery.
Preferred Qualifications:
Experience with serverless computing and containerized deployments.
Knowledge of authentication and security best practices, including JWT, OAuth, and IAM policies.
Familiarity with A/B testing methodologies for optimizing user experiences.
Hands-on experience with data crawling, scraping, and automation tools (Scrapy, Selenium, Puppeteer).
Strong understanding of NLP, knowledge graphs, and retrieval-augmented generation (RAG).
Ability to work with multi-cloud environments (AWS, GCP, Azure) and optimize cloud costs.
Strong analytical and problem-solving skills with an interest in AI-driven applications.
Nice to Have:
Experience working with LLMs, RAG pipelines, and hybrid search approaches (BM25 + Embeddings).
Exposure to message brokers (RabbitMQ, Kafka) for distributed processing.
Hands-on experience with SupaBase, Firebase, or other backend-as-a-service solutions.
Knowledge of edge computing and CDN optimization for performance tuning.
Why Join Us?
Work on cutting-edge AI and cloud-based technologies.
Opportunity to contribute to open-source projects and research-driven AI initiatives.
Collaborative team environment with mentorship and professional growth.
Flexible work environment with hybrid and remote options.
"""

user_message = f"Job Description:\n{job_description}"

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": systemMessage},
        {"role": "user", "content": user_message},
    ],
    model="gpt-4o",
)

output_content = chat_completion.choices[0].message.content.strip()
print("minhdz", output_content, "\n")


def extract_json(text):
    """Extracts valid JSON from an OpenAI response (handles markdown and extra text)."""
    match = re.search(r"```json\s*([\s\S]+?)\s*```", text)  # Look for JSON code block
    json_str = match.group(1) if match else text  # If no markdown, assume pure JSON
    try:
        return json.loads(json_str)  # Validate JSON
    except json.JSONDecodeError as e:
        print("Error: Invalid JSON output:", e)
        return None  # Handle error case


parsed_json = extract_json(output_content)

print(parsed_json)
