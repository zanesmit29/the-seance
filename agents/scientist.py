"""
The Scientist — nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16
Cold, precise, field-note voice. Channels impossible concepts as measurement and classification.
"""
import os
from pathlib import Path

SCIENTIST_PROMPT = Path("prompts/scientist.txt").read_text()

MOCK_RESPONSES = {
    "default": "Mass: 0.0g. Detectable only by absence of referential load in adjacent neural pathways. Half-life: variable. Classification: phantom datum. No known containment method.",
    "color": "Wavelength: unmeasurable. Spectral position: post-visible. Observed once at the boundary of photon decay. Classification: terminal chromatic event.",
    "sound": "Frequency: 0hz. Waveform: flat. Detectable only at perception threshold when ambient noise reaches absolute zero. Duration: indefinite.",
}

class ScientistAgent:
    def __init__(self):
        self.model_id = "nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16"
        self._pipeline = None

    def _load(self):
        if not self._pipeline:
            from transformers import pipeline
            print("[Scientist] Loading Nemotron-Nano-4B...")
            self._pipeline = pipeline(
                "text-generation",
                model=self.model_id,
                torch_dtype="auto",
                device_map="auto",
                token=os.getenv("HF_TOKEN"),
            )

    def _unload(self):
        """Unload model to free VRAM for next model in chain."""
        if self._pipeline:
            import torch
            del self._pipeline
            self._pipeline = None
            torch.cuda.empty_cache()
            print("[Scientist] Model unloaded.")

    def channel(self, concept: str) -> str:
        if os.getenv("MOCK_MODE", "true").lower() == "true":
            for key, response in MOCK_RESPONSES.items():
                if key in concept.lower():
                    return response
            return MOCK_RESPONSES["default"]

        self._load()
        messages = [
            {"role": "system", "content": SCIENTIST_PROMPT},
            {"role": "user", "content": f"Channel this concept: {concept}"},
        ]
        output = self._pipeline(
            messages,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.7,
            pad_token_id=self._pipeline.tokenizer.eos_token_id,
        )
        self._unload()
        return output[0]["generated_text"][-1]["content"].strip()
