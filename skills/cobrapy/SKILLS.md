# COBRApy SKILLS

## Purpose

Expose deterministic metabolic model analysis operations to an LLM agent.

## Core Tasks

- Load model from SBML or built-in dataset.
- Optimize objective (FBA).
- Inspect model statistics.
- Query reaction details.
- Run FVA on selected reactions.
- Simulate gene knockout effects.

## MCP Mapping

Use `mcp-servers/cobrapy-server/server.py` endpoints:
- `POST /tools/load_model`
- `POST /tools/get_model_stats`
- `POST /tools/optimize_model`
- `POST /tools/get_reaction_info`
- `POST /tools/run_fva`
- `POST /tools/gene_knockout`

## Constraints

- Model IDs must exist in cache before analysis tools are called.
- Long outputs should be summarized, not fully dumped.
