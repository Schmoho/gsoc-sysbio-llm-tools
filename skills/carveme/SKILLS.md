# CarveMe SKILLS

## Purpose

Automate GEM reconstruction from genome/protein inputs and make the process callable by an LLM.

## Core Tasks

- Submit reconstruction job from input FASTA.
- Track long-running reconstruction status.
- Retrieve generated SBML artifact.
- Optionally run gap-filling under selected media assumptions.

## Recommended MCP Shape

- `POST /tools/reconstruct_model`
- `GET /jobs/<job_id>`
- `GET /jobs/<job_id>/artifact`

## Constraints

- Reconstruction is compute-heavy and should be asynchronous.
- Store job metadata and output paths explicitly.
- Validate file inputs before launching commands.
