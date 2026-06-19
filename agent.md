# Wikipedia Agent Configuration & Playbook

This playbook defines the environment setup and operation rules for the Wikipedia Agent in the Antigravity IDE. It explains how the agent connects to Wikipedia and how it processes the operation queue to search and summarize articles.

---

## 1. Setup Guide: Connecting the Wikipedia MCP

Add the following configuration block under the `"mcpServers"` object in your active [mcp_config.json](file:///c:/Users/vaish/.gemini/config/mcp_config.json) to register the Wikipedia MCP server:

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

## 2. Agent Operation Manual

When the user instructs you to **"process the Wikipedia queue"**, you must execute the tasks listed in [queue.json](file:///c:/Users/vaish/OneDrive/it/wikipedia%20mcp/queue.json) by following these instructions:

### Workflow
1. **Read Queue**: Read the contents of [queue.json](file:///c:/Users/vaish/OneDrive/it/wikipedia%20mcp/queue.json).
2. **Filter Pending**: Identify all tasks with `"status": "pending"`.
3. **Execute Actions**: For each pending task, call the corresponding tool on the `wikipedia` server:
   - **`search_wikipedia`**: Search Wikipedia for articles matching `query`.
   - **`get_wikipedia_article_summary`**: Retrieve the summary of a specific page using `title`.
4. **Format Summaries (Critical)**: When executing a `get_wikipedia_article_summary` action, you **MUST** format the output returned to the user and saved in the queue's `"result"` field using the following exact 4-part structure:
   
   ```
   **Topic:** [a short phrase naming what the content is fundamentally about]
   
   **Timeline:** [dates, years, or chronological span covered — or an explicit note that there isn't one]
   
   **Subject:** [exactly one sentence — the "what happened" in a single line, like a headline]
   
   **Explanation:** [five sentences expanding on the Subject with the most important supporting details]
   ```
   
   - *Topic*: A short phrase, not a full sentence (e.g., "The 2008 global financial crisis").
   - *Timeline*: Name actual dates/years/spans found in the content. If the content has no timeline, state "No specific dates — this is a general explainer on X."
   - *Subject*: Exactly one sentence, the headline-level takeaway.
   - *Explanation*: A target of five sentences (up to 6 if needed for coherence) covering causes, key players, outcomes, or significance.
   
5. **Update Queue**: Upon completion (or failure), update the task's state in [queue.json](file:///c:/Users/vaish/OneDrive/it/wikipedia%20mcp/queue.json):
   - Set `"status"` to `"completed"` or `"failed"`.
   - Update `"updated_at"` to the current timestamp.
   - Populate `"result"` with the formatted summary/results or error messages.
6. **Summarize**: Provide the user with a summary of successfully executed operations and any errors encountered.
