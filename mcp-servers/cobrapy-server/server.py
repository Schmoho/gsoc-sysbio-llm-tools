"""
COBRApy MCP Server - FastMCP Migration
Model Context Protocol server for metabolic model analysis

Original Author: Atul B Raj
Migration Date: 2026-05-20
"""

import os
import traceback
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
import cobra
from cobra.io import load_model, read_sbml_model
from cobra.flux_analysis import flux_variability_analysis

# Initialize the FastMCP server
mcp = FastMCP("cobrapy-mcp")

# In-memory model cache
model_cache = {}

# ============================================================================
# Docker Health & Utility Routes (Standard HTTP)
# ============================================================================

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for Docker."""
    return JSONResponse({
        "status": "healthy",
        "service": "cobrapy-mcp",
        "version": "0.1.0",
        "cached_models": len(model_cache)
    })

@mcp.custom_route("/models", methods=["GET"])
async def list_cached_models(request: Request) -> JSONResponse:
    """List all cached models"""
    models_info = [
        {
            "model_id": m_id,
            "name": m.name,
            "reactions": len(m.reactions),
            "metabolites": len(m.metabolites),
            "genes": len(m.genes)
        }
        for m_id, m in model_cache.items()
    ]
    return JSONResponse({
        "cached_models": len(model_cache),
        "models": models_info
    })

@mcp.custom_route("/models/{model_id}", methods=["DELETE"])
async def delete_cached_model(request: Request) -> JSONResponse:
    """Remove model from cache"""
    model_id = request.path_params.get("model_id")
    if model_id in model_cache:
        del model_cache[model_id]
        return JSONResponse({"success": True, "message": f"Model '{model_id}' removed from cache"})
    return JSONResponse({"error": f"Model '{model_id}' not in cache"}, status_code=404)

# ============================================================================
# LLM Tools (MCP Protocol)
# ============================================================================

@mcp.tool()
def load_model_endpoint(model_id: str, model_path: str = None) -> dict:
    """Load a metabolic model into cache"""
    try:
        if model_path:
            if not os.path.exists(model_path):
                return {"error": f"Model file not found: {model_path}"}
            model = read_sbml_model(model_path)
        else:
            model = load_model(model_id)
        
        model_cache[model_id] = model
        
        return {
            "success": True,
            "model_id": model_id,
            "model_name": model.name,
            "reactions": len(model.reactions),
            "metabolites": len(model.metabolites),
            "genes": len(model.genes),
            "compartments": list(model.compartments.keys())
        }
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

@mcp.tool()
def get_model_stats(model_id: str) -> dict:
    """Get basic statistics about a model"""
    try:
        if model_id not in model_cache:
            return {"error": f"Model '{model_id}' not loaded. Call load_model first."}
        
        model = model_cache[model_id]
        
        return {
            "model_id": model.id,
            "model_name": model.name,
            "statistics": {
                "reactions": len(model.reactions),
                "metabolites": len(model.metabolites),
                "genes": len(model.genes),
                "compartments": len(model.compartments)
            },
            "compartments": list(model.compartments.keys()),
            "objective": str(model.objective.expression)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def optimize_model(model_id: str) -> dict:
    """Run FBA optimization"""
    try:
        if model_id not in model_cache:
            return {"error": f"Model '{model_id}' not loaded"}
        
        model = model_cache[model_id]
        solution = model.optimize()
        
        return {
            "success": True,
            "status": solution.status,
            "objective_value": float(solution.objective_value) if solution.objective_value else None,
            "fluxes_sample": {
                rxn_id: float(flux) 
                for rxn_id, flux in list(solution.fluxes.items())[:10]
            } if solution.fluxes is not None else {}
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_reaction_info(model_id: str, reaction_id: str) -> dict:
    """Get information about a specific reaction"""
    try:
        if model_id not in model_cache:
            return {"error": f"Model '{model_id}' not loaded"}
        
        model = model_cache[model_id]
        
        try:
            reaction = model.reactions.get_by_id(reaction_id)
        except KeyError:
            return {"error": f"Reaction '{reaction_id}' not found"}
        
        return {
            "id": reaction.id,
            "name": reaction.name,
            "reaction": reaction.reaction,
            "subsystem": reaction.subsystem,
            "bounds": {
                "lower": float(reaction.lower_bound),
                "upper": float(reaction.upper_bound)
            },
            "genes": [g.id for g in reaction.genes],
            "metabolites": {
                m.id: float(coeff) 
                for m, coeff in reaction.metabolites.items()
            }
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def run_fva(model_id: str, reaction_ids: list[str] = None) -> dict:
    """Run Flux Variability Analysis"""
    try:
        if model_id not in model_cache:
            return {"error": f"Model '{model_id}' not loaded"}
        
        model = model_cache[model_id]
        
        if reaction_ids:
            reactions = [model.reactions.get_by_id(rid) for rid in reaction_ids]
        else:
            reactions = model.reactions[:10]
        
        fva_result = flux_variability_analysis(model, reactions)
        
        result_dict = {
            index: {
                "minimum": float(row['minimum']),
                "maximum": float(row['maximum'])
            }
            for index, row in fva_result.iterrows()
        }
        
        return {
            "success": True,
            "reactions_analyzed": len(result_dict),
            "results": result_dict
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def gene_knockout(model_id: str, gene_id: str) -> dict:
    """Simulate gene knockout"""
    try:
        if model_id not in model_cache:
            return {"error": f"Model '{model_id}' not loaded"}
        
        model = model_cache[model_id]
        
        wt_solution = model.optimize()
        wt_growth = float(wt_solution.objective_value) if wt_solution.objective_value else 0
        
        with model:
            try:
                gene = model.genes.get_by_id(gene_id)
                gene.knock_out()
                ko_solution = model.optimize()
                ko_growth = float(ko_solution.objective_value) if ko_solution.objective_value else 0
                
                return {
                    "success": True,
                    "gene_id": gene_id,
                    "wildtype_growth": wt_growth,
                    "knockout_growth": ko_growth,
                    "growth_reduction": wt_growth - ko_growth,
                    "growth_reduction_percent": 100 * (wt_growth - ko_growth) / wt_growth if wt_growth > 0 else 0,
                    "essential": ko_growth < 0.01,
                    "knockout_status": ko_solution.status
                }
            except KeyError:
                return {"error": f"Gene '{gene_id}' not found in model"}
    except Exception as e:
        return {"error": str(e)}

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("COBRApy MCP Server (FastMCP Migration) - Starting")
    print("=" * 60)
    print("\nStarting server on port 5001 using SSE transport...")
    print("=" * 60)
    
    mcp.run(transport="sse", host="0.0.0.0", port=5001)