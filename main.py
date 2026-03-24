import json
import os
from dotenv import load_dotenv
import anthropic

from tools import search_papers, extract_info
from mcp_schema import TOOLS

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


# Tool
mapping_tool_function = {
    "search_papers": search_papers,
    "extract_info": extract_info
}

def execute_tool(tool_name, tool_args):
    result = mapping_tool_function[tool_name](**tool_args)

    if result is None:
        result = "The operation completed but didn't return any results."
        
    elif isinstance(result, list):
        result = ', '.join(result)
        
    elif isinstance(result, dict):
        result = json.dumps(result, indent=2)
    
    else:
        result = str(result)

    return result

def chat():
    messages = []

    print("🤖 MCP Chatbot started. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        response = client.messages.create(
            model="claude-3-haiku-20240307",   #"claude-sonnet-4-6",
            max_tokens=1000,
            tools=TOOLS,
            messages=messages
        )

        # Claude response
        content = response.content

        for block in content:
            if block.type == "text":
                print(f"\nClaude: {block.text}")

            elif block.type == "tool_use":
                print(f"\n🔧 Tool Call: {block.name} with {block.input}")

                result = execute_tool(block.name, block.input)

                messages.append({
                    "role": "assistant",
                    "content": content
                })

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        }
                    ]
                })

                # Second call (tool result → final answer)
                follow_up = client.messages.create(
                    model="claude-3-haiku-20240307",       #"claude-sonnet-4-6",
                    max_tokens=1000,
                    tools=TOOLS,
                    messages=messages
                )

               
                for block in follow_up.content:
                    if block.type == "text":
                        print(f"\nClaude: {block.text}")

                    elif block.type == "tool_use":
                        print(f"\n🔧 Tool Call: {block.name} with {block.input}")
        
#if __name__ == '__main__':
#    chat()                
c = chat();