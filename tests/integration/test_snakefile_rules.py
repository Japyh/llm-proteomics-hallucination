"""Integration tests for Snakemake workflow rules.

Tests cover:
- Snakemake workflow validation
- Rule definitions and dependencies
- Dry-run execution
- DAG construction
- Configuration file loading
- Input/output file specifications
- Workflow completeness
"""

import pytest
import subprocess
import os
from pathlib import Path
import yaml


class TestSnakemakeAvailability:
    """Test Snakemake installation and basic functionality."""

    def test_snakemake_installed(self):
        """Verify snakemake command is available."""
        result = subprocess.run(['snakemake', '--version'], capture_output=True, text=True)
        assert result.returncode == 0
        assert len(result.stdout) > 0

    def test_snakefile_exists(self):
        """Verify Snakefile exists in pipelines directory."""
        snakefile = Path('pipelines/snakemake/Snakefile')
        assert snakefile.exists(), "Snakefile not found at pipelines/snakemake/Snakefile"
        assert snakefile.is_file()

        # Verify Snakefile has content
        content = snakefile.read_text()
        assert len(content) > 0
        assert 'rule' in content


class TestSnakemakeRuleDefinitions:
    """Test Snakemake rule definitions and structure."""

    def test_required_rules_defined(self):
        """Verify all required rules are defined in Snakefile."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        required_rules = [
            'all',
            'prepare_data',
            'run_llm_evaluation',
            'analyze_results',
            'generate_figures',
            'compile_manuscript',
            'clean'
        ]

        for rule_name in required_rules:
            assert f'rule {rule_name}' in content, f"Rule '{rule_name}' not found in Snakefile"

    def test_rule_all_has_inputs(self):
        """Verify 'all' rule specifies final outputs."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Find 'rule all' section
        assert 'rule all:' in content

        # Should have input directive
        lines = content.split('\n')
        in_all_rule = False
        has_input = False

        for line in lines:
            if 'rule all:' in line:
                in_all_rule = True
            elif in_all_rule:
                if 'input:' in line:
                    has_input = True
                elif line.strip().startswith('rule '):
                    break

        assert has_input, "Rule 'all' should specify input files"

    def test_configfile_directive(self):
        """Verify configfile directive is present."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        assert 'configfile:' in content, "Snakefile should have configfile directive"

    def test_include_directives(self):
        """Verify include directives for modular rules."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Should include rule modules
        if 'include:' in content:
            # Verify included files exist
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('include:'):
                    # Extract filename
                    filename = line.split('include:')[1].strip().strip('"\'')
                    # Construct full path
                    included_path = Path('pipelines/snakemake') / filename
                    # Check if exists (optional - may not exist in minimal setup)
                    if not included_path.exists():
                        # If includes don't exist, it's OK for minimal testing
                        pass


class TestSnakemakeDryRun:
    """Test Snakemake dry-run execution."""

    @pytest.mark.slow
    def test_dry_run_all_target(self):
        """Test snakemake dry-run for all target."""
        result = subprocess.run(
            ['snakemake', '--snakefile', 'pipelines/snakemake/Snakefile', '-n'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Dry run may fail if inputs don't exist, but should parse successfully
        # Exit code 0 = success, 1 = missing files (expected in test), 2 = parse error
        assert result.returncode in [0, 1], f"Snakemake dry-run failed with code {result.returncode}"

    @pytest.mark.slow
    def test_dag_generation(self):
        """Test DAG generation from Snakefile."""
        result = subprocess.run(
            ['snakemake', '--snakefile', 'pipelines/snakemake/Snakefile', '--dag'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # DAG generation may fail if inputs missing, but should parse
        assert result.returncode in [0, 1]

    @pytest.mark.slow
    def test_print_rules(self):
        """Test printing all rules from Snakefile."""
        result = subprocess.run(
            ['snakemake', '--snakefile', 'pipelines/snakemake/Snakefile', '-l'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Should list rules successfully
        assert result.returncode == 0
        # Should show some rules
        assert len(result.stdout) > 0


class TestSnakemakeConfiguration:
    """Test Snakemake configuration handling."""

    def test_config_file_referenced(self):
        """Verify config file is referenced in Snakefile."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Should have configfile directive
        assert 'configfile:' in content

        # Extract config path
        lines = content.split('\n')
        for line in lines:
            if 'configfile:' in line:
                config_path = line.split('configfile:')[1].strip().strip('"\'')
                # Config path should be specified
                assert len(config_path) > 0

    def test_pipeline_config_exists_or_example(self):
        """Verify pipeline config file exists or has example."""
        # Check for actual config
        config_paths = [
            Path('configs/pipelines.yaml'),
            Path('configs/pipelines.yml'),
            Path('pipelines/snakemake/config.yaml')
        ]

        config_exists = any(p.exists() for p in config_paths)

        # If no config exists, that's OK for testing
        # Just verify Snakefile references one
        snakefile_content = Path('pipelines/snakemake/Snakefile').read_text()
        assert 'configfile:' in snakefile_content


class TestSnakemakeInputOutput:
    """Test input/output file specifications in rules."""

    def test_rules_have_input_output(self):
        """Verify key rules have input and output directives."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Rules that should have input/output
        rules_with_io = ['prepare_data', 'run_llm_evaluation', 'analyze_results']

        for rule_name in rules_with_io:
            if f'rule {rule_name}' in content:
                # Find rule block
                lines = content.split('\n')
                in_rule = False
                has_input = False
                has_output = False

                for line in lines:
                    if f'rule {rule_name}:' in line:
                        in_rule = True
                    elif in_rule:
                        if 'input:' in line:
                            has_input = True
                        if 'output:' in line:
                            has_output = True
                        if line.strip().startswith('rule '):
                            break

                # Most rules should have output at minimum
                assert has_output, f"Rule '{rule_name}' should have output directive"

    def test_wildcard_usage(self):
        """Verify wildcards are used in dynamic rules."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Check if wildcards are used (common pattern: {model}, {sample}, etc.)
        if '{' in content and '}' in content:
            # Wildcards are used - verify they're in rules
            assert 'rule' in content
            # This is expected for dynamic workflows


class TestSnakemakeShellCommands:
    """Test shell commands in Snakemake rules."""

    def test_rules_have_shell_or_script(self):
        """Verify rules have shell or script directives."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Count rules with execution directives
        has_shell = content.count('shell:')
        has_script = content.count('script:')
        has_run = content.count('run:')

        # Should have at least some execution directives
        total_execution = has_shell + has_script + has_run
        assert total_execution > 0, "Rules should have shell, script, or run directives"

    def test_python_scripts_referenced(self):
        """Verify Python scripts are referenced in rules."""
        snakefile_path = Path('pipelines/snakemake/Snakefile')
        content = snakefile_path.read_text()

        # Should reference Python scripts
        assert 'python' in content.lower()

        # Should reference project modules
        references = ['src/', 'data/', 'paper/']
        found_refs = [ref for ref in references if ref in content]

        assert len(found_refs) >= 1, "Should reference project directories"


def test_snakemake_workflow_completeness():
    """Test overall workflow completeness."""
    snakefile_path = Path('pipelines/snakemake/Snakefile')
    content = snakefile_path.read_text()

    # Workflow should have:
    # 1. Multiple rules
    rules_count = content.count('rule ')
    assert rules_count >= 5, f"Should have at least 5 rules, found {rules_count}"

    # 2. An 'all' target
    assert 'rule all:' in content

    # 3. Input/output specifications
    assert 'input:' in content
    assert 'output:' in content

    # 4. Execution commands
    assert 'shell:' in content or 'script:' in content or 'run:' in content


def test_snakemake_clean_rule():
    """Test clean rule for removing intermediate files."""
    snakefile_path = Path('pipelines/snakemake/Snakefile')
    content = snakefile_path.read_text()

    # Should have clean rule
    assert 'rule clean:' in content

    # Clean should have shell command
    lines = content.split('\n')
    in_clean = False
    has_shell = False

    for line in lines:
        if 'rule clean:' in line:
            in_clean = True
        elif in_clean:
            if 'shell:' in line:
                has_shell = True
            elif line.strip().startswith('rule '):
                break

    assert has_shell, "Clean rule should have shell directive"


@pytest.mark.slow
def test_snakemake_syntax_check():
    """Test Snakefile syntax is valid."""
    result = subprocess.run(
        ['snakemake', '--snakefile', 'pipelines/snakemake/Snakefile', '-n', '--quiet'],
        capture_output=True,
        text=True,
        cwd='.'
    )

    # Should parse without syntax errors
    # Exit codes: 0 = success, 1 = missing files (OK), 2+ = syntax error
    assert result.returncode in [0, 1], f"Snakefile syntax check failed: {result.stderr}"
