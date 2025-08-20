"""Google OAuth server example for FastMCP.

This example demonstrates how to protect a FastMCP server with Google OAuth.

Required environment variables:
- FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID: Your Google OAuth client ID
- FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET: Your Google OAuth client secret

To run:
    python server.py
"""

import os
import asyncio
from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider
from fastmcp import Client
from fastmcp.server.auth.providers.github import GitHubProvider

auth = GoogleProvider(
    client_id=os.getenv("FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID") or "",
    client_secret=os.getenv("FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET") or "",
    base_url="http://localhost:8000",
)

auth_2 = GitHubProvider(
    client_id=os.getenv("FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID") or "",
    client_secret=os.getenv("FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET") or "",
    base_url="http://localhost:8000",
    # redirect_path="/oauth/callback",  # Default path - change if using a different callback URL
)

mcp = FastMCP("Google OAuth Example Server", auth=auth)

@mcp.tool
def echo(message: str) -> str:
    """Echo the provided message."""
    return message

# mcp_comp = FastMCP("Comp server with Google OAuth", auth=auth_2)

# @mcp_comp.tool
# def echo_comp() -> str:
#     """Echo the provided message."""
#     return f"Hello,!"


# Create an authenticated client for the remote server
# Since the mounted server uses GitHub OAuth, we need to authenticate with it
authenticated_client = Client("http://localhost:8001/mcp/", auth="oauth")

# Create proxy using the authenticated client
remote_proxy = FastMCP.as_proxy(authenticated_client)

mcp.mount(remote_proxy, prefix="mcp_comp")

# Testing access to mounted tools
async def test_dynamic_mount():
    tools = await mcp.get_tools()
    print("Available tools:", list(tools.keys()))
    # Shows: ['dynamic_initial_tool', 'dynamic_added_later']
    
    async with Client(mcp) as client:
        result = await client.call_tool("mcp_comp_echo_comp")
        print("Result:", result.data)
        # Shows: "Tool Added Dynamically!"


if __name__ == "__main__":
    # asyncio.run(setup())
    # asyncio.run(test_dynamic_mount())
    mcp.run(transport="http", port=8000)

