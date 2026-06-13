"""
The Scientist — nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16
Cold, precise, field-note voice. Channels impossible concepts as measurement and classification.
"""
import os
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import is_mock_mode, load_env

load_env()

SCIENTIST_PROMPT = Path("prompts/scientist.txt").read_text()

MOCK_RESPONSES = {
    "default": "Mass: 0.0g. Detectable only by absence of referential load in adjacent neural pathways. Half-life: variable. Classification: phantom datum. No known containment method.",
    "color": "Wavelength: unmeasurable. Spectral position: post-visible. Observed once at the boundary of photon decay. Classification: terminal chromatic event.",
    "sound": "Frequency: 0hz. Waveform: flat. Detectable only at perception threshold when ambient noise reaches absolute zero. Duration: indefinite.",
}

class ScientistAgent:
    def __init__(self):
        self.model_id = "nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16"
        self.fallback_model_id = "Qwen/Qwen2.5-3B-Instruct"
        self.active_model_id = self.model_id
        self._pipeline: Any = None
        self.tokenizer: Any = None

    def _load(self):
        if not self._pipeline:
            import torch
            from transformers.models.auto.modeling_auto import AutoModelForCausalLM
            from transformers.models.auto.tokenization_auto import AutoTokenizer
            from transformers.utils.quantization_config import BitsAndBytesConfig
            print("[Scientist] Loading Nemotron-Nano-4B (4-bit)\n")
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )

            try:
                self.active_model_id = self.model_id
                self._pipeline = AutoModelForCausalLM.from_pretrained(
                    self.active_model_id,
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                    token=os.getenv("HF_TOKEN"),
                )
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.active_model_id,
                    trust_remote_code=True,
                    token=os.getenv("HF_TOKEN"),
                )
            except ImportError as e:
                if "mamba_ssm" in str(e) or "causal_conv1d" in str(e):
                    print(f"[Scientist] Nemotron dependencies missing ({e}). Falling back to {self.fallback_model_id}.")
                    self.active_model_id = self.fallback_model_id
                    self._pipeline = AutoModelForCausalLM.from_pretrained(
                        self.active_model_id,
                        quantization_config=bnb_config,
                        device_map="auto",
                        token=os.getenv("HF_TOKEN"),
                    )
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.active_model_id,
                        token=os.getenv("HF_TOKEN"),
                    )
                else:
                    raise

    def _unload(self):
        """Unload model to free VRAM for next model in chain."""
        if self._pipeline:
            import torch
            del self._pipeline
            self._pipeline = None
            torch.cuda.empty_cache()
            print("[Scientist] Model unloaded.\n")

    def channel(self, concept: str) -> str:
        if is_mock_mode():
            for key, response in MOCK_RESPONSES.items():
                if key in concept.lower():
                    return response
            return MOCK_RESPONSES["default"]

        self._load()
        messages = [
            {"role": "system", "content": SCIENTIST_PROMPT},
            {"role": "user", "content": f"Channel this concept: {concept}"},
        ]
        tokenized_chat = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
            )
        
        tokenized_chat = {k: v.to("cuda:0") for k, v in tokenized_chat.items()}
        
        output = self._pipeline.generate(**tokenized_chat, max_new_tokens=100, temperature=0.8, repetition_penalty=1.2, do_sample=True)
        input_tokens = tokenized_chat["input_ids"].shape[-1]
        generated_tokens = output[0][input_tokens:]
        self._unload()
        text = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        if "</think>" in text:
            text = text.split("</think>")[-1].strip()
        return text

if __name__ == "__main__":
    agent = ScientistAgent()
    test_concepts = ["the sound the last color makes"]
    for concept in test_concepts:
        print(f"Concept: {concept}")
        print(f"Scientist Output: {agent.channel(concept)}\n")
