#!/usr/bin/env python3
"""
Random seed control and reproducibility management.

This script ensures reproducibility across all data generation scripts
by providing centralized seed management and validation.
"""

import random
import numpy as np
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Global seed for all experiments
GLOBAL_SEED = 42


class ReproducibilityManager:
    """Manage random seeds and ensure reproducibility."""

    def __init__(self, seed: int = GLOBAL_SEED):
        self.seed = seed
        self.seed_registry: Dict[str, int] = {}
        self.execution_log: List[Dict] = []

    def set_global_seed(self, seed: Optional[int] = None):
        """Set global random seed for all libraries."""
        if seed is None:
            seed = self.seed

        random.seed(seed)
        np.random.seed(seed)

        # Try to set torch seed if available
        try:
            import torch
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
        except ImportError:
            pass

        self.log_action("set_global_seed", {"seed": seed})
        print(f"Global random seed set to: {seed}")

    def generate_module_seed(self, module_name: str, offset: int = 0) -> int:
        """Generate a deterministic seed for a specific module."""
        # Hash module name to get deterministic offset
        hash_object = hashlib.md5(module_name.encode())
        hash_int = int(hash_object.hexdigest(), 16)
        module_seed = (self.seed + hash_int + offset) % (2**31 - 1)

        self.seed_registry[module_name] = module_seed
        self.log_action("generate_module_seed", {
            "module": module_name,
            "seed": module_seed,
            "offset": offset
        })

        return module_seed

    def log_action(self, action: str, details: Dict):
        """Log an action for reproducibility tracking."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
        }
        self.execution_log.append(log_entry)

    def save_seed_registry(self, output_path: Path):
        """Save seed registry to file."""
        registry = {
            "global_seed": self.seed,
            "module_seeds": self.seed_registry,
            "generation_timestamp": datetime.now().isoformat(),
            "execution_log": self.execution_log,
        }

        with open(output_path, 'w') as f:
            json.dump(registry, f, indent=2)

        print(f"Seed registry saved to {output_path}")

    def load_seed_registry(self, input_path: Path) -> Dict:
        """Load existing seed registry."""
        with open(input_path) as f:
            registry = json.load(f)

        self.seed = registry["global_seed"]
        self.seed_registry = registry["module_seeds"]

        print(f"Loaded seed registry from {input_path}")
        print(f"Global seed: {self.seed}")
        print(f"Registered modules: {len(self.seed_registry)}")

        return registry

    def validate_reproducibility(self, test_size: int = 1000) -> bool:
        """Validate that random number generation is reproducible."""
        print("Validating reproducibility...")

        # Generate test data with seed
        self.set_global_seed()
        test_data_1 = [random.random() for _ in range(test_size)]
        test_array_1 = np.random.randn(test_size)

        # Reset seed and regenerate
        self.set_global_seed()
        test_data_2 = [random.random() for _ in range(test_size)]
        test_array_2 = np.random.randn(test_size)

        # Compare
        python_match = test_data_1 == test_data_2
        numpy_match = np.allclose(test_array_1, test_array_2)

        if python_match and numpy_match:
            print("✓ Reproducibility validation PASSED")
            self.log_action("validate_reproducibility", {
                "status": "passed",
                "test_size": test_size
            })
            return True
        else:
            print("✗ Reproducibility validation FAILED")
            if not python_match:
                print("  - Python random mismatch")
            if not numpy_match:
                print("  - NumPy random mismatch")
            self.log_action("validate_reproducibility", {
                "status": "failed",
                "test_size": test_size
            })
            return False

    def get_summary(self) -> Dict:
        """Get summary of seed management."""
        return {
            "global_seed": self.seed,
            "registered_modules": len(self.seed_registry),
            "module_names": list(self.seed_registry.keys()),
            "total_actions": len(self.execution_log),
        }


def main():
    """Main execution function."""
    manager = ReproducibilityManager(seed=GLOBAL_SEED)

    # Set global seed
    manager.set_global_seed()

    # Validate reproducibility
    is_reproducible = manager.validate_reproducibility(test_size=10000)

    if not is_reproducible:
        print("\nWARNING: Reproducibility validation failed!")
        return

    # Generate module-specific seeds
    modules = [
        "query_simulation",
        "response_generation",
        "annotation_synthesis",
        "msms_generation",
        "protein_augmentation",
    ]

    print("\nGenerating module-specific seeds...")
    for module in modules:
        seed = manager.generate_module_seed(module)
        print(f"  {module}: {seed}")

    # Save seed registry
    output_dir = Path(__file__).parent.parent
    registry_path = output_dir / "seed_registry.json"
    manager.save_seed_registry(registry_path)

    # Display summary
    print("\n" + "="*60)
    print("REPRODUCIBILITY SUMMARY")
    print("="*60)
    summary = manager.get_summary()
    for key, value in summary.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"{key}: {value}")

    print("\n✓ Reproducibility framework initialized successfully")
    print(f"✓ All random operations will use seed: {GLOBAL_SEED}")
    print(f"✓ Seed registry saved to: {registry_path}")


if __name__ == "__main__":
    main()
