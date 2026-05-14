"""
Exploring COBRApy basics for GSoC project
Author: Atul B Raj
Date: 2026-01-28
"""

import cobra
from cobra.io import load_model

print("Loading E. coli test model...")
model = load_model("textbook")

print(f"Model ID: {model.id}")
print(f"Number of reactions: {len(model.reactions)}")
print(f"Number of metabolites: {len(model.metabolites)}")
print(f"Number of genes: {len(model.genes)}")

# Run FBA
print("\nRunning FBA optimization...")
solution = model.optimize()
print(f"Objective value: {solution.objective_value}")
print(f"Status: {solution.status}")

# Example reaction
print("\n--- Example Reaction ---")
reaction = model.reactions.get_by_id("PFK")
print(f"Reaction: {reaction.name}")
print(f"Formula: {reaction.reaction}")
print(f"Bounds: {reaction.bounds}")

print("\n--- First 5 Metabolites ---")
for met in list(model.metabolites)[:5]:
    print(f"{met.id}: {met.name}")
