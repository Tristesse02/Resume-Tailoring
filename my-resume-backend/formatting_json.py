import json
import copy


class FormattingJSON:
    def __init__(self, input_json):
        """
        Initializes the FormattingJSON class with input JSON data.
        """
        # TODO: Code fixing for consistency:
        # The code is now all over the place with self.new_obj containing so many forms!!
        self.input_json = input_json
        self.new_obj = copy.deepcopy(input_json)
        self.extracted_need_tailored_fields = copy.deepcopy(input_json)
        self.augmented_skill_input_json = copy.deepcopy(input_json)

    def get_resume_data(self):
        """
        Returns the resume data from the input JSON.
        """
        return self.input_json["resume_data"]

    def get_job_description(self):
        """
        Returns the job description data from the input JSON.
        """
        return self.input_json["job_description"]

    def get_profile_data(self):
        """
        Returns the profile data from the input JSON.
        """
        return self.input_json["profile_data"]

    def get_university_data(self):
        """
        Returns the university data from the input JSON.
        """
        return self.input_json["university_data"]

    def get_resume_need_tailor_data(self):
        """
        Returns the extracted fields that need tailoring from the input JSON.
        """
        return self.extracted_need_tailored_fields["resume_data"]

    def get_extracted_need_tailored_fields(self):
        """
        Returns the extracted fields that need tailoring from the input JSON.
        """
        return self.extracted_need_tailored_fields

    def get_augmented_skill_input_json(self):
        """
        Returns the augmented skill input JSON data.
        """
        return self.augmented_skill_input_json

    def get_augmented_skill_input_json_data(self):
        """
        Returns the augmented skill input JSON data.
        """
        return self.augmented_skill_input_json["resume_data"]

    def set_augmented_skill_input_json(self, data):
        """
        Sets the augmented skill input JSON data.
        """
        self.augmented_skill_input_json = data

    def update_need_tailored_fields(self, field, data):
        self.extracted_need_tailored_fields["resume_data"][field] = data

    def format_augment_skill(self):
        """
        Formats either personal projects or work experiences by restructuring descriptions.
        """
        formatted_augment_skill = {}

        # print(self.get_resume_need_tailor_data())
        for exp_obj in self.get_resume_need_tailor_data()[
            "work_experiences"
        ]:  # TODO: Replace this to get_resume_data to improve readability
            formatted_augment_skill[exp_obj["title"]] = {}
            formatted_augment_skill[exp_obj["title"]]["tech_skills"] = exp_obj[
                "techStack"
            ]
            formatted_augment_skill[exp_obj["title"]]["description"] = exp_obj[
                "description"
            ]

        # print("till this point eh?", flush=True)
        for exp_obj in self.get_resume_need_tailor_data()["personal_projects"]:
            formatted_augment_skill[exp_obj["title"]] = {}
            formatted_augment_skill[exp_obj["title"]]["tech_skills"] = exp_obj[
                "techStack"
            ]
            formatted_augment_skill[exp_obj["title"]]["description"] = exp_obj[
                "description"
            ]
        return formatted_augment_skill

    def format_untailored_bullet_points(self, arr):
        for key, value in arr.items():
            # Remove the bullet points from the string
            arr[key] = self.remove_format_bullet_points(value)

        return arr

    def remove_format_bullet_points(self, s):
        """
        Removes bullet points from a string.
        """
        return [line.strip("• ").strip() for line in s.splitlines() if line.strip()]

    def augment_skill_to_input_json(self, formatted_augment_skill):
        """
        Augments the skill to the input JSON data
        After the run of this function, the changes will be made on self.augmented_skill_input_json

        return: None
        """

        # augmented_skill_input_json now only contains the tailored data!
        for personal_project in self.get_augmented_skill_input_json_data()[
            "personal_projects"
        ]:
            personal_project["techStack"] = formatted_augment_skill[
                personal_project["title"]
            ]["tech_skills"]

        for work_experience in self.get_augmented_skill_input_json_data()[
            "work_experiences"
        ]:
            work_experience["techStack"] = formatted_augment_skill[
                work_experience["title"]
            ]["tech_skills"]

    def format_experiences(self, key):
        """
        Formats either personal projects or work experiences by restructuring descriptions.
        """
        formatted_list = []
        # Now the augmented skill is properly updated and ready to be tailored in deep tailoring
        # print(self.augmented_skill_input_json, key, flush=True)
        for exp_obj in self.get_augmented_skill_input_json_data()[key]:
            obj_pass_gpt = {
                "title": exp_obj["title"],
                "description": (
                    # TODO: This current code mean that we haven't use the augmented skill yet??
                    f"{exp_obj['type']};Tech Stack: {', '.join(exp_obj['techStack'])};"
                    f"Description: {exp_obj['description']};"
                    f"Quantifiable Metrics: {exp_obj['quantifiableMetrics']};"
                    f"Bullet Points: {exp_obj['bulletPoints']}"
                ),
            }
            formatted_list.append(obj_pass_gpt)
        self.new_obj["resume_data"][key] = formatted_list

    def format_resume_data(self):
        """
        Formats both personal projects and work experiences in the resume data.
        """
        self.format_experiences("personal_projects")
        print("pass 1", flush=True)
        self.format_experiences("work_experiences")
        print("pass 2", flush=True)

        # TODO: Classify between jobs needed to be tailored by gpt and job that doesn't need to be tailored

    def get_formatted_json(self):
        """
        Returns the formatted JSON object.
        """
        json_string = json.dumps(self.new_obj, ensure_ascii=False, indent=4)
        return json.loads(json_string)

    def extract_fields_need_tailoring(self):
        """
        Extracts fields that need tailoring from the resume data.

        Returns [list] the jobs that no need tailoring.
        """
        jobs_need_tailoring = []
        project_need_tailoring = []

        jobs_no_need_tailoring = {}
        project_no_need_tailoring = {}

        for exp_obj in self.get_resume_data()["work_experiences"]:
            if exp_obj["isBulletDescription"]:
                jobs_need_tailoring.append(exp_obj)
            else:
                jobs_no_need_tailoring[exp_obj["title"]] = exp_obj["bulletDescription"]

        for exp_obj in self.get_resume_data()["personal_projects"]:
            if exp_obj["isBulletDescription"]:
                project_need_tailoring.append(exp_obj)
            else:
                project_no_need_tailoring[exp_obj["title"]] = exp_obj[
                    "bulletDescription"
                ]

        # self.get_resume_need_tailor_data()["work_experiences"] = jobs_need_tailoring
        # self.get_resume_need_tailor_data()["personal_projects"] = project_need_tailoring

        self.update_need_tailored_fields("work_experiences", jobs_need_tailoring)
        self.update_need_tailored_fields("personal_projects", project_need_tailoring)

        self.set_augmented_skill_input_json(self.get_extracted_need_tailored_fields())

        def get_untailored(field_type):
            if field_type == "jobs":
                return self.format_untailored_bullet_points(jobs_no_need_tailoring)
            elif field_type == "projects":
                # print("ducdz a", project_no_need_tailoring)
                return self.format_untailored_bullet_points(project_no_need_tailoring)
            else:
                raise ValueError("field_type must be either 'jobs' or 'projects'")

        return get_untailored


# Debugging purpose
if __name__ == "__main__":
    input_json = {
        "resume_data": {
            "personal_projects": [
                {
                    "title": "CloudCueAI",
                    "type": "Project",
                    "techStack": [
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
                    "quantifiableMetrics": "500-1000 daily visits webpage, 350+ UIs and modals, 20,000 data entries",
                    "bulletPoints": "4",
                },
                {
                    "title": "Beatcode",
                    "type": "Project",
                    "techStack": [
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
                    "quantifiableMetrics": "500+ players during beta, 1,000+ concurrent users, 300 unique account created in first 12 hours",
                    "bulletPoints": "4",
                },
            ],
            "work_experiences": [
                {
                    "title": "FPT Software",
                    "type": "Intern",
                    "techStack": ["AngularJS", "TypeScript", "JavaScript", "Observer"],
                    "description": "Creating a functional webpage for Japanese Pharmacists Association. My tasks was to refined company's JavaScript SDK, to ensure it works with UI through multiple webpage and modals. I also create observer pattern that helps automate the 20,000 data binding from frontend to backend and vice versa, with high accuracy and consuming less time of coding. I also managed tasks and schedules in fast-paced environment, improving communication and collaboration using Agile-Scrum method",
                    "quantifiableMetrics": "500-1000 daily visits webpage, 350+ UIs and modals, 20,000 data entries",
                    "bulletPoints": "4",
                },
                {
                    "title": "Avocademy (YC W22)",
                    "type": "Intern",
                    "techStack": [
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
                    "description": "Developing an automated tailoring job application where student just has to pre-fill in information and everyday, the system will automatically apply to desired job for them. Jobs will be crawl on daily basis and user can pick their desired job that they want to apply then system will autofill and apply to the job. We also use openai api to help extract necessary information to display to user.",
                    "quantifiableMetrics": "750+ daily job postings; 70000+ entries in database",
                    "bulletPoints": "5",
                },
                {
                    "title": "Viettel AI",
                    "type": "Intern",
                    "techStack": [
                        "Solr",
                        "SBERT",
                        "NLP",
                        "Machine Learning",
                        "Microsoft Graph RAG",
                        "BM25",
                    ],
                    "description": "At Viettel AI, my main tasks were to doing research on how to develop a fully functional chatbot for Vietnamese people like the one that openAI has done with the world (chatgpt). I was working on creating the pipeline for searching system (first do fulltext search, after receiving the data, we could augmenting it by applying semantic search). After that, I was assigned to looking into the way to store and retrieve data using Microsoft Graph RAG",
                    "quantifiableMetrics": "",
                    "bulletPoints": "2",
                },
            ],
        },
        "job_description": "1. Cloud Engineer (Serverless & DevOps)\nLocation: Remote / Hybrid\nJob Type: Full-time\n\nAbout the Role:\nWe are seeking a Cloud Engineer specializing in serverless architectures and DevOps automation. You will design and maintain scalable cloud infrastructure, optimize deployments, and enhance system reliability through automation and CI/CD best practices.\n\nResponsibilities:\nDesign and maintain serverless applications using AWS Lambda, API Gateway, S3, DynamoDB, and Cognito.\nAutomate infrastructure management using Terraform, AWS SAM, and Kubernetes.\nOptimize CI/CD pipelines with GitHub Actions, GitLab CI, and Jenkins.\nEnhance security and authentication using JWT, OAuth, and IAM policies.\nImplement monitoring and observability with CloudWatch and logging solutions.\nPreferred Qualifications:\nExperience with multi-cloud environments (AWS, GCP, Azure).\nStrong knowledge of containerized deployments and orchestration.\nExposure to CDN optimization and edge computing.\n",
    }

    formattingJSON = FormattingJSON(input_json)
    # print(formattingJSON.format_augment_skill())
