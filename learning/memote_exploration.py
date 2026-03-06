"""
Exploring MEMOTE for GSoC project
Author: Atul B Raj
Date: 2026-01-28
"""

import cobra
from cobra.io import load_model

def main():
    """Main function to avoid multiprocessing issues"""
    
    print("=" * 50)
    print("MEMOTE - Metabolic Model Testing")
    print("=" * 50)
    
    model = load_model('textbook')
    
    print(f"\nModel: {model.id}")
    print(f"Reactions: {len(model.reactions)}")
    print(f"Metabolites: {len(model.metabolites)}")
    print(f"Genes: {len(model.genes)}")
    
    # Test optimization
    print("\n--- Optimization Test ---")
    solution = model.optimize()
    print(f"Status: {solution.status}")
    print(f"Objective value: {solution.objective_value:.4f}")
    
    print("\n--- MEMOTE Key Features ---")
    print("MEMOTE provides:")
    print("  1. Model quality scoring")
    print("  2. Annotation completeness checks")
    print("  3. Stoichiometric consistency validation")
    print("  4. Mass and charge balance checks")
    print("  5. Metabolite connectivity analysis")
    print("  6. Gene-Protein-Reaction (GPR) validation")
    
    print("\n--- Main Usage ---")
    print("Command-line: memote report snapshot model.xml")
    print("Output: Comprehensive HTML quality report")
    
    print("\n--- Basic Model Checks ---")
    
    reactions_with_genes = sum(1 for r in model.reactions if r.genes)
    print(f"Reactions with genes: {reactions_with_genes}/{len(model.reactions)}")
    
    metabolites_with_formula = sum(1 for m in model.metabolites if m.formula)
    print(f"Metabolites with formula: {metabolites_with_formula}/{len(model.metabolites)}")
    
    reactions_with_annotation = sum(1 for r in model.reactions if r.annotation)
    print(f"Reactions with annotations: {reactions_with_annotation}/{len(model.reactions)}")
    
    print("\n✓ Exploration complete!")

if __name__ == '__main__':
    main()
