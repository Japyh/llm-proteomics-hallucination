# Data Processing Module

Data loading, validation, and processing utilities.

---

## Modules

### protein_database.py

Interface to protein databases (UniProt, HPA, PeptideAtlas).

**Classes**:
- `ProteinDatabase`: Database interface
- `UniProtClient`: UniProt API client

**Usage**:
```python
from src.data_processing.protein_database import UniProtClient

client = UniProtClient()
protein = client.get_protein('P68871')  # HBB
print(protein['function'])
```

### synthetic_data_generator.py

Generate synthetic proteomics data for testing.

**Classes**:
- `SyntheticDataGenerator`: Main generator

**Usage**:
```python
from src.data_processing.synthetic_data_generator import SyntheticDataGenerator

gen = SyntheticDataGenerator()
proteins = gen.generate_proteins(n=100)
```
