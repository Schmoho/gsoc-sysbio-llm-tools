# Neo4JSBML Tool Skills

## Purpose
This tool allows the LLM to interact with Genome-scale Metabolic Models (GEMs) stored as graph structures in a Neo4j database. It transforms SBML-derived data into a searchable knowledge graph.

## Capabilities
- **Graph Querying**: Execute Cypher queries to find metabolites, reactions, and gene associations.
- **Model Grounding**: Verify if a specific reaction exists in the reconstructed model.
- **Pathfinding**: Identify metabolic pathways between two nodes in the graph.

## LLM Instructions
When the user asks to "search the model" or "check connectivity":
1. Ensure the Neo4j container is running.
2. Formulate a Cypher query (e.g., `MATCH (m:Metabolite {name: 'Glucose'}) RETURN m`).
3. Use the `neo4jsbml_query` tool to execute and interpret the result.
4. **Safety**: Do not assume relationships not present in the Neo4j schema provided in the documentation.

## Example Prompt
"Check if there is a reaction in the current Neo4j database that connects ATP and ADP via a Phosphotransferase."