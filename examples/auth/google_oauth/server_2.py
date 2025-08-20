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


auth_2 = GitHubProvider(
    client_id=os.getenv("FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID") or "",
    client_secret=os.getenv("FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET") or "",
    base_url="http://localhost:8001",
    # redirect_path="/oauth/callback",  # Default path - change if using a different callback URL
)


mcp_comp = FastMCP("Comp server with Google OAuth", auth=auth_2)

@mcp_comp.tool
def echo_comp() -> str:
    """Echo the provided message."""
    return f"Hello,!"




if __name__ == "__main__":
    mcp_comp.run(transport="http", port=8001)

