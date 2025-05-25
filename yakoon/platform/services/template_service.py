import markdown
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT_DIR = Path(__file__).resolve().parents[2]  # geht nach yakoon/
TEMPLATE_DIR = ROOT_DIR / "solution" / "templates"
if not (TEMPLATE_DIR).exists():
    raise ValueError(f"Template directory found: {TEMPLATE_DIR}")
    

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=False, # wir wollen Markdown, nicht HTML escapen
    trim_blocks=True,
    lstrip_blocks=True
)

def render(template_name: str, context: dict) -> str:
    """
    Renders a named template using Jinja2 and the given context.
    """
    try:
        template = env.get_template(template_name)
        return template.render(**context)
    except Exception as e:
        return f"⚠ Template error: {e}"

def render_markdown(template_name: str, context: dict) -> str:
    """
    Renders a named template using Jinja2 and and the given context.
    + markdown
    """
    md_output = render(template_name, context)
    html_output = markdown.markdown(md_output)
    return html_output