from typing import Dict, Any, List, Optional

def validate_column_schema(columns: Dict[str, Dict[str, Any]]) -> bool:
    """
    Validates that columns conform to the expected schema format.
    
    Expected format:
    {
        "column_name": {"type": "string|number|boolean|date", "required": true|false},
        ...
    }
    """
    if not isinstance(columns, dict):
        return False
        
    valid_types = {"string", "number", "integer", "boolean", "date"}
    
    for column_name, column_def in columns.items():
        # Column name must be a string
        if not isinstance(column_name, str):
            return False
            
        # Column definition must be a dict
        if not isinstance(column_def, dict):
            return False
            
        # Type is required
        if "type" not in column_def:
            return False
            
        # Type must be one of the valid types
        if column_def["type"] not in valid_types:
            return False
            
        # If required is present, it must be a boolean
        if "required" in column_def and not isinstance(column_def["required"], bool):
            return False
    
    return True

def validate_row_data(data: Dict[str, Any], column_schema: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    Validates row data against the table's column schema.
    Returns a list of validation errors, or empty list if valid.
    """
    errors = []
    
    # Check required fields
    for column_name, column_def in column_schema.items():
        if column_def.get("required", False) and column_name not in data:
            errors.append(f"Required column '{column_name}' is missing")
    
    # Check data types
    for column_name, value in data.items():
        # Skip if column is not in schema
        if column_name not in column_schema:
            errors.append(f"Column '{column_name}' is not defined in the table schema")
            continue
            
        column_type = column_schema[column_name]["type"]
        
        # Check data type
        if column_type == "string" and not isinstance(value, str):
            errors.append(f"Column '{column_name}' must be a string")
        elif column_type == "number" and not isinstance(value, (int, float)):
            errors.append(f"Column '{column_name}' must be a number")
        elif column_type == "integer" and not isinstance(value, int):
            errors.append(f"Column '{column_name}' must be an integer")
        elif column_type == "boolean" and not isinstance(value, bool):
            errors.append(f"Column '{column_name}' must be a boolean")
        elif column_type == "date":
            # Basic ISO format date check
            if not isinstance(value, str) or not _is_valid_date_format(value):
                errors.append(f"Column '{column_name}' must be a valid ISO date string (YYYY-MM-DD)")
    
    return errors

def _is_valid_date_format(date_str: str) -> bool:
    """Simple check for YYYY-MM-DD format"""
    try:
        import datetime
        datetime.datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False