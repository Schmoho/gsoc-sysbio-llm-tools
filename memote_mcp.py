from flask import Flask, request, jsonify
import logging

# Importing your core extraction logic from PR #7
from memote_filter import extract_actionable_errors

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/mcp/memote/filter', methods=['POST'])
def filter_memote():
    """
    MCP Endpoint: Accepts a raw MEMOTE JSON report, applies smart truncation, 
    and returns the optimized report for the LLM agent.
    """
    try:
        # Parse the incoming JSON payload from the LLM agent
        raw_report = request.get_json()
        
        if not raw_report:
            return jsonify({
                "error": "No JSON payload provided. Please send a valid MEMOTE report."
            }), 400

        logging.info("Received MEMOTE report. Applying context filter...")
        
        # Pass the report through your Intelligent Context Filter
        optimized_report = extract_actionable_errors(raw_report)
        
        logging.info("Report successfully filtered and truncated.")
        
        return jsonify({
            "status": "success",
            "data": optimized_report,
            "message": "Report processed. Graph query hints injected where truncation occurred."
        }), 200

    except Exception as e:
        logging.error(f"Unexpected error during MEMOTE filtering: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Running on 5006 so it doesn't conflict with your Neo4j server on 5005
    print("Starting MEMOTE Context Filter MCP Server on port 5006...")
    app.run(port=5006)