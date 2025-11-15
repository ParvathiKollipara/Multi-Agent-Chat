import ast
import operator
import google.generativeai as genai
import streamlit as st

# ---- Configure Google Gemini API ----
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: GEMINI_API_KEY missing in Streamlit Secrets!")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

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
        if not message.strip():
            return "Please enter a message."

        self.memory.append((sender_name, message))

        # --- Calculation command ---
        if message.lower().startswith("calc:"):
            expr = message[5:].strip()
            result = calculator_tool(expr)
            return f"The result of '{expr}' is {result}."

        # --- AI response using Gemini ---
        context = "\n".join([f"{s}: {m}" for s, m in self.memory[-5:]])

        prompt = f"""
You are {self.name}.
Recent conversation:
{context}

User message: {message}

Reply politely, clearly, and briefly.
"""

        try:
            response = model.generate_content(prompt)

            # handle NONE issues
            if not hasattr(response, "text") or response.text is None:
                return "⚠️ Gemini returned no output."

            return response.text

        except Exception as e:
            return f"⚠️ Gemini Error: {str(e)}"
