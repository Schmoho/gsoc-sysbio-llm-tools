# COBRApy MCP Server

Simple Model Context Protocol server for COBRApy metabolic model analysis.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python server.py

# In another terminal, validate or test
python validate_server.py  # Validate code (no server needed)
python test_server.py      # Full HTTP tests (server must be running)
```

Server runs on `http://localhost:5001` (port 5001 avoids macOS AirPlay conflict on 5000)

## Available Endpoints

### Health Check
```bash
curl http://localhost:5001/health
```

### List Tools
```bash
curl http://localhost:5001/tools
```

### Load Model
```bash
curl -X POST http://localhost:5001/tools/load_model \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'
```

### Run FBA
```bash
curl -X POST http://localhost:5001/tools/optimize_model \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'
```

### Get Model Stats
```bash
curl -X POST http://localhost:5001/tools/get_model_stats \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'
```

### Get Reaction Info
```bash
curl -X POST http://localhost:5001/tools/get_reaction_info \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook", "reaction_id": "PFK"}'
```

### Run FVA
```bash
curl -X POST http://localhost:5001/tools/run_fva \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'
```

### Gene Knockout
```bash
curl -X POST http://localhost:5001/tools/gene_knockout \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook", "gene_id": "b0008"}'
```

### List Cached Models
```bash
curl http://localhost:5001/models
```

## Example API Workflow

```bash
# 1. Check health
curl http://localhost:5001/health

# 2. Load model
curl -X POST http://localhost:5001/tools/load_model \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'

# 3. Get stats
curl -X POST http://localhost:5001/tools/get_model_stats \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'

# 4. Optimize
curl -X POST http://localhost:5001/tools/optimize_model \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook"}'

# 5. Test gene knockout
curl -X POST http://localhost:5001/tools/gene_knockout \
  -H "Content-Type: application/json" \
  -d '{"model_id": "textbook", "gene_id": "b0008"}'
```

## Python Client Example

```python
import requests
import json

base_url = "http://localhost:5001"

# Load model
response = requests.post(
    f"{base_url}/tools/load_model",
    json={"model_id": "textbook"}
)
print(json.dumps(response.json(), indent=2))

# Optimize
response = requests.post(
    f"{base_url}/tools/optimize_model",
    json={"model_id": "textbook"}
)
result = response.json()
print(f"Growth rate: {result['objective_value']}")

# Gene knockout
response = requests.post(
    f"{base_url}/tools/gene_knockout",
    json={"model_id": "textbook", "gene_id": "b0008"}
)
result = response.json()
print(f"WT growth: {result['wildtype_growth']:.3f}")
print(f"KO growth: {result['knockout_growth']:.3f}")
print(f"Essential: {result['essential']}")
```

## Architecture

```
Client Request
    ↓
Flask Server (server.py)
    ↓
COBRApy Library
    ↓
Model Cache (in-memory)
    ↓
JSON Response
```

## Next Steps for Production

- [ ] Add authentication/API keys
- [ ] Implement rate limiting
- [ ] Add request logging
- [ ] Docker containerization
- [ ] Database for persistent model storage
- [ ] WebSocket support for long-running operations
- [ ] Batch operations support
- [ ] Model comparison endpoints
- [ ] Integration with MEMOTE quality checks
- [ ] Integration with CarveMe reconstruction

## Development

```bash
# Run in debug mode (auto-reload)
python server.py

# Check code style
black server.py
flake8 server.py
```

## License

Same as parent project.

