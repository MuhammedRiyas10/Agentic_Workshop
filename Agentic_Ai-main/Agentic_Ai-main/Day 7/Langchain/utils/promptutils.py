def format_prompt(template: str, **kwargs) -> str:
    """
    Replace placeholders in the template with values passed as kwargs.
    Example: format_prompt(template, text="abc") replaces {text}
    """
    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", value)
    return template
