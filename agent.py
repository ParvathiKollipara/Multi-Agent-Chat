class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = []
import re

def respond(self, message, sender_name):
    self.memory.append((sender_name, message))

    # Auto detect math expressions anywhere in the message
    math_expr = re.findall(r"\d+\s*[\+\-\*\/]\s*\d+", message)
    if math_expr:
        expression = math_expr[0]
        result = calculator_tool(expression)
        response = f"Hi {sender_name}, the result of '{expression}' is {result}."
        self.memory.append((self.name, response))
        return response

    # Normal conversation logic
    recent_messages = self.memory[-4:]
    context_summary = ""
    if len(recent_messages) >= 2:
        context_summary = "Recent conversation: "
        for sender, msg in recent_messages:
            context_summary += f"[{sender}] said '{msg}'. "
    elif len(recent_messages) == 1:
        context_summary = f"You said '{recent_messages[0][1]}'"

    response = (
        f"Hi {sender_name}! {context_summary} "
        f"Regarding your message '{message}', what are your thoughts?"
    )

    self.memory.append((self.name, response))
    return response
