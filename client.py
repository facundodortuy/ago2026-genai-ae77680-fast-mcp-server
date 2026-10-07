import asyncio

from fastmcp import Client

from config import get_config

config = get_config()

client = Client(
    config.mcp.base_url,
    auth=config.mcp.api_key,
)


async def main():
    async with client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        print("Tools:", [t.name for t in tools])
        print("Resources:", [r.uri for r in resources])
        print("Prompts:", [p.name for p in prompts])

        result = await client.call_tool("greet", {"name": "Juan Perez"})
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())

