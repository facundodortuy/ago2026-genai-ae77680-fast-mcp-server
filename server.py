from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

@mcp.tool
def sum_two_numbers(a: int, b: int) -> int:
    """Suma dos numeros enteros."""
    return a + b

if __name__ == "__main__":
    mcp.run()