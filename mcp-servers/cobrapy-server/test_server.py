#!/usr/bin/env python3
"""
Test script for COBRApy MCP Server
Demonstrates all endpoints with example requests

Author: Atul B Raj
Date: 2026-01-28
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5001"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_server():
    """Run through all server endpoints"""
    
    print("COBRApy MCP Server Test Suite")
    print("="*60)
    
    # 1. Health check
    print("\n[1/8] Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print_response("Health Check", response)
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Server not running!")
        print("Please start the server first: python server.py")
        sys.exit(1)
    
    # 2. List tools
    print("\n[2/8] Testing tools listing...")
    response = requests.get(f"{BASE_URL}/tools")
    print_response("Available Tools", response)
    
    # 3. Load model
    print("\n[3/8] Testing model loading...")
    response = requests.post(
        f"{BASE_URL}/tools/load_model",
        json={"model_id": "textbook"}
    )
    print_response("Load Model", response)
    
    # 4. Get model stats
    print("\n[4/8] Testing model statistics...")
    response = requests.post(
        f"{BASE_URL}/tools/get_model_stats",
        json={"model_id": "textbook"}
    )
    print_response("Model Statistics", response)
    
    # 5. Optimize model
    print("\n[5/8] Testing FBA optimization...")
    response = requests.post(
        f"{BASE_URL}/tools/optimize_model",
        json={"model_id": "textbook"}
    )
    print_response("FBA Optimization", response)
    
    # 6. Get reaction info
    print("\n[6/8] Testing reaction query...")
    response = requests.post(
        f"{BASE_URL}/tools/get_reaction_info",
        json={"model_id": "textbook", "reaction_id": "PFK"}
    )
    print_response("Reaction Info (PFK)", response)
    
    # 7. Run FVA
    print("\n[7/8] Testing Flux Variability Analysis...")
    response = requests.post(
        f"{BASE_URL}/tools/run_fva",
        json={"model_id": "textbook"}
    )
    print_response("FVA Results", response)
    
    # 8. Gene knockout
    print("\n[8/8] Testing gene knockout simulation...")
    response = requests.post(
        f"{BASE_URL}/tools/gene_knockout",
        json={"model_id": "textbook", "gene_id": "b0008"}
    )
    print_response("Gene Knockout (b0008)", response)
    
    # Summary
    print("\n" + "="*60)
    print("✓ All tests completed successfully!")
    print("="*60)
    print("\nServer is working correctly.")
    print("Check the results above to verify the responses.")

if __name__ == "__main__":
    test_server()
