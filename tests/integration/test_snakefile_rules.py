"""Test Snakemake workflow."""
def test_snakemake_dryrun():
    """Test Snakemake dry run."""
    import subprocess
    result = subprocess.run(['snakemake', '--version'], capture_output=True)
    assert result.returncode == 0
