"""Data validation utilities."""
import pandas as pd
import jsonschema
from typing import Dict, List

class DataValidator:
    """Validate data against schemas."""
    
    def validate_json_schema(self, data: Dict, schema: Dict) -> bool:
        """Validate JSON data against schema."""
        try:
            jsonschema.validate(instance=data, schema=schema)
            return True
        except jsonschema.ValidationError:
            return False
    
    def validate_dataframe_schema(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Check if DataFrame has required columns."""
        return all(col in df.columns for col in required_columns)
    
    def check_missing_values(self, df: pd.DataFrame, threshold: float = 0.1) -> Dict:
        """Check for excessive missing values."""
        missing_pct = df.isnull().mean()
        return {col: pct for col, pct in missing_pct.items() if pct > threshold}
