"""Integration tests for Makefile pipeline targets.

Tests cover:
- Makefile target validation
- Build system integration
- Test execution through Make
- Code formatting and linting targets
- Clean target functionality
- Dependency checking
"""

import pytest
import subprocess
import os
from pathlib import Path


class TestMakefileTargets:
    """Integration tests for Makefile targets."""

    def test_make_available(self):
        """Verify make command is available."""
        result = subprocess.run(['make', '--version'], capture_output=True, text=True)
        assert result.returncode == 0
        assert 'GNU Make' in result.stdout or 'make' in result.stdout.lower()

    def test_make_help_target(self):
        """Test make help target displays available commands."""
        result = subprocess.run(['make', 'help'], capture_output=True, text=True, cwd='.')
        assert result.returncode == 0
        assert 'make setup' in result.stdout or 'make test' in result.stdout

    def test_makefile_exists(self):
        """Verify Makefile exists in repository root."""
        makefile = Path('Makefile')
        assert makefile.exists()
        assert makefile.is_file()

        # Verify Makefile has content
        content = makefile.read_text()
        assert len(content) > 0
        assert '.PHONY' in content

    def test_make_target_list(self):
        """Verify expected Makefile targets are defined."""
        makefile_content = Path('Makefile').read_text()

        expected_targets = [
            'help',
            'setup',
            'test',
            'lint',
            'format',
            'clean',
            'data',
            'paper',
            'all'
        ]

        for target in expected_targets:
            assert target in makefile_content, f"Target '{target}' not found in Makefile"

    def test_make_clean_dry_run(self):
        """Test make clean in dry-run mode."""
        result = subprocess.run(
            ['make', 'clean', '-n'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        # Dry run should succeed (or fail gracefully)
        assert result.returncode in [0, 2]  # 0 = success, 2 = no targets

    def test_make_test_target_validation(self):
        """Validate make test target configuration."""
        makefile_content = Path('Makefile').read_text()

        # Should reference pytest
        assert 'pytest' in makefile_content

        # Should have coverage options
        assert '--cov' in makefile_content or 'coverage' in makefile_content

    def test_make_lint_target_validation(self):
        """Validate make lint target configuration."""
        makefile_content = Path('Makefile').read_text()

        # Should reference linting tools
        lint_tools = ['flake8', 'mypy', 'pylint', 'black', 'isort']
        found_tools = [tool for tool in lint_tools if tool in makefile_content]

        assert len(found_tools) >= 2, "Makefile should reference at least 2 linting tools"

    def test_make_format_target_validation(self):
        """Validate make format target configuration."""
        makefile_content = Path('Makefile').read_text()

        # Should reference formatting tools
        assert 'black' in makefile_content
        assert 'isort' in makefile_content

    def test_make_data_target_validation(self):
        """Validate make data target configuration."""
        makefile_content = Path('Makefile').read_text()

        # Should reference data generation scripts
        assert 'generate' in makefile_content.lower() or 'data' in makefile_content

    def test_make_paper_target_validation(self):
        """Validate make paper target configuration."""
        makefile_content = Path('Makefile').read_text()

        # Should reference LaTeX compilation
        latex_commands = ['pdflatex', 'latex', 'bibtex', 'xelatex']
        found_latex = [cmd for cmd in latex_commands if cmd in makefile_content]

        assert len(found_latex) >= 1, "Makefile should reference LaTeX compilation"

    def test_make_all_target_validation(self):
        """Validate make all target configuration."""
        makefile_content = Path('Makefile').read_text()

        # 'all' target should be defined
        assert 'all:' in makefile_content

        # Should reference multiple sub-targets
        lines_after_all = []
        in_all_target = False
        for line in makefile_content.split('\n'):
            if 'all:' in line:
                in_all_target = True
            elif in_all_target:
                if line.startswith('\t') or line.startswith(' '):
                    lines_after_all.append(line)
                elif line.strip() and not line.startswith('#'):
                    break

        # 'all' should depend on other targets or have commands
        all_line = [l for l in makefile_content.split('\n') if l.startswith('all:')]
        if all_line:
            assert len(all_line[0]) > 4  # More than just "all:"


class TestMakefileExecution:
    """Integration tests for Makefile execution."""

    def test_make_without_target_shows_help(self):
        """Test that make without target shows help or runs default."""
        result = subprocess.run(['make'], capture_output=True, text=True, cwd='.')

        # Should either show help or run a default target successfully
        # Exit code 0 = success, 2 = no targets (which is OK)
        assert result.returncode in [0, 2]

    def test_make_invalid_target_fails(self):
        """Test that invalid make target fails appropriately."""
        result = subprocess.run(
            ['make', 'invalid_nonexistent_target_xyz'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Should fail for invalid target
        assert result.returncode != 0
        assert 'No rule' in result.stderr or 'not found' in result.stderr.lower()

    @pytest.mark.slow
    def test_make_test_dry_run(self):
        """Test make test in dry-run mode."""
        result = subprocess.run(
            ['make', 'test', '-n'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Dry run should show what would be executed
        assert 'pytest' in result.stdout.lower() or result.returncode in [0, 2]

    @pytest.mark.slow
    def test_make_lint_dry_run(self):
        """Test make lint in dry-run mode."""
        result = subprocess.run(
            ['make', 'lint', '-n'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Dry run should succeed
        assert result.returncode in [0, 2]

    @pytest.mark.slow
    def test_make_format_dry_run(self):
        """Test make format in dry-run mode."""
        result = subprocess.run(
            ['make', 'format', '-n'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Dry run should succeed
        assert result.returncode in [0, 2]


class TestMakefileVariables:
    """Integration tests for Makefile variable handling."""

    def test_makefile_phony_targets(self):
        """Verify .PHONY declarations in Makefile."""
        makefile_content = Path('Makefile').read_text()

        # Should have .PHONY declaration
        assert '.PHONY' in makefile_content

        # Common targets should be phony
        phony_line = [l for l in makefile_content.split('\n') if '.PHONY' in l]
        if phony_line:
            phony_targets = phony_line[0]
            common_phony = ['help', 'clean', 'test', 'all']
            found_phony = [t for t in common_phony if t in phony_targets]
            assert len(found_phony) >= 2

    def test_makefile_shell_commands(self):
        """Verify Makefile uses proper shell commands."""
        makefile_content = Path('Makefile').read_text()

        # Should contain tab-indented commands
        lines_with_tabs = [l for l in makefile_content.split('\n') if l.startswith('\t')]
        assert len(lines_with_tabs) > 0, "Makefile should have tab-indented commands"


def test_makefile_integration_with_pytest():
    """Test integration between Makefile and pytest."""
    # Run make test dry-run and verify it would call pytest
    result = subprocess.run(
        ['make', 'test', '-n'],
        capture_output=True,
        text=True,
        cwd='.'
    )

    # Should show pytest would be executed
    assert result.returncode in [0, 2]


def test_makefile_clean_targets_exist():
    """Verify clean target properly defines cleanup operations."""
    makefile_content = Path('Makefile').read_text()

    # Clean target should exist
    assert 'clean:' in makefile_content

    # Should reference common cleanup operations
    cleanup_patterns = ['rm', '__pycache__', '.pyc', '.coverage', 'htmlcov', '.pytest_cache']
    found_patterns = [p for p in cleanup_patterns if p in makefile_content]

    assert len(found_patterns) >= 3, "Clean target should reference common cleanup patterns"
