"""
observability/env.py

Environment variable utilities.
Configuration is fully driven by environment variables.
"""

import os


def get_env(key: str, default: str = "") -> str:
    """
    Get environment variable or return default value.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)

