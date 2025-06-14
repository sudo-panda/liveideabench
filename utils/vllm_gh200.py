VLLM_MODEL_CONFIGS = {
    "DEFAULT": {
        "tensor_parallel_size": 1,
    },


    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "gpu_memory_utilization": 0.8,
    },
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 4096,
        "gpu_memory_utilization": 0.9,
    },
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B": {
        "tensor_parallel_size": 4,
        "max_model_len": 2048,
        "dtype": "bfloat16",
        "gpu_memory_utilization": 0.90,
    },
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B": {
        "gpu_memory_utilization": 0.9,
        "max_model_len": 4096,
        "dtype": "bfloat16",
    },
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": {
        "gpu_memory_utilization": 0.9,
        "max_model_len": 4096,
        "dtype": "bfloat16",
    },


    "Qwen/Qwen3-32B": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
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
        "max_model_len": 8192,
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
        "max_model_len": 8192,
        "rope_scaling": {
            "rope_type": "yarn", 
            "factor":4.0, 
            "original_max_position_embeddings":32768
        },
        "gpu_memory_utilization": 0.85,
    },
    "Qwen/Qwen3-30B-A3B": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "rope_scaling": {
            "rope_type": "yarn", 
            "factor":4.0, 
            "original_max_position_embeddings":32768
        },
        "gpu_memory_utilization": 0.9,
    },
    "Qwen/Qwen3-235B-A22B": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "rope_scaling": {
            "rope_type": "yarn",
            "factor": 4.0,
            "original_max_position_embeddings": 32768
        },
        "gpu_memory_utilization": 0.9
    },
    "Qwen/Qwen2.5-72B-Instruct": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "gpu_memory_utilization": 0.8,
        "max_model_len": 8192,
        "dtype": "bfloat16",
    },
    "Qwen/Qwen2.5-72B-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.9,
        "enforce_eager": False,
    },
    "Qwen/Qwen2.5-72B": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.9,
        "enforce_eager": False,
    },
    "Qwen/Qwen2.5-Math-72B-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 4096,
        "gpu_memory_utilization": 0.9,
        "enforce_eager": False,
    },
    "Qwen/Qwen2-72B": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.9,
        "enforce_eager": False,
    },
    "Qwen/Qwen2-72B-Instruct": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.9,
        "enforce_eager": False,
    },
    "Qwen/Qwen2.5-VL-72B-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.9,
        "enforce_eager": False,
    },
    "Qwen/Qwen2.5-14B-Instruct": {
        "gpu_memory_utilization": 0.92,
        "max_model_len": 4096,
    },
    "Qwen/Qwen1.5-14B-Chat": {
        "NOT_SUPPORTED": True,

        "gpu_memory_utilization": 0.90,
        "max_model_len": 2048,
    },


    "meta-llama/Llama-4-Scout-17B-16E-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "gpu_memory_utilization": 0.9,
    },
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "gpu_memory_utilization": 0.8,
    },
    "meta-llama/Llama-3.3-70B-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "gpu_memory_utilization": 0.9
    },
    "meta-llama/Meta-Llama-3-70B-Instruct": {
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 8192,
        "gpu_memory_utilization": 0.9
    },


    "microsoft/Phi-4-reasoning-plus": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 2,
        "max_model_len": 2048,
        "gpu_memory_utilization": 0.85,
        "swap_space": 16,
        "dtype": "bfloat16",
    },


    "mistralai/Mistral-7B-Instruct-v0.3": {
        "gpu_memory_utilization": 0.92,
        "max_model_len": 2048,
        "tokenizer_mode": "mistral",
    },
    "mistralai/Mixtral-8x22B-v0.1": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 65536,
        "gpu_memory_utilization": 0.85,
        "enable_chunked_prefill": True,
        "tokenizer": "mistralai/Mixtral-8x22B-v0.1",
        "tokenizer_mode": "mistral",
    },
    "mistralai/Mixtral-8x7B-Instruct-v0.1": {
        "NOT_SUPPORTED": True,
        
        "tensor_parallel_size": 4,
        "dtype": "bfloat16",
        "max_model_len": 32768,
        "gpu_memory_utilization": 0.85,
        "enable_chunked_prefill": True,
        "tokenizer_mode": "mistral",
    },
    "mistralai/Mistral-Small-3.1-24B-Instruct-2503": {
        "NOT_SUPPORTED": True,

        "tensor_parallel_size": 2,
        "pipeline_parallel_size": 1,
        "dtype": "bfloat16",
        "max_model_len": 131072,
        "gpu_memory_utilization": 0.9,
        "enable_chunked_prefill": True,
        "tokenizer_mode": "mistral",
    },
    "mistralai/Magistral-Small-2506": {
        "NOT_SUPPORTED": True,
        
        "tensor_parallel_size": 2,
        "pipeline_parallel_size": 1,
        "dtype": "bfloat16",
        "max_model_len": 40960,
        "gpu_memory_utilization": 0.9,
        "enable_chunked_prefill": True,
        "tokenizer_mode": "mistral",
        "config_format": "mistral",
        "load_format": "mistral",
    },


    "tiiuae/falcon-40b-instruct": {
        "tensor_parallel_size": 4,
        "max_model_len": 2048,
        "gpu_memory_utilization": 0.88,
    },
}