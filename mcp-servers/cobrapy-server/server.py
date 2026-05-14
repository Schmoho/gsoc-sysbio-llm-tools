"""
COBRApy MCP Server - Proof of Concept
Simple Model Context Protocol server for metabolic model analysis

Author: Atul B Raj
Date: 2026-01-28
"""

from flask import Flask, request, jsonify
import cobra
from cobra.io import load_model, read_sbml_model
from cobra.flux_analysis import flux_variability_analysis, single_gene_deletion
import traceback
import os

app = Flask(__name__)

# In-memory model cache
model_cache = {}

# ============================================================================
# Health Check & Tool Listing
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "cobrapy-mcp",
        "version": "0.1.0",
        "cached_models": len(model_cache)
    })

@app.route('/tools', methods=['GET'])
def list_tools():
    """List available tools (MCP standard)"""
    return jsonify({
        "tools": [
            {
                "name": "load_model",
                "description": "Load a metabolic model into cache",
                "parameters": {
                    "model_id": {"type": "string", "required": True, "description": "Model identifier (e.g., 'textbook')"},
                    "model_path": {"type": "string", "required": False, "description": "Path to SBML file"}
                }
            },
            {
                "name": "optimize_model",
                "description": "Run FBA optimization on a cached model",
                "parameters": {
                    "model_id": {"type": "string", "required": True}
                }
            },
            {
                "name": "get_model_stats",
                "description": "Get basic statistics about a model",
                "parameters": {
                    "model_id": {"type": "string", "required": True}
                }
            },
            {
                "name": "get_reaction_info",
                "description": "Get information about a specific reaction",
                "parameters": {
                    "model_id": {"type": "string", "required": True},
                    "reaction_id": {"type": "string", "required": True}
                }
            },
            {
                "name": "run_fva",
                "description": "Run Flux Variability Analysis",
                "parameters": {
                    "model_id": {"type": "string", "required": True},
                    "reaction_ids": {"type": "array", "required": False, "description": "Specific reactions (default: all)"}
                }
            },
            {
                "name": "gene_knockout",
                "description": "Simulate gene knockout",
                "parameters": {
                    "model_id": {"type": "string", "required": True},
                    "gene_id": {"type": "string", "required": True}
                }
            }
        ]
    })

# ============================================================================
# Model Management
# ============================================================================

@app.route('/tools/load_model', methods=['POST'])
def load_model_endpoint():
    """Load a model into cache"""
    try:
        data = request.json
        model_id = data.get('model_id')
        model_path = data.get('model_path')
        
        if not model_id:
            return jsonify({"error": "model_id required"}), 400
        
        # Load model
        if model_path:
            if not os.path.exists(model_path):
                return jsonify({"error": f"Model file not found: {model_path}"}), 404
            model = read_sbml_model(model_path)
        else:
            # Try to load built-in model
            model = load_model(model_id)
        
        # Cache it
        model_cache[model_id] = model
        
        return jsonify({
            "success": True,
            "model_id": model_id,
            "model_name": model.name,
            "reactions": len(model.reactions),
            "metabolites": len(model.metabolites),
            "genes": len(model.genes),
            "compartments": list(model.compartments.keys())
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/tools/get_model_stats', methods=['POST'])
def get_model_stats():
    """Get model statistics"""
    try:
        data = request.json
        model_id = data.get('model_id')
        
        if model_id not in model_cache:
            return jsonify({"error": f"Model '{model_id}' not loaded. Call load_model first."}), 400
        
        model = model_cache[model_id]
        
        return jsonify({
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
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# Analysis Tools
# ============================================================================

@app.route('/tools/optimize_model', methods=['POST'])
def optimize_model():
    """Run FBA optimization"""
    try:
        data = request.json
        model_id = data.get('model_id')
        
        if model_id not in model_cache:
            return jsonify({"error": f"Model '{model_id}' not loaded"}), 400
        
        model = model_cache[model_id]
        solution = model.optimize()
        
        return jsonify({
            "success": True,
            "status": solution.status,
            "objective_value": float(solution.objective_value) if solution.objective_value else None,
            "fluxes_sample": {
                rxn_id: float(flux) 
                for rxn_id, flux in list(solution.fluxes.items())[:10]
            } if solution.fluxes is not None else {}
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tools/get_reaction_info', methods=['POST'])
def get_reaction_info():
    """Get information about a specific reaction"""
    try:
        data = request.json
        model_id = data.get('model_id')
        reaction_id = data.get('reaction_id')
        
        if model_id not in model_cache:
            return jsonify({"error": f"Model '{model_id}' not loaded"}), 400
        
        if not reaction_id:
            return jsonify({"error": "reaction_id required"}), 400
        
        model = model_cache[model_id]
        
        try:
            reaction = model.reactions.get_by_id(reaction_id)
        except KeyError:
            return jsonify({"error": f"Reaction '{reaction_id}' not found"}), 404
        
        return jsonify({
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
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tools/run_fva', methods=['POST'])
def run_fva():
    """Run Flux Variability Analysis"""
    try:
        data = request.json
        model_id = data.get('model_id')
        reaction_ids = data.get('reaction_ids', None)
        
        if model_id not in model_cache:
            return jsonify({"error": f"Model '{model_id}' not loaded"}), 400
        
        model = model_cache[model_id]
        
        # Get reactions to analyze
        if reaction_ids:
            reactions = [model.reactions.get_by_id(rid) for rid in reaction_ids]
        else:
            reactions = model.reactions[:10]  # Limit to first 10 for demo
        
        fva_result = flux_variability_analysis(model, reactions)
        
        # Convert to dict
        result_dict = {
            index: {
                "minimum": float(row['minimum']),
                "maximum": float(row['maximum'])
            }
            for index, row in fva_result.iterrows()
        }
        
        return jsonify({
            "success": True,
            "reactions_analyzed": len(result_dict),
            "results": result_dict
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tools/gene_knockout', methods=['POST'])
def gene_knockout():
    """Simulate gene knockout"""
    try:
        data = request.json
        model_id = data.get('model_id')
        gene_id = data.get('gene_id')
        
        if model_id not in model_cache:
            return jsonify({"error": f"Model '{model_id}' not loaded"}), 400
        
        if not gene_id:
            return jsonify({"error": "gene_id required"}), 400
        
        model = model_cache[model_id]
        
        # Wild-type growth
        wt_solution = model.optimize()
        wt_growth = float(wt_solution.objective_value) if wt_solution.objective_value else 0
        
        # Knockout
        with model:
            try:
                gene = model.genes.get_by_id(gene_id)
                gene.knock_out()
                ko_solution = model.optimize()
                ko_growth = float(ko_solution.objective_value) if ko_solution.objective_value else 0
                
                return jsonify({
                    "success": True,
                    "gene_id": gene_id,
                    "wildtype_growth": wt_growth,
                    "knockout_growth": ko_growth,
                    "growth_reduction": wt_growth - ko_growth,
                    "growth_reduction_percent": 100 * (wt_growth - ko_growth) / wt_growth if wt_growth > 0 else 0,
                    "essential": ko_growth < 0.01,
                    "knockout_status": ko_solution.status
                })
            
            except KeyError:
                return jsonify({"error": f"Gene '{gene_id}' not found in model"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# Utility Endpoints
# ============================================================================

@app.route('/models', methods=['GET'])
def list_cached_models():
    """List all cached models"""
    models_info = []
    
    for model_id, model in model_cache.items():
        models_info.append({
            "model_id": model_id,
            "name": model.name,
            "reactions": len(model.reactions),
            "metabolites": len(model.metabolites),
            "genes": len(model.genes)
        })
    
    return jsonify({
        "cached_models": len(model_cache),
        "models": models_info
    })

@app.route('/models/<model_id>', methods=['DELETE'])
def delete_cached_model(model_id):
    """Remove model from cache"""
    if model_id in model_cache:
        del model_cache[model_id]
        return jsonify({"success": True, "message": f"Model '{model_id}' removed from cache"})
    else:
        return jsonify({"error": f"Model '{model_id}' not in cache"}), 404

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("COBRApy MCP Server - Starting")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  GET  /health              - Health check")
    print("  GET  /tools               - List available tools")
    print("  GET  /models              - List cached models")
    print("  POST /tools/load_model    - Load a model")
    print("  POST /tools/optimize_model - Run FBA")
    print("  POST /tools/get_model_stats - Get model statistics")
    print("  POST /tools/get_reaction_info - Get reaction details")
    print("  POST /tools/run_fva       - Run FVA")
    print("  POST /tools/gene_knockout - Simulate gene knockout")
    print("\nStarting server on http://localhost:5001")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
