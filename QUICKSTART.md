# Quickstart

## 1. Start baseline services

```bash
cd sysbio-llm-tools
docker compose up -d neo4j mcp-orchestrator cobrapy-mcp memote-mcp
```

Services:
- Neo4j Browser: `http://localhost:7474`
- Neo4j Bolt: `bolt://localhost:7687`
- Central MCP Orchestrator: `http://localhost:5000`
- COBRApy MCP server (Internal): `http://localhost:5001`
- MEMOTE MCP server (Internal): `http://localhost:5002`

## 2. Verify COBRApy MCP server

```bash
curl http://localhost:5000/health
curl http://localhost:5000/mcp/tools
```

## 3. Run local validation (optional)

```bash
cd mcp_server_core
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 4. Review skills docs

- `skills/cobrapy/SKILLS.md`
- `skills/carveme/SKILLS.md`
- `skills/memote/SKILLS.md`
- `skills/refinegems/SKILLS.md`
- `skills/cytoscape/SKILLS.md`
- `skills/neo4jsbml/SKILLS.md`
