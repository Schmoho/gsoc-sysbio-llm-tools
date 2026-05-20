# SysBio LLM Tools (GSoC High-Level Implementation)

This repository provides a practical implementation baseline for the GSoC project:
"Provide established Metabolic Systems Biology tooling for reconstruction and analysis for LLMs."

The project goal is not to replace systems biology modeling with LLMs, but to reduce setup and workflow friction by exposing deterministic GEM tooling through:
- Model Context Protocol (MCP) servers
- `SKILLS.md` documentation interfaces

## What Is Implemented Now

**Unified MCP Architecture:**
- Central orchestrator at `mcp_server_core/`
- Individual tool servers: COBRApy, Neo4JSBML, and MEMOTE.

**Working MCP Microservices:**
- `mcp-servers/cobrapy-server/` (Flask-based, tool-style endpoints)
- `mcp-servers/memote-server/` (JSON filtering and parsing)

**Repository scaffold for remaining tools:**
- CarveMe
- refineGEMs
- Cytoscape

**Portable baseline runtime:**
- Unified `docker-compose.yml` deploying Neo4j, the central MCP orchestrator, COBRApy, and MEMOTE.

## Architecture (High Level)

1. LLM agent calls MCP tools via the central orchestrator and/or uses `SKILLS.md` guidance.
2. Tool servers execute deterministic systems biology operations.
3. Artifacts (SBML, reports, summaries) are produced.
4. Optional graph layer (Neo4j) supports network-centric queries.

## Current Repository Layout

```text
sysbio-llm-tools/
├── examples/
├── learning/
├── mcp_server_core/          <-- Central Orchestrator
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
├── docker-compose.yml        <-- Unified Deployment Stack
├── memote_filter.py
├── pyproject.toml
├── PROJECT_STRUCTURE.md
├── QUICKSTART.md
└── README.md
```

## Quick Start

```bash
docker compose up -d neo4j mcp-orchestrator cobrapy-mcp
curl http://localhost:5000/health
curl http://localhost:5000/mcp/tools
```

See `QUICKSTART.md` for full setup details.

## Community Roadmap

- Containerize `memote_mcp.py` and `neo4j_mcp.py` to match the standard Docker deployment.
- Implement MCP servers (or tool wrappers) for:
  - CarveMe (async reconstruction jobs)
  - refineGEMs (curation/refinement)
  - Cytoscape (REST-driven network visualization)

- Provide one reproducible bacterial reconstruction + analysis PoC.

Detailed execution plan is currently tracked in `docs/GSOC_IMPLEMENTATION_PLAN.md` (serving as our baseline roadmap).

## Notes

- `_sample-repo/` is preserved as reference material.
- The top-level implementation is intentionally high-level and modular to encourage iterative expansion and easy peer review from all contributors.
