import asyncio
import sys
import re
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_workflow(query: str):
    # Configure the server connection parameters
    # The server runs using python against wikipedia_mcp_server.py
    server_params = StdioServerParameters(
        command="python",
        args=["wikipedia_mcp_server.py"]
    )
    
    print(f"Connecting to Wikipedia MCP server and executing workflow for query: '{query}'...\n")
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # Initialize session
                await session.initialize()
                
                # Call search_wikipedia tool
                print(f"Step 1: Calling search_wikipedia tool for query: '{query}'...")
                search_response = await session.call_tool(
                    "search_wikipedia",
                    arguments={"query": query, "limit": 3}
                )
                
                search_text = ""
                for content in search_response.content:
                    if hasattr(content, "text"):
                        search_text += content.text
                    elif isinstance(content, dict) and "text" in content:
                        search_text += content["text"]
                    else:
                        search_text += str(content)
                
                print("Search Results returned successfully.")
                
                # Extract the first title from search results
                lines = search_text.split("\n")
                first_title = None
                for line in lines:
                    if line.startswith("Title: "):
                        first_title = line[len("Title: "):].strip()
                        break
                
                if not first_title or "No Wikipedia articles found" in search_text:
                    print(f"Could not find any articles for '{query}'.")
                    return
                
                print(f"\nStep 2: Found article title: '{first_title}'. Fetching summary...")
                summary_response = await session.call_tool(
                    "get_wikipedia_article_summary",
                    arguments={"title": first_title}
                )
                
                summary_text = ""
                for content in summary_response.content:
                    if hasattr(content, "text"):
                        summary_text += content.text
                    elif isinstance(content, dict) and "text" in content:
                        summary_text += content["text"]
                    else:
                        summary_text += str(content)
                
                # Extract the main summary extract
                extract = ""
                m_title = first_title
                if "Summary:" in summary_text:
                    parts = summary_text.split("Summary:\n")
                    if len(parts) > 1:
                        main_body = parts[1]
                        if "\n\nLink:" in main_body:
                            extract = main_body.split("\n\nLink:")[0].strip()
                        else:
                            extract = main_body.strip()
                
                if not extract:
                    extract = summary_text
                
                # Split sentences using regex to keep periods intact or reconstruct them properly
                sentences = [s.strip() for s in re.split(r'\.(?=\s|$)', extract) if s.strip()]
                
                # Format 4-part structure
                topic = f"The Wikipedia page for {m_title}"
                timeline = "No specific dates - this is a general overview."
                
                # Look for years in the extract to build a timeline
                years = re.findall(r'\b\d{4}\b', extract)
                if years:
                    timeline = ", ".join(sorted(list(set(years))))
                    
                subject = sentences[0] + "." if sentences else "No subject available."
                explanation = " ".join([s + "." for s in sentences[1:6]])
                
                formatted_summary = (
                    f"**Topic:** {topic}\n\n"
                    f"**Timeline:** {timeline}\n\n"
                    f"**Subject:** {subject}\n\n"
                    f"**Explanation:** {explanation}"
                )
                
                print("\n================ FORMATTED SUMMARY ================")
                print(formatted_summary)
                print("===================================================\n")
                
    except Exception as e:
        print(f"Error during workflow execution: {e}", file=sys.stderr)

if __name__ == "__main__":
    query = "Python (programming language)"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    asyncio.run(run_workflow(query))
