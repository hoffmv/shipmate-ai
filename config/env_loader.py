"""
Shipmate Config Loader
Loads environment configuration values from OS variables or .env files.
"""

import os

def get_env_var(key, default=""):
    return os.getenv(key, default)
