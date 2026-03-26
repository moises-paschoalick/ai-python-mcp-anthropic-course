import json
from typing import List
from mcp.server.fastmcp import FastMCP

from tools import search_papers as search_papers_impl
from tools import extract_info as extract_info_impl

# Initialize FastMCP server
mcp = FastMCP("research")

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    """
    return search_papers_impl(topic=topic, max_results=max_results)


@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for papers on arXiv based on a topic and store their information.
    """
    result = extract_info_impl(paper_id)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")