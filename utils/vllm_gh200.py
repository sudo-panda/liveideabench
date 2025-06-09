VLLM_MODEL_CONFIGS = {
    "DEFAULT": {
        "tensor_parallel_size": 4,
    },

    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.8,
    },
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.9,
    },
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B": {
        "tensor_parallel_size": 4,
        "max_model_len": 2048,
        "gpu_memory_utilization": 0.90,
    },

    "Qwen/Qwen3-32B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "rope_scaling": {
            "rope_type": "yarn", 
            "factor":4.0, 
            "original_max_position_embeddings":32768
        },
        "gpu_memory_utilization": 0.9,
    },
    "Qwen/Qwen3-14B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "rope_scaling": {
            "rope_type": "yarn", 
            "factor":4.0, 
            "original_max_position_embeddings":32768
        },
        "gpu_memory_utilization": 0.9,
    },
    "Qwen/Qwen3-8B": {
        "tensor_parallel_size": 2,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "rope_scaling": {
            "rope_type": "yarn", 
            "factor":4.0, 
            "original_max_position_embeddings":32768
        },
        "gpu_memory_utilization": 0.85,
    },
    "Qwen/Qwen3-30B-A3B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "rope_scaling": {
            "rope_type": "yarn", 
            "factor":4.0, 
            "original_max_position_embeddings":32768
        },
        "gpu_memory_utilization": 0.9,
    },
    "Qwen/Qwen3-235B-A22B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "rope_scaling": {
            "rope_type": "yarn",
            "factor": 4.0,
            "original_max_position_embeddings": 32768
        },
        "gpu_memory_utilization": 0.9
    },
    "Qwen/Qwen2.5-72B-Instruct": {
        "gpu_memory_utilization": 0.8,
        "max_model_len": 32768,
        "dtype": "bfloat16",
    },
    "Qwen/Qwen2.5-14B-Instruct": {
        "gpu_memory_utilization": 0.92,
        "max_model_len": 4096,
    },
    "Qwen/Qwen1.5-14B-Chat": {
        "gpu_memory_utilization": 0.90,
        "max_model_len": 2048,
    },

    "meta-llama/Llama-4-Scout-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 10_000_000,
        "gpu_memory_utilization": 0.9
    },
    "meta-llama/Llama-4-Maverick-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 1_000_000,
        "gpu_memory_utilization": 0.9
    },
    "meta-llama/Llama-3.3-70B-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "gpu_memory_utilization": 0.9
    },

    "microsoft/Phi-4-reasoning-plus": {
        "tensor_parallel_size": 2,
        "max_model_len": 2048,
        "gpu_memory_utilization": 0.85,
        "swap_space": 16,
    },

    "mistralai/Mistral-7B-Instruct-v0.3": {
        "gpu_memory_utilization": 0.92,
        "max_model_len": 2048,
        "tokenizer_mode": "mistral",
    },

    "tiiuae/falcon-40b-instruct": {
        "tensor_parallel_size": 4,
        "max_model_len": 2048,
        "gpu_memory_utilization": 0.88,
    },
}