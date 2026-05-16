# Project Structure

## Repository Layout

```text
sysbio-llm-tools/
├── examples/
│   └── poc_bacterial_workflow.md
├── learning/
│   ├── carveme_exploration.py
│   ├── cobrapy_exploration.py
│   └── memote_exploration.py
├── mcp_server_core/          <-- Central Orchestrator
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── mcp-servers/              <-- Individual Tool Servers
│   ├── cobrapy-server/
│   ├── memote_mcp.py
│   └── neo4j_mcp.py
├── skills/
│   ├── carveme/
│   ├── cobrapy/
│   ├── cytoscape/
│   ├── memote/
│   ├── neo4jsbml/
│   └── refinegems/
├── tests/
├── docker-compose.yml        <-- Unified Deployment Stack
├── memote_filter.py          
├── pyproject.toml
├── QUICKSTART.md
└── README.md
```

## Current Implementation Status

- Unified Architecture: A central `mcp_server_core` orchestrates individual tool servers for the LLM agents.
- Active Tools: COBRApy (FBA), Neo4JSBML (Graph Queries), and MEMOTE (Quality Filtering) are officially structured as independent MCP servers.
- Deployment: A unified `docker-compose.yml` at the root directory manages the core infrastructure.
- Skills: Scaffolding complete for all required tools.

- Next implementation steps:
- Containerize memote_mcp.py and neo4j_mcp.py to match the cobrapy-server Docker standard.
- Implement MCP servers for CarveMe (async processing), refineGEMs, and Cytoscape.
- Add end-to-end proof-of-concept run for one bacterial network.
