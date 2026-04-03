from pathlib import Path
from typing import Any
from jinja2 import Template

BASE_DIR = Path(__file__).parent / "email-templates" / "build"

def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_path = BASE_DIR / template_name

    template_str =template_path.read_text(encoding="utf-8")
    html_content = Template(template_str).render(context)

    return html_content