
import ast
import operator
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# Initialize the Groq language model
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Tool 1: Web Search
search_tool = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the web for information about a topic."""
    try:
        return search_tool.run(query)
    except Exception as error:
        return f"Web search failed: {error}"


# Tool 2: Python Calculator
@tool
def calculator(expression: str) -> str:
    """Calculate basic mathematical expressions.
    Supports numbers and +, -, *, /, //, %, and ** operators.
    """
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = calculate(node.left)
            right = calculate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent is too large.")

            return allowed_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](calculate(node.operand))

        raise ValueError("Unsupported mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = calculate(tree.body)
        return str(result)
    except Exception as error:
        return f"Calculation error: {error}"


# Tool 3: Local File Reader
@tool
def read_local_file(filename: str) -> str:
    """Read a text file from this project's folder.
    Use sample.txt when asked about the sample project information.
    """
    project_folder = Path(__file__).resolve().parent
    allowed_file = (project_folder / "sample.txt").resolve()

    requested_file = Path(filename).name.lower()

    if requested_file != "sample.txt":
        return "Access denied. Only sample.txt can be read."

    try:
        return allowed_file.read_text(encoding="utf-8")
    except Exception as error:
        return f"File reading failed: {error}"


# Create the autonomous tool-calling agent
tools = [web_search, calculator, read_local_file]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful multi-tool AI agent. "
        "Use web_search for current or online information. "
        "Use calculator for mathematical calculations. "
        "Use read_local_file to answer questions about sample.txt. "
        "Choose tools when they are useful, observe their results, "
        "and continue until you can answer the user's question. "
        "Never claim you used a tool if you did not use it. "
        "Explain the final answer clearly."
    ),
)


# Console application
def main():
    print("\n" + "=" * 55)
    print("       MULTI-TOOL AUTONOMOUS AI AGENT")
    print("=" * 55)
    print("Tools: Web Search | Calculator | Local File Reader")
    print("Type 'exit' to close the application.")
    print("-" * 55)

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Agent: Goodbye!")
            break

        if not question:
            continue

        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": question}]}
            )

            final_message = result["messages"][-1]
            print(f"\nAgent: {final_message.content}")

        except Exception as error:
            print(f"\nAgent error: {error}")


if __name__ == "__main__":
    main()
