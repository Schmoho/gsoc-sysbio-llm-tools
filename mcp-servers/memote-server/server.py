from flask import Flask, request, jsonify
import logging
from memote_filter import extract_actionable_errors

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check for Docker orchestration."""
    return jsonify({"status": "healthy", "service": "memote-mcp-server"}), 200

@app.route('/mcp/memote/filter', methods=['POST'])
def filter_memote():
    """Accepts a raw MEMOTE JSON report and applies smart truncation."""
    try:
        raw_report = request.get_json()
        if not raw_report:
            return jsonify({"error": "No JSON payload provided."}), 400
        
        logging.info("Applying MEMOTE context filter...")
        optimized_report = extract_actionable_errors(raw_report)
        
        return jsonify({
            "status": "success",
            "data": optimized_report
        }), 200
        
    except Exception as e:
        logging.error(f"Error during MEMOTE filtering: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 is required for Docker
    app.run(host='0.0.0.0', port=5002)