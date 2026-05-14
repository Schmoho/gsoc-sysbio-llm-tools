# MEMOTE SKILLS

## Purpose

Evaluate GEM quality and report actionable model issues in a deterministic format.

## Core Tasks

- Run MEMOTE report on SBML model.
- Extract key scores and failed checks.
- Compare two reports to track quality improvements.

## Recommended MCP Shape

- `POST /tools/run_memote`
- `POST /tools/summarize_report`
- `POST /tools/compare_reports`

## Constraints

- Reports can be large; return compact JSON summaries.
- Ensure reproducible execution with pinned MEMOTE version.
