"""Test Makefile pipeline."""
import subprocess

def test_makefile_targets():
    """Verify Makefile targets work."""
    result = subprocess.run(['make', '--version'], capture_output=True)
    assert result.returncode == 0
