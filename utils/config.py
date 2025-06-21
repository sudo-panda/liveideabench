"""
Configuration File Processing Module

Includes API key management, general configuration items, and environment variable processing logic
"""

import os
from typing import Dict, List, Optional

# Define the supported model providers
PROVIDER_NAMES = ["openrouter", "ollama", "stepfun", "gemini", "aigcbest", "vllm", "default"]

# Define the critic models (stronger models)
CRITIC_MODELS = [
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",

    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",

    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",

    "mistralai/Mistral-7B-Instruct-v0.3",
]

IDEA_MODELS = [
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",

    "Qwen/Qwen3-14B",
    "Qwen/Qwen3-8B",
    "Qwen/Qwen2.5-Math-72B-Instruct",
    "Qwen/Qwen2-72B",
    "Qwen/Qwen2.5-VL-72B-Instruct",

    "meta-llama/Llama-4-Scout-17B-16E-Instruct",

    "microsoft/Phi-4-reasoning-plus",

    "tiiuae/falcon-40b-instruct",
] + CRITIC_MODELS

class Config:
    """Configuration class responsible for loading and managing API keys and other configuration items"""

    def __init__(self):
        # Load keys from environment variables or apikey file
        self.api_keys = self._load_api_keys()
        
        # Default values
        self.default_provider = "vllm"
        
        # Mapping from model names to providers
        self.model_provider_mapping = {
            # Mapping for Ollama models
            "dracarys": "ollama",
            "6cf/": "ollama",
            # Gemini models use aigcbest by default
            "gemini": "aigcbest",
            "step-2-16k-202411": "stepfun"
            # Other mappings can be dynamically added at runtime
        }

        self.samples_for_hallucination = 1  # Number of samples to generate for hallucination detection

    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from apikey file and environment variables"""
        # Initialize default values
        keys = {
            "openrouter": None,
            "stepfun": None,
            "gemini": [],
            "aigcbest": None,
        }
        
        # Load from environment variables
        if os.getenv("OPENROUTER_API_KEY"):
            keys["openrouter"] = os.getenv("OPENROUTER_API_KEY")
        if os.getenv("STEP_API_KEY"):
            keys["stepfun"] = os.getenv("STEP_API_KEY")
        if os.getenv("GEMINI_API_KEYS"):
            # Assume the environment variable is comma-separated
            keys["gemini"] = os.getenv("GEMINI_API_KEYS").split(",")
        if os.getenv("AIGCBEST_API_KEY"):
            keys["aigcbest"] = os.getenv("AIGCBEST_API_KEY")
            
        # Load from apikey file
        try:
            with open("apikey", "r") as f:
                content = f.read().strip()
                if not keys["openrouter"]:
                    keys["openrouter"] = content
        except (FileNotFoundError, IOError):
            pass
            
        # Ensure at least one valid API key is found
        # if not keys["openrouter"]:
        #     raise ValueError("No valid OpenRouter API key found, please provide one in the apikey file or environment variable")
            
        return keys
        
    def get_api_key(self, provider: str) -> str:
        """Get the API key for the specified provider"""
        if provider == "gemini":
            # For Gemini, randomly select one of the keys
            import random
            if not self.api_keys["gemini"]:
                raise ValueError("No valid Gemini API keys found")
            return random.choice(self.api_keys["gemini"])
        return self.api_keys.get(provider)
        
    def get_provider_for_model(self, model_name: str) -> str:
        """Determine the provider to use based on the model name"""
        # Check for direct matches
        for prefix, provider in self.model_provider_mapping.items():
            if prefix in model_name.lower():
                return provider
                
        # No match found, return the default provider
        return self.default_provider
        
    def set_default_provider(self, provider: str) -> None:
        """Set the default provider"""
        if provider not in PROVIDER_NAMES:
            raise ValueError(f"Unsupported provider: {provider}. Supported providers are: {', '.join(PROVIDER_NAMES)}")
        self.default_provider = provider

    def set_samples_for_hallucination(self, num_samples: int) -> None:
        """Set the number of samples to generate for hallucination detection"""
        if num_samples <= 0:
            raise ValueError("Number of samples must be a positive integer")
        self.samples_for_hallucination = num_samples


# Create a global config instance
config = Config()