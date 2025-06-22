import subprocess
import requests
import time
import atexit
import signal
from typing import List, Dict, Optional

class VLLMOpenAIWrapper:
    def __init__(
        self,
        model_name: str,
        port: int = 8000,
        server_kwargs: dict = None
    ):
        self.port = port
        self.url = f"http://localhost:{self.port}/v1/chat/completions"
        self.model_name = model_name
        server_kwargs = server_kwargs or {}

        # Default arguments
        args = [
            "python", "-m", "vllm.entrypoints.openai.api_server",
            "--model", model_name,
            "--port", str(self.port)
        ]

        # Add additional args from server_kwargs
        for key, value in server_kwargs.items():
            flag = f"--{key.replace('_', '-')}"
            if isinstance(value, bool):
                if value:
                    args.append(flag)
            else:
                args.extend([flag, str(value)])

        # Launch the vLLM OpenAI-compatible API server
        self.process = subprocess.Popen(args)

        atexit.register(self.cleanup)
        self._wait_until_ready()

    def _wait_until_ready(self, timeout=60):
        start = time.time()
        while time.time() - start < timeout:
            try:
                r = requests.get(f"http://localhost:{self.port}/health")
                if r.status_code == 200:
                    return
            except Exception:
                time.sleep(1)
        raise TimeoutError(f"vLLM API server on port {self.port} did not become ready in {timeout} seconds")

    def generate(self, prompt: str, system_prompt: Optional[str] = None, sampling_params: dict = None) -> dict:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            **(sampling_params or {})
        }

        r = requests.post(self.url, json=payload)
        r.raise_for_status()
        return r.json()

    def cleanup(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()

        print(f"vLLM API server on port {self.port} has been cleaned up.")