import traceback
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from memote_filter import extract_actionable_errors

# Initialize the FastMCP server
mcp = FastMCP("memote-mcp")

# ============================================================================
# Docker Health & Legacy Routes (Standard HTTP)
# ============================================================================

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check for Docker orchestration."""
    return JSONResponse({"status": "healthy", "service": "memote-mcp-server"})

@mcp.custom_route("/mcp/memote/filter", methods=["POST"])
async def filter_memote_route(request: Request) -> JSONResponse:
    """Legacy POST endpoint to match existing SKILLS.md instructions."""
    try:
        raw_report = await request.json()
        if not raw_report:
            return JSONResponse({"error": "No JSON payload provided."}, status_code=400)
        
        optimized_report = extract_actionable_errors(raw_report)
        return JSONResponse({"status": "success", "data": optimized_report})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ============================================================================
# LLM Tools (MCP Protocol)
# ============================================================================

@mcp.tool()
def filter_memote_report(raw_report: dict) -> dict:
    """
    Accepts a raw MEMOTE JSON report (as a dictionary) and applies smart truncation.
    Returns only the actionable errors to protect the LLM context window.
    """
    try:
        return extract_actionable_errors(raw_report)
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

if __name__ == '__main__':
    print("Starting FastMCP MEMOTE Server on port 5002...")
    mcp.run(transport="sse", host="0.0.0.0", port=5002)