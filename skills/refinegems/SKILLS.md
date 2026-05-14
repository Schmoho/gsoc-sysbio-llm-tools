# refineGEMs SKILLS

## Purpose

Refine and curate reconstructed GEMs after initial generation and quality checks.

## Core Tasks

- Apply curation/refinement routines to model artifacts.
- Standardize annotations and resolve common model inconsistencies.
- Export refined SBML for downstream analysis.

## Recommended MCP Shape

- `POST /tools/refine_model`
- `POST /tools/standardize_annotations`
- `POST /tools/export_model`

## Constraints

- Keep transformations traceable and reversible where possible.
- Return explicit before/after summary metrics.
