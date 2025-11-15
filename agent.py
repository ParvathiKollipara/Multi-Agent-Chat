import ast
import operator
import google.generativeai as genai

# ---- Configure Google Gemini API ----
genai.configure(api_key="YOUR_API_KEY_HERE")

gemini = genai.GenerativeModel("gemini-1.5-flash")


# ---- Tool: Safe calculator ----
def calculator_tool(expression):
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](eval_expr(node.operand))
        else:
            raise ValueError("Unsupported expression")

    try:
        node = ast.parse(expression, mode='eval').body
        return eval_expr(node)
    except Exception as e:
        return f"Error in calculation: {e}"


# ---- Agent Class Powered by Gemini ----
class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = []

    def respond(self, message, sender_name):
        self.memory.append((sender_name, message))

        # --- Check for calculations ---
        if message.lower().startswith("calc:"):
            expr = message[5:].strip()
            result = calculator_tool(expr)
            reply = f"The result of '{expr}' is {result}."
            return reply

        # --- AI response using Google Gemini ---
        context = "\n".join([f"{s}: {m}" for s, m in self.memory[-5:]])

        prompt = f"""
        You are {self.name}.
        Conversation history:
        {context}

        User message: {message}
        Respond politely and clearly.
        """

        gemini_reply = gemini.generate_content(prompt).text
        return gemini_reply
