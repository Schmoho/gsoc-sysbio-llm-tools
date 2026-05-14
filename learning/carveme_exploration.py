"""
Exploring CarveMe for GSoC project
Author: Atul B Raj
Date: 2026-01-28
"""

print("=" * 50)
print("CarveMe - Automated Metabolic Model Reconstruction")
print("=" * 50)

print("\nCarveMe Overview:")
print("- Automated genome-scale metabolic model reconstruction")
print("- Uses protein sequences (FASTA) or genome annotations")
print("- Template-based approach (uses universal model)")
print("- Automated gap-filling")
print("- Outputs SBML format models")

print("\n--- Main Usage ---")
print("Command-line tool (primary interface):")
print("  carve genome.faa -o model.xml")
print("  carve --refseq GCF_000005845.2 -o ecoli_model.xml")

print("\n--- Key Features ---")
print("1. Genome-to-model in one command")
print("2. RefSeq database integration")
print("3. Multiple media conditions")
print("4. Gap-filling algorithms")
print("5. Quality checks built-in")

print("\n--- Reconstruction Steps ---")
print("1. Load genome/protein sequences")
print("2. Annotate genes (if needed)")
print("3. Map to universal reactions")
print("4. Build draft model")
print("5. Gap-fill for biomass production")
print("6. Export SBML")

print("\n--- Media Options ---")
print("CarveMe supports multiple growth media:")
print("  --mediadb - Use pre-defined media")
print("  M9 - Minimal medium")
print("  LB - Rich medium")
print("  Custom media via CSV")

print("\n--- For MCP Integration ---")
print("Challenges:")
print("  - Long running (minutes to hours)")
print("  - Command-line tool (need subprocess)")
print("  - Async job queue needed")
print("  - Progress tracking important")

print("\n--- Example API Workflow ---")
print("1. Submit genome file/RefSeq ID")
print("2. Start reconstruction job (async)")
print("3. Return job ID")
print("4. Poll job status endpoint")
print("5. Download completed model")

print("\n--- Typical Reconstruction Times ---")
print("Small bacterial genome: 5-15 minutes")
print("Large bacterial genome: 15-45 minutes")
print("Eukaryotic genome: 1-3 hours")

print("\n✓ Exploration complete!")
print("\nNext: Create comprehensive CarveMe SKILLS.md")
