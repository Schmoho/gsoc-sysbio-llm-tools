# PoC Bacterial Workflow (High Level)

## Goal

Show end-to-end reconstruction and analysis assisted by LLM agents using MCP tools and SKILLS docs.

## Candidate Workflow

1. Reconstruct model from genome using CarveMe.
2. Load model in COBRApy and run baseline FBA.
3. Validate quality with MEMOTE.
4. Refine with refineGEMs where needed.
5. Visualize selected network views in Cytoscape.
6. Optionally map SBML to Neo4j and run graph queries.

## Minimal Success Criteria

- Reconstructed model artifact produced.
- Growth simulation completed.
- MEMOTE report generated and key issues summarized.
- At least one refinement action documented.
- At least one visualization screenshot/export generated.
