import json

def extract_actionable_errors(report_data, max_items=5):
    """
    Parses a full MEMOTE JSON dictionary and extracts critical errors.
    Implements smart truncation to guarantee the LLM context window is protected.
    """
    actionable_errors = []
    tests = report_data.get("tests", {})

    for test_id, test_info in tests.items():
        # Only process failed tests or tests with poor scores/warnings
        if test_info.get("result") in ["Failed", "Warning"]:
            
            raw_data = test_info.get("data", [])
            truncated_data = raw_data
            
            if isinstance(raw_data, list) and len(raw_data) > max_items:
                truncated_data = raw_data[:max_items]
                truncated_data.append(f"...and {len(raw_data) - max_items} more items. (Use specific graph queries to explore further.)")
            
            elif isinstance(raw_data, dict):
                truncated_data = "Complex dictionary data omitted to save context. See raw report."

            error_summary = {
                "issue": test_info.get("title", test_id),
                "description": test_info.get("summary", "No description provided."),
                "metric": test_info.get("metric"),
                "affected_items": truncated_data
            }
            actionable_errors.append(error_summary)

    return actionable_errors

def run_memote_filter(file_path):
    """
    File handling wrapper for the extraction logic.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            report_data = json.load(file)
            
        return extract_actionable_errors(report_data)

    except FileNotFoundError:
        return {"error": f"Report not found at {file_path}."}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the MEMOTE report."}
    except Exception as e:
        return {"error": f"Unexpected pipeline error: {str(e)}"}

if __name__ == "__main__":
    test_file_path = "tests/sample_memote_report.json"
    print("Running Production-Grade MEMOTE Filter...\n")
    results = run_memote_filter(test_file_path)
    print(json.dumps(results, indent=2))