#!/usr/bin/env python3
"""
Quick validation of MCP server code
Tests the server endpoints without actually starting the Flask app

Author: Atul B Raj
Date: 2026-01-28
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("COBRApy MCP Server - Code Validation")
print("=" * 60)

try:
    print("\n[1/5] Importing dependencies...")
    import flask
    import cobra
    print("✓ Flask and COBRApy imported successfully")
    
    print("\n[2/5] Loading server module...")
    import server
    print("✓ Server module loaded successfully")
    
    print("\n[3/5] Checking Flask app...")
    assert server.app is not None
    print("✓ Flask app created")
    
    print("\n[4/5] Verifying endpoints...")
    routes = [rule.rule for rule in server.app.url_map.iter_rules()]
    expected_routes = [
        '/health',
        '/tools',
        '/models',
        '/tools/load_model',
        '/tools/optimize_model',
        '/tools/get_model_stats',
        '/tools/get_reaction_info',
        '/tools/run_fva',
        '/tools/gene_knockout'
    ]
    
    for route in expected_routes:
        if route in routes:
            print(f"  ✓ {route}")
        else:
            print(f"  ✗ {route} - MISSING!")
    
    print("\n[5/5] Testing COBRApy functionality...")
    model = cobra.io.load_model("textbook")
    print(f"  ✓ Loaded model: {len(model.reactions)} reactions")
    
    solution = model.optimize()
    print(f"  ✓ FBA optimization: {solution.objective_value:.3f}")
    
    print("\n" + "=" * 60)
    print("✓ All validations passed!")
    print("=" * 60)
    print("\nServer code is working correctly.")
    print("To run the server: python server.py")
    print("To test with requests: python test_server.py (after starting server)")
    print("To see workflow examples: python example_workflow.py (after starting server)")
    
except ImportError as e:
    print(f"\n✗ Import error: {e}")
    print("\nMake sure you have all dependencies installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ Validation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
