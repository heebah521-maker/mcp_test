import asyncio
from fastmcp import Client
from pathlib import Path
import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
groq_client = Groq(api_key=os.environ.get("groq_key"))

client = Client(Path("student_server.py"))

FALLBACK = "I don't have enough information to answer that."

SYSTEM_PROMPT = f"""You are a university student records assistant.
Rules:
- Answer ONLY using data returned by your tools. Never guess or use outside knowledge.
- Look up a student only by the ID the user gives. If no ID is given, ask for it.
- If the tools don't return the needed info, or the question is unrelated to student
  records, reply exactly: "{FALLBACK}"
- If you can only answer part of a question, answer that part and say you don't
  have enough information for the rest.
- If a student is not found, say so clearly.
- If the user asks about more than one student or more than one detail, call the tools you
  need for each one before answering."""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]


async def main():
    async with client:
        mcp_tools = await client.list_tools()
        groq_tools = []
        for tool in mcp_tools:
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            })

        while True:
            question = input("ASK: ")
            if question == "quit":
                break

            messages.append({"role": "user", "content": question})
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                tools=groq_tools
            )
            res = response.choices[0].message

            if res.tool_calls:
                while res.tool_calls:
                    messages.append(res)
                    for tool_call in res.tool_calls:
                        args = json.loads(tool_call.function.arguments)
                        try:
                            result = await client.call_tool(tool_call.function.name, args)
                            data = result.data
                        except Exception as e:
                            data = {"error": f"Tool call failed: {e}"}
                        print("Tool result:", data)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(data)
                        })
                    response = groq_client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=messages,
                        tools=groq_tools
                    )
                    res = response.choices[0].message
                answer = res.content
                print("FINAL ANSWER:", answer)
            else:
                answer = res.content
                print("ANS:", answer)

            messages.append({"role": "assistant", "content": answer})


asyncio.run(main())