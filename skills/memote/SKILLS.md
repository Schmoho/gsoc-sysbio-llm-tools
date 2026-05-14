# MEMOTE Context Filter Tool Skills

## Purpose
This tool acts as a protective proxy between raw, massive MEMOTE JSON reports and the LLM context window. It prevents agent hallucination and timeouts by filtering. It evaluates GEM quality and reports actionable model issues in a deterministic format.

## Capabilities & Core Tasks
* **Smart Filtering**: Extracts only "Failed" or "Warning" metrics from raw MEMOTE data.
* **Context Protection**: Automatically caps massive arrays of failing metabolites/reactions to a strict limit.
* **Workflow Routing**: Injects semantic hints prompting the LLM to use the Neo4j Graph database when massive model gaps are detected.
* **Execution**: Runs MEMOTE report on SBML model, extracts key scores, and compares two reports to track quality improvements.

## LLM Instructions
When the user asks to "analyze the MEMOTE report" or "check model quality":
1. Do NOT attempt to read the raw MEMOTE JSON file directly into your context.
2. Send the raw JSON payload via a POST request to the `memote_filter` tool (running locally on port 5006).
3. Read the truncated, safe response.
4. **Crucial**: If the response includes the hint "...Use specific graph queries to explore further", you MUST transition to using the `neo4jsbml_query` tool to investigate.

## Recommended MCP Shape
- `POST /tools/run_memote`
- `POST /tools/summarize_report`
- `POST /tools/compare_reports`

## Constraints
- Reports can be large; return compact JSON summaries.
- Ensure reproducible execution with pinned MEMOTE version.

## Example Prompt
"Analyze the MEMOTE report for this bacterial model. If there are massive stoichiometric failures, give me a summary and then check the graph database for the first failing reaction."
