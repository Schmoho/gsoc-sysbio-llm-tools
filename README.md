# SysBio LLM Tools (GSoC High-Level Implementation)

This repository provides a practical implementation baseline for the GSoC project:
"Provide established Metabolic Systems Biology tooling for reconstruction and analysis for LLMs."

The project goal is not to replace systems biology modeling with LLMs, but to reduce setup and workflow friction by exposing deterministic GEM tooling through:
- Model Context Protocol (MCP) servers
- `SKILLS.md` documentation interfaces

## What Is Implemented Now

- Repository scaffold for all required tools:
- CarveMe
- COBRApy
- MEMOTE
- refineGEMs
- Cytoscape

- Working MCP prototype:
- `mcp-servers/cobrapy-server/` (Flask-based, tool-style endpoints)

- Portable baseline runtime:
- `docker-compose.yml` with Neo4j + COBRApy MCP server

- High-level project docs:
- `QUICKSTART.md`
- `PROJECT_STRUCTURE.md`
- `docs/GSOC_IMPLEMENTATION_PLAN.md`
- `examples/poc_bacterial_workflow.md`

## Architecture (High Level)

1. LLM agent calls MCP tools and/or uses `SKILLS.md` guidance.
2. Tool servers execute deterministic systems biology operations.
3. Artifacts (SBML, reports, summaries) are produced.
4. Optional graph layer (Neo4j) supports network-centric queries.

## Current Repository Layout

```
sysbio-llm-tools/
├── docs/
├── examples/
├── learning/
├── mcp-servers/
│   └── cobrapy-server/
├── skills/
│   ├── carveme/
│   ├── cobrapy/
│   ├── cytoscape/
│   ├── memote/
│   └── refinegems/
├── docker-compose.yml
├── PROJECT_STRUCTURE.md
├── QUICKSTART.md
└── README.md
```

## Quick Start

```bash
docker compose up -d neo4j cobrapy-mcp
curl http://localhost:5001/health
curl http://localhost:5001/tools
```

See `QUICKSTART.md` for full setup details.

## Planned Work for Full GSoC Scope

- Implement MCP servers (or tool wrappers) for:
- CarveMe (async reconstruction jobs)
- MEMOTE (quality reports and summaries)
- refineGEMs (curation/refinement)
- Cytoscape (REST-driven network visualization)

- Integrate SBML to Neo4j workflow (Neo4JSBML strategy).
- Provide one reproducible bacterial reconstruction + analysis PoC.

Detailed execution plan is in `docs/GSOC_IMPLEMENTATION_PLAN.md`.

## Notes

- `_sample-repo/` is preserved as reference material.
- The top-level implementation is intentionally high-level and review-friendly for iterative expansion during GSoC.
