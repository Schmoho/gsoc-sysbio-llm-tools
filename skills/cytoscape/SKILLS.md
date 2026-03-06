# Cytoscape SKILLS

## Purpose

Support network visualization and subnetwork analysis via Cytoscape REST automation.

## Core Tasks

- Create/import network from model-derived edges.
- Apply style and layout for metabolic pathways.
- Filter or highlight nodes/reactions by analysis results.
- Export figures for reporting.

## Recommended MCP Shape

- `POST /tools/create_network`
- `POST /tools/apply_layout`
- `POST /tools/style_network`
- `POST /tools/export_image`

## Constraints

- Cytoscape must be running and reachable via REST.
- Use explicit IDs to avoid ambiguous network selection.
