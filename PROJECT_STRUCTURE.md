# Project Structure

## Repository Layout

```
sysbio-llm-tools/
├── docs/
│   └── GSOC_IMPLEMENTATION_PLAN.md
├── examples/
│   └── poc_bacterial_workflow.md
├── learning/
│   ├── NOTES.md
│   ├── carveme_exploration.py
│   ├── cobrapy_exploration.py
│   └── memote_exploration.py
├── mcp-servers/
│   └── cobrapy-server/
│       ├── Dockerfile
│       ├── README.md
│       ├── requirements.txt
│       ├── server.py
│       ├── test_server.py
│       └── validate_server.py
├── skills/
│   ├── carveme/
│   │   └── SKILLS.md
│   ├── cobrapy/
│   │   └── SKILLS.md
│   ├── cytoscape/
│   │   └── SKILLS.md
│   ├── memote/
│   │   └── SKILLS.md
│   └── refinegems/
│       └── SKILLS.md
├── docker-compose.yml
├── LICENSE
├── QUICKSTART.md
└── README.md
```

## Current Implementation Status

- Implemented now:
- `cobrapy-server` MCP prototype (Flask API).
- Skills scaffolding for all required tools.
- Portable container baseline with Neo4j + COBRApy MCP server.
- Quickstart and implementation roadmap docs.

- Next implementation steps:
- Add MCP servers for CarveMe, MEMOTE, refineGEMs, Cytoscape.
- Integrate Neo4J MCP server container in compose stack.
- Add end-to-end proof-of-concept run for one bacterial network.
