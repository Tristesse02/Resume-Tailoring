import json
from jinja2 import Template
from urllib.parse import urlparse


class LatexResumeBuilder:
    def __init__(self, template_path):
        """Initialize the ResumeTailor with a template JSON file."""
        with open(template_path, "r") as f:
            self.template = json.load(f)  # Load the template

    def update_template(
        self, output, profile_data, resume_data, university_data, **kwargs
    ):
        """
        Update the resume template with the provided AI-generated output.

        params:
        output: AI-generated output from deep_tailoring.py
        profile_data: Profile data (metadata) extracted from the front-end
        resume_data: Resume data (work experiences and personal project) extracted from the front-end
        university_data: University data (university, degree, GPA, etc.) extracted from the front-end
        """
        work_exp = {}

        # **Store AI-generated work experience & project descriptions**
        for tailored_experience in output["work_experiences"]:
            work_exp[tailored_experience["title"]] = tailored_experience["description"]

        for tailored_project in output["personal_projects"]:
            work_exp[tailored_project["title"]] = tailored_project["description"]

        # **Store untailored work experience & project descriptions**
        if "untailored_jobs" in kwargs:
            for key, value in kwargs["untailored_jobs"].items():
                work_exp[key] = value

        if "untailored_projects" in kwargs:
            for key, value in kwargs["untailored_projects"].items():
                work_exp[key] = value

        # [Issue #2.1] - If there exist the same title, then it would be bug lol

        # Extract an empty array work_experience from the temp_personal_info.json
        work_exp_field = self.template["work_experiences"]
        # print("buon the nho", resume_data)
        # Paste work_experiences into the temp_personal_info.json
        for experiences in resume_data["work_experiences"]:
            # TODO: Now we have to cope with the fact that there are experience
            # that we don't tailor and there are exp that we do actually tailor
            work_exp_field.append(
                {
                    "title": experiences["title"],
                    "position": experiences["position"],
                    "duration": experiences["duration"],
                    "location": experiences["location"],
                    "description": work_exp[experiences["title"]],
                }
            )

        # Extract an empty array personal_projects from the temp_personal_info.json
        personal_projects_field = self.template["personal_projects"]
        # Paste personal_projects into the temp_personal_info.json

        augmented_skill_obj = {}
        if "skill_augmented_resume_data" in kwargs:
            for projects in kwargs["skill_augmented_resume_data"]["resume_data"][
                "personal_projects"
            ]:
                augmented_skill_obj[projects["title"]] = projects["techStack"]

        for projects in resume_data["personal_projects"]:
            print("huh??", projects, flush=True)
            personal_projects_field.append(
                {
                    "title": projects["title"],
                    "techstack": (
                        projects["techStack"]
                        if projects["title"] not in augmented_skill_obj
                        else augmented_skill_obj[projects["title"]]
                    ),  # TODO: considering if augmented tech stack should be override (too much is not good!)
                    "description": work_exp[projects["title"]],
                }
            )

        # [Debug Purpose]
        # print(tailored_experience, flush=True)

        # LinkedIn and Github extraction
        linkedIn_url = urlparse(profile_data["linkedin"])
        linkedIn_none_url = linkedIn_url.netloc + linkedIn_url.path

        github_url = urlparse(profile_data["github"])
        github_non_url = github_url.netloc + github_url.path

        # **Update personal information**
        self.template["name"] = profile_data["name"]
        self.template["email"] = f"{{{profile_data['email']}}}"
        self.template["phone"] = profile_data["phone"]
        self.template["linkedin"] = f"{{{linkedIn_none_url}}}"
        self.template["linkedin_link"] = f"{{{profile_data['linkedin']}}}"
        self.template["github"] = f"{{{github_non_url}}}"
        self.template["github_link"] = f"{{{profile_data['github']}}}"

        # Technical Skills/Frameworks Showoff
        self.template["technical_skills"] = [
            f"Languages: {profile_data['languages']}",
            f"Libraries/Framework: {profile_data['frameworks']}",
        ]

        # University Data
        education_obj = self.template["educations"][0]
        education_obj["university"] = university_data["university"]
        education_obj["degree"] = university_data["degree"]
        education_obj["gpa"] = university_data["gpa"]
        education_obj["graduate"] = university_data["graduate"]
        education_obj["location"] = university_data["location"]
        education_obj["courses"].append(f"Courses: {university_data['courses']}")

        # [Debug Purpose]
        # print("ditmenooo", self.template, flush=True)

        return self.template  # Return the updated template

    def get_template(self):
        return self.template

    def save_to_file(self, output_path):
        """
        Save the updated resume template to a new JSON file.
        """
        with open(output_path, "w") as updated_file:
            json.dump(self.template, updated_file, indent=2)
        print(f"Resume updated and saved to {output_path}")

    def escape_latex(self, value):
        """Escape LaTeX special characters."""
        if isinstance(value, str):
            return (
                value.replace("%", r"\%")
                .replace("_", r"\_")
                .replace("&", r"\&")
                .replace("#", r"\#")
            )
        return value

    def recursive_escape(self, obj):
        """Recursively escape LaTeX characters in the JSON structure."""
        if isinstance(obj, dict):
            return {k: self.recursive_escape(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.recursive_escape(v) for v in obj]
        elif isinstance(obj, str):
            return self.escape_latex(obj)
        return obj

    def generate_latex(self, template_path, output_latex_path="output/output.tex"):
        """
        Generate a LaTeX file from the updated JSON template using Jinja2.
        """
        # **Escape LaTeX special characters**
        escaped_data = self.recursive_escape(self.template)
        print("thoi ditmenoroi", escaped_data, flush=True)

        # **Load the LaTeX template**
        with open(template_path, "r") as f:
            template = Template(f.read())

        # **Render the template with the escaped JSON data**
        rendered_latex = template.render(escaped_data)

        # **Write the output to a LaTeX file**
        with open(output_latex_path, "w") as f:
            f.write(rendered_latex)

        print(f"LaTeX file generated successfully at: {output_latex_path}")
