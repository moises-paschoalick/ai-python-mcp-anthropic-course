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

## Old chat (use process_query)
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
        
def process_query(query):
    
    messages = [{'role': 'user', 'content': query}]
    
    response = client.messages.create(
        max_tokens=2024,
        model="claude-3-haiku-20240307",
        tools=TOOLS,
        messages=messages
    )
    
    process_query_flag = True
    
    while process_query_flag:
        
        assistant_content = []
        
        for content in response.content:
            
            # Normal text response
            if content.type == 'text':
                print(f"\nClaude: {content.text}")
                assistant_content.append(content)
                
                # If onlyuu text -> finish
                if len(response.content) == 1:
                    process_query_flag = False
            
            # Tool call
            elif content.type == 'tool_use':
                
                assistant_content.append(content)
                
                # save assitant decision (important for MCP)
                messages.append({
                    'role': 'assistant',
                    'content': assistant_content
                })
                
                tool_id = content.id
                tool_args = content.input
                tool_name = content.name
                
                print(f"\n Calling tool {tool_name} with arg {tool_args}")
                
                result = execute_tool(tool_name, tool_args)
                
                # Send toll result back to Claude
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result
                        }
                    ]
                })

                # Call Claude again
                response = client.messages.create(
                    max_tokens=2024,
                    model="claude-3-haiku-20240307",
                    tools=TOOLS,
                    messages=messages
                )

                if len(response.content) == 1 and response.content[0].type == "text":
                    print(f"\nClaude: {response.content[0].text}")
                    process_query_flag = False


def chat_loop():
    print("Type your queries or 'quit' to exit.")
    while True:
        try:
            query = input("\nQuery: ").strip()
            if query.lower() == 'quit':
                break
    
            process_query(query)
            print("\n")
        except Exception as e:
            print(f"\nError: {str(e)}")

c = chat_loop();

#if __name__ == '__main__':
#    chat()                

