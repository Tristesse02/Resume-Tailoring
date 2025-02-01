import json
from jinja2 import Template


def escape_latex(value):
    """Escape LaTeX special characters."""
    if isinstance(value, str):
        return (
            value.replace("%", r"\%")
            .replace("_", r"\_")
            .replace("&", r"\&")
            .replace("#", r"\#")
        )
    return value


def recursive_escape(obj):
    if isinstance(obj, dict):
        return {k: recursive_escape(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_escape(v) for v in obj]
    elif isinstance(obj, str):
        return escape_latex(obj)
    return obj


# Load the JSON file
with open("personalData.json") as f: # TODO: Fix this one
    data = json.load(f)

data = recursive_escape(data)

# Load the LaTeX template
with open("templateResume.j2") as f:
    template = Template(f.read())

rendered_latex = template.render(data)

# Write the output to a new LaTeX file
with open("output.tex", "w") as f:
    f.write(rendered_latex)

print("LaTeX file generated successfully at: output.tex")
