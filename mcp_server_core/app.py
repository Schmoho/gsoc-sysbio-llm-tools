from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Standard health check endpoint for Docker/MCP orchestration."""
    return jsonify({
        "status": "healthy", 
        "service": "sysbio-mcp-server",
        "message": "MCP orchestration layer is active."
    }), 200

@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """Returns the JSON schema of available biological tools for the LLM."""
    tools_schema = {
        "tools": [
            {
                "name": "cobrapy_fba",
                "description": "Run Flux Balance Analysis using COBRApy. Deterministic biological modeling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "model_path": {
                            "type": "string", 
                            "description": "Path to the SBML model file (e.g., e_coli_core.xml)"
                        }
                    },
                    "required": ["model_path"]
                }
            }
        ]
    }
    return jsonify(tools_schema), 200

if __name__ == '__main__':
    # Running on 0.0.0.0 is required for Docker containerization
    app.run(host='0.0.0.0', port=5000)
