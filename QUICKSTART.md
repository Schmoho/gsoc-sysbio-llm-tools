# Quickstart

## 1. Start baseline services

```bash
cd sysbio-llm-tools
docker compose up -d neo4j cobrapy-mcp
```

Services:
- Neo4j Browser: `http://localhost:7474`
- Neo4j Bolt: `bolt://localhost:7687`
- COBRApy MCP server: `http://localhost:5001`

## 2. Verify COBRApy MCP server

```bash
curl http://localhost:5001/health
curl http://localhost:5001/tools
```

## 3. Run local validation (optional)

```bash
cd mcp-servers/cobrapy-server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python validate_server.py
```

## 4. Review skills docs

- `skills/cobrapy/SKILLS.md`
- `skills/carveme/SKILLS.md`
- `skills/memote/SKILLS.md`
- `skills/refinegems/SKILLS.md`
- `skills/cytoscape/SKILLS.md`

## 5. Follow implementation roadmap

Open `docs/GSOC_IMPLEMENTATION_PLAN.md` and execute by phase.
