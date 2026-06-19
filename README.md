# Wikipedia MCP (Model Context Protocol) Server & Workflows

A feature-rich Model Context Protocol (MCP) project built with [FastMCP](https://github.com/modelcontext/fastmcp). This project includes a Wikipedia MCP server, an automated queue processor, and an programmatic MCP client workflow.

---

## ⚡ Features

- **Search Wikipedia**: Query Wikipedia articles and get titles, descriptions, and page links.
- **Article Summaries**: Retrieve article extracts formatted into structured markdown summaries.
- **Task Queue Runner**: A stateful queue processor that reads, runs, and updates pending Wikipedia jobs from a JSON file.
- **Interactive Client**: A native Python MCP client script that programmatically connects to the server and automates multi-tool workflows.

---

## 📂 Repository Structure

- `wikipedia_mcp_server.py`: The core FastMCP server exposing tools for searching and summarizing Wikipedia pages.
- `mcp_client_workflow.py`: A client script that spawns the server, connects to it, executes the tools, and formats the summaries.
- `run_workflow.py`: A helper script that reads from `queue.json` and updates task results.
- `queue.json`: Stores pending and completed workflows.
- `agent.md`: The agent instruction playbook and IDE configuration guide.
- `wikipedia_workflow.md`: Detailed system architecture, data flow, and formatting specifications.

---

## 🛠 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed and the required libraries:
```bash
pip install mcp fastmcp requests
```

### 2. Configure in your IDE
Add the following configuration block under the `"mcpServers"` object in your active `mcp_config.json` configuration file:
```json
    "wikipedia": {
      "type": "stdio",
      "command": "python",
      "args": [
        "c:/Users/vaish/OneDrive/it/wikipedia mcp/wikipedia_mcp_server.py"
      ]
    }
```

---

## 🚀 Usage

### Run the Client Workflow
You can execute the automated search-and-summarize client workflow script directly:
```bash
python mcp_client_workflow.py "Artificial Intelligence"
```

### Format of Generated Summaries
Summaries are formatted into a strict 4-part structure:
```markdown
**Topic:** The Wikipedia page for [Article Title]

**Timeline:** [Dates/Years referenced in the article, or "No specific dates"]

**Subject:** [One-sentence takeaway headline]

**Explanation:** [Exactly five sentences expanding on the Subject]
```

### Run the Queue Processor
To run tasks defined in `queue.json`:
```bash
python run_workflow.py
```
