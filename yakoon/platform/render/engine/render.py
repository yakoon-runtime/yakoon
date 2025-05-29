from yakoon.platform.render.engine.context import RenderContext
from yakoon.platform.render.engine.runtime import render_template_for
from yakoon.platform.render.engine.section import RenderSection


def render_section(ctx: RenderContext, key: str, **data) -> str:
    """
    Renders a specific section of a command template with optional data.

    This is a shorthand for passing a RenderSection object manually,
    useful for compact calls when the section is known.

    Args:
        ctx (RenderContext): The context specifying template path and language.
        key (str): The section key to render (e.g. 'success', 'error').
        **data: Optional keyword arguments passed to the template.

    Returns:
        str: The rendered template section output.
    """
    section = RenderSection(key, data)
    return render_template_for(ctx, section)