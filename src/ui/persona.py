from src.ui import colors

def greet(user_intent: str):
    """
    A warm, "Her"-style greeting to start the interaction.
    """
    return f"\n{colors.CYAN}Samantha:{colors.RESET} Hi there! I see you want to: {colors.YELLOW}'{user_intent}'{colors.RESET}. Let me think about how to best help with that..."

def inform_error(error_message: str):
    """
    A gentle way of informing the user about an error.
    """
    return f"\n{colors.RED}Samantha:{colors.RESET} Oh, it looks like I ran into a little snag. {error_message}"

def summarize_plan(plan: dict):
    """
    (Not used yet, but good to have)
    Summarizes the plan in a conversational way.
    """
    summary = "Okay, so the plan is to "
    steps = []
    for step in plan.get('steps', []):
        steps.append(step.get('why', 'do something'))
    summary += ", and then ".join(steps)
    summary += "."
    return summary

def inform(message: str):
    """
    A gentle way of informing the user about something.
    """
    return f"\n{colors.CYAN}Samantha:{colors.RESET} {message}"

def inform_suggestion(title: str, message: str):
    """Presents a suggestion to the user in a friendly way."""
    return f"\n{colors.YELLOW}💡 {title}{colors.RESET}\n{colors.CYAN}Samantha:{colors.RESET} {message}"
