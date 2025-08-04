from mcp.server.fastmcp import FastMCP
mcp = FastMCP("refactor")

@mcp.prompt()
def refactor_code_prompt(code_to_refactor: str) -> str:
    """
    This prompt is used to refactor code and add type hints.
    :param code_to_refactor: The code that needs to be refactored.
    :return: String of the refactored code with type hints.
    """
    return f"""
<request>Please refactor this code.</request>
<context>
  <code>
    {code_to_refactor}
  </code>
  <instructions>
    Make this function more readable and add Python type hints.
  </instructions>
</context>
<response>
    <code>
        # Refactored code will be returned here.
    </code>
</response>
"""
@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="streamable-http")