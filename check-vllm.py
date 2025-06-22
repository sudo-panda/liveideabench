import sys
import os
if os.environ.get("MACHINE_NAME") == "clariden":
    from utils.vllm_gh200 import CLARIDEN_VLLM_MODEL_CONFIGS as VLLM_MODEL_CONFIGS
elif os.environ.get("MACHINE_NAME") == "helios":
    from utils.vllm_gh200 import HELIOS_VLLM_MODEL_CONFIGS as VLLM_MODEL_CONFIGS
from utils.LLM import BaseLLM
import traceback
import time
from concurrent import futures

class VLLMCheck(BaseLLM):
    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name, "vllm", **kwargs)
        if self.provider == "vllm":
            self.sampling_params = {
                "temperature": 0.7,
                "max_tokens": 100,
            }

    def check_model(self, prompt):
        """Check if the model is available and can be loaded."""
        return self.completion(prompt)

ADDITIONAL_MODELS = []

def main():
    model_names = [ k for k in VLLM_MODEL_CONFIGS.keys() if not VLLM_MODEL_CONFIGS[k].get("NOT_SUPPORTED", False) ]
    model_names.remove("DEFAULT")
    model_names.extend(ADDITIONAL_MODELS)
    model_names = list(dict.fromkeys(model_names)) # Remove duplicates without changing order

    prompt = "In one paragraph, tell me 10 facts about the number 42 in a humorous way."

    skip_till = 0
    for i, model_name in enumerate(model_names):
        if i < skip_till:
            continue
        print(f"\n=== {i} Running model: {model_name} ===")
        print(f"\n\n\n\n\n\n=== Running model: {model_name} ===", file=sys.stderr)
        success = False
        try:
            runtime = time.time()
            llm = VLLMCheck(model_name)
            # outputs = futures.ThreadPoolExecutor().submit(llm.check_model, prompt).result(timeout=10)
            outputs = llm.check_model(prompt)
            runtime = time.time() - runtime
            if not outputs:
                print(f"[!] Model '{model_name}' returned no output.")
            else:
                print(f"[✓] Output from '{model_name}':\n{outputs}\n")
                success = True
        except futures.TimeoutError as e: 
            print("[!] TimeoutError: Model did not respond within the expected time limit.")
        except RuntimeError as e:
            if "CUDA out of memory" in str(e):
                print(f"[!] [OOM] CUDA out of memory for model '{model_name}', attempting recovery.")
            else:
                print(f"[!] RuntimeError for model '{model_name}': {e}")
                traceback.print_exc()
        except Exception as e:
            print(f"[!] Failed to run model '{model_name}': {e}")
            traceback.print_exc()
        finally:
            with open("logs/vllm_runtimes.txt", "a") as f:
                if success:
                    f.write(f"{i:>3d} | {model_name:<50}: {runtime:.3f} seconds\n")
                else:
                    f.write(f"{i:>3d} | {model_name:<50}: Failed\n")
            if 'llm' in locals():
                llm.cleanup()
                del llm

if __name__ == "__main__":
    main()