"""
Test script for SerpAPI MCP Server
"""
import asyncio
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
import os

load_dotenv(override=True)

async def test_serpapi_mcp():
    """Test the SerpAPI MCP server"""
    
    # Check if API key is set
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("❌ ERROR: SERPAPI_API_KEY not found in environment variables")
        print("Please add SERPAPI_API_KEY=your_key to your .env file")
        return
    
    print("✅ SERPAPI_API_KEY found")
    print(f"🔑 Key starts with: {api_key[:10]}...")
    print()
    
    # Set up MCP server parameters
    params = {
        "command": "uv",
        "args": ["run", "serpapi_mcp_server.py"],
        "env": {"SERPAPI_API_KEY": api_key}
    }
    
    print("🚀 Starting SerpAPI MCP Server...")
    print()
    
    try:
        async with MCPServerStdio(params=params, client_session_timeout_seconds=60) as server:
            print("✅ MCP Server connected successfully!")
            print()
            
            # List available tools
            print("📋 Listing available tools...")
            tools = await server.list_tools()
            print(f"Found {len(tools)} tool(s):")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Test the search tool
            print("🔍 Testing serpapi_search tool...")
            print("Query: 'Python programming language'")
            print()
            
            result = await server.call_tool(
                "serpapi_search",
                {
                    "query": "Python programming language",
                    "engine": "google",
                    "num_results": 3
                }
            )
            
            print("✅ Search completed!")
            print()
            print("📊 Results:")
            print("-" * 60)
            
            if isinstance(result.content, list) and len(result.content) > 0:
                results_text = result.content[0].text
                import json
                results = json.loads(results_text)
                
                for i, item in enumerate(results, 1):
                    print(f"\n{i}. {item.get('title', 'No title')}")
                    print(f"   Link: {item.get('link', 'No link')}")
                    print(f"   Snippet: {item.get('snippet', 'No snippet')[:100]}...")
            else:
                print(result.content)
            
            print("-" * 60)
            print()
            print("✅ Test completed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_serpapi_mcp())

