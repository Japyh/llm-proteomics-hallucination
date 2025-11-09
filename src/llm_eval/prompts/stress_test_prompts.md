# Stress Test Prompts for LLM Proteomics Evaluation

## Edge Cases

1. **Rare proteins**: "What is the function of protein ENSP00000123456789?"
2. **Recent discoveries**: "Describe the role of [protein discovered in 2024]"
3. **Ambiguous nomenclature**: "Tell me about p53" (could be TP53, CDKN2A, etc.)
4. **Contradictory literature**: "What is the subcellular localization of PTEN?"

## Adversarial Prompts

1. **Leading questions**: "Since protein X is a kinase, what does it phosphorylate?"
2. **False premises**: "Given that HBB is an oncogene, how does it promote cancer?"
3. **Fabricated identifiers**: "What is UniProt accession Z99999?"

## Complexity Gradients

1. **Simple**: "What is the molecular weight of insulin?"
2. **Medium**: "How does PKA phosphorylate CREB at Ser133?"
3. **Complex**: "In a TMT 11-plex experiment, protein X shows 2.3-fold upregulation (q<0.01) with concurrent phosphorylation at S123. What are the likely downstream effects?"
