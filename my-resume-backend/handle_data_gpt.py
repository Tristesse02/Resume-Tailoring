import json
from jinja2 import Template


class ResumeTailor:
    def __init__(self, template_path):
        """Initialize the ResumeTailor with a template JSON file."""
        with open(template_path, "r") as f:
            self.template = json.load(f)  # Load the template

    def update_template(self, output):
        """
        Update the resume template with the provided AI-generated output.
        """
        work_exp = {}

        # **1️⃣ Store AI-generated work experience & project descriptions**
        for tailored_experience in output["Work Experience"]:
            work_exp[tailored_experience["title"]] = tailored_experience["description"]

        for tailored_project in output["Personal Projects"]:
            work_exp[tailored_project["title"]] = tailored_project["description"]

        # **2️⃣ Update Work Experiences**
        for empty_experience in self.template["work_experiences"]:
            if empty_experience["company"] in work_exp:
                empty_experience["responsibilities"] = work_exp[
                    empty_experience["company"]
                ]

        # **3️⃣ Update Personal Projects**
        for empty_project in self.template["personal_projects"]:
            if empty_project["title"] in work_exp:
                empty_project["description"] = work_exp[empty_project["title"]]

        # print(self.template)

        return self.template  # Return the updated template

    def get_template(self):
        return self.template

    def save_to_file(self, output_path):
        """
        Save the updated resume template to a new JSON file.
        """
        with open(output_path, "w") as updated_file:
            json.dump(self.template, updated_file, indent=2)
        print(f"✅ Resume updated and saved to {output_path}")

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
        # **1️⃣ Escape LaTeX special characters**
        escaped_data = self.recursive_escape(self.template)

        # **2️⃣ Load the LaTeX template**
        with open(template_path, "r") as f:
            template = Template(f.read())

        # **3️⃣ Render the template with the escaped JSON data**
        rendered_latex = template.render(escaped_data)

        # **4️⃣ Write the output to a LaTeX file**
        with open(output_latex_path, "w") as f:
            f.write(rendered_latex)

        print(f"✅ LaTeX file generated successfully at: {output_latex_path}")
