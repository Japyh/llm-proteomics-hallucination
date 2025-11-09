"""Test protein metadata integrity."""
def test_uniprot_accessions():
    """Validate UniProt accession format."""
    import re
    accession_pattern = r'^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$'
    test_ids = ['P04637', 'Q8WXI7', 'P68871']
    for acc_id in test_ids:
        assert re.match(accession_pattern, acc_id), f"Invalid accession: {acc_id}"
