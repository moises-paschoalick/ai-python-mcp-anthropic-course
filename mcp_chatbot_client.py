from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stio connection
server_params = StdioServerParameters(
    command="uv", # Executable
    args=["run example_server.py"], # Command line arguments
    env=None, # Optional enviroment variabels
)

async def run():
    # Launch the server as a subprocess & returns the read and write streams
    # read: the stream that the client will use to read msgs from the server
    # write: the stream that client will use to write msgs to the server
    async with stdio_client(server_params) as (read, write):
        # the client sesssio is used to initiate the connection
        # and send requests to server
        async with ClientSession(read, write) as session:
            # Initialize the connection (1:1 connection with the server)
            # and send request to server
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            
            # will call the chat_loop here
            # ...
            
            # Call a tool: this will be in the process_query method
            result = await session.call_tool("tool-name", argument={"arg1":"value"})
            
if __name__ == "__main__":
    asyncio.run(run())