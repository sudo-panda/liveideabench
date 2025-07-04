"""
General utility function module

Contains general utility functions such as hash generation and timeout handling
"""

import hashlib
import signal
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# Generate a stable hash value, ensuring the same text always produces the same hash value
def stable_hash(text):
    """
    Generate a stable MD5 hash value for the input text
    
    Args:
        text: The text to be hashed
        
    Returns:
        The MD5 hash value of the text (hexadecimal string)
    """
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()

# Timeout handling related functions
def timeout_handler(signum, frame):
    """Handler triggered when function execution times out"""
    raise TimeoutError("Function call timed out")

def run_with_timeout(func, timeout, *args, **kwargs):
    """
    Run a function within a specified time, raising an exception if it times out
    
    Args:
        func: The function to execute
        timeout: Timeout duration (seconds)
        *args, **kwargs: Arguments to pass to func
        
    Returns:
        The result of the function execution
        
    Raises:
        TimeoutError: If the function execution exceeds the specified time
    """
    # Set the signal handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        result = func(*args, **kwargs)
    finally:
        # Cancel the alarm
        signal.alarm(0)
    return result

def append_content_new(txt_path, content_new):
    """
    Append new content to the specified text file
    
    Args:
        txt_path: Target file path
        content_new: The content to append
    """
    with open(txt_path, "a", encoding='utf-8') as f:
        f.write(content_new)

def load_prompt_input(dataset_name: str = "proofnet") -> List[str]:
    """Load prompt input from the specified dataset

    Args:
        dataset_name: The dataset to load prompts for

    Returns:
        List of prompt input
    """
    import importlib

    try:
        config_module = importlib.import_module(f"dataset_configs.{dataset_name}.config")
        load_prompt_input_fn = config_module.load_prompt_input
    except ImportError as e:
        logger.error(f"Failed to import config module for dataset '{dataset_name}'")
        raise e
    except AttributeError as e:
        logger.error(f"Config module for dataset '{dataset_name}' does not have 'load_prompt_input' function")
        raise e

    if not callable(load_prompt_input_fn):
        raise TypeError(f"Function 'load_prompt_input' in dataset '{dataset_name}' is not callable")
    
    return load_prompt_input_fn()

def load_prompts(dataset_name: str = "proofnet") -> Dict[str, Dict[str, str]]:
    """Load prompt templates

    Args:
        dataset_name: The dataset to load prompts for

    Returns:
        Dictionary of prompt templates
    """
    import importlib

    try:
        config_module = importlib.import_module(f"dataset_configs.{dataset_name}.config")
        load_prompts_fn = config_module.load_prompts
    except ImportError as e:
        logger.error(f"Failed to import config module for dataset '{dataset_name}'")
        raise e
    except AttributeError as e:
        logger.error(f"Config module for dataset '{dataset_name}' does not have 'load_prompts' function")
        raise e

    if not callable(load_prompts_fn):
        raise TypeError(f"Function 'load_prompts' in dataset '{dataset_name}' is not callable")
    
    return load_prompts_fn()


def clean_text(text: str) -> str:
    """Clean text by removing unnecessary whitespace

    Args:
        text: Raw text

    Returns:
        Cleaned text
    """
    # Remove newlines, carriage returns, and tabs
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Replace multiple spaces with a single space
    return ' '.join(text.split())