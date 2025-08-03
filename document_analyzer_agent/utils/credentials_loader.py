"""
Credentials loader module for document analyzer agent.

This module provides functionality to load credentials from a properties file.
"""

import configparser
import logging
import os

def load_credentials(credentials_file):
    """
    Load credentials from a properties file.
    
    Args:
        credentials_file (str): Path to the credentials file
        
    Returns:
        dict: Dictionary containing the credentials
    """
    credentials = {
        "LANGFUSE_PUBLIC_KEY": None,
        "LANGFUSE_SECRET_KEY": None,
        "LANGFUSE_HOST": None
    }
    
    if not os.path.exists(credentials_file):
        logging.warning(f"Credentials file not found: {credentials_file}")
        return credentials
    
    try:
        config = configparser.ConfigParser()
        config.read(credentials_file)
        
        if 'langfuse' in config:
            for key in credentials.keys():
                if key.lower() in config['langfuse']:
                    credentials[key] = config['langfuse'][key.lower()]
        
        logging.info(f"Loaded credentials from {credentials_file}")
    except Exception as e:
        logging.error(f"Error loading credentials: {str(e)}")
    
    return credentials
