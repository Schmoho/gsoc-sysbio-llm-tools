import sys

def main():
    print("="*60)
    print(" SysBio LLM Tools - Project Environment")
    print("="*60)
    print("\nThis project is orchestrated via Docker.")
    print("\nTo start the database, orchestrator, and tool servers, run:")
    print("    docker compose up -d neo4j mcp-orchestrator cobrapy-mcp")
    print("\nTo view the active tools available to the LLM agent, run:")
    print("    curl http://localhost:5000/mcp/tools")
    print("\nFor full setup instructions, please read QUICKSTART.md")
    print("="*60)

if __name__ == "__main__":
    main()