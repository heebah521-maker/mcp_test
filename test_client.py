import asyncio
from fastmcp import Client


async def main():
    async with Client("student_server.py") as client:
        tools = await client.list_tools()
        print("AVAILABLE TOOLS:")
        for tool in tools:
            print("-", tool.name, ":", tool.description)

        result = await client.call_tool("get_student_attendance", {"student_id": 101})
        print("\nTOOL RESULT:", result.data)


asyncio.run(main())