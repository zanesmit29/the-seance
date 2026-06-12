"""
The Mythologist — openbmb/MiniCPM3-4B
Ancient, folkloric, feeling-forward. Channels impossible concepts as oral tradition fragments.
"""
import os
from pathlib import Path

MYTHOLOGIST_PROMPT = Path("prompts/mythologist.txt").read_text()

MOCK_RESPONSES = {
    "default": "Before the rivers had names, there was a word for this. The elder stones carried it. To speak it aloud was to leave something behind — not lost, but released into the roots of the oldest tree.",
    "color": "The weavers of the first sky made it on the last morning. Only the blind could see it. When light learned to end, this was the color it chose.",
    "sound": "A crow that remembers every silence knew this sound. It was the noise between heartbeats before hearts existed. The deep caves still hold an echo of it.",
}

class MythologistAgent:
    def __init__(self):
        self.model_id = "openbmb/MiniCPM3-4B"
        self._pipeline = None

    def _load(self):
        if not self._pipeline:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            print("[Mythologist] Loading MiniCPM3-4B...")
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_id, trust_remote_code=True, token=os.getenv("HF_TOKEN")
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_id, trust_remote_code=True,
                torch_dtype=torch.bfloat16, device_map="auto",
                token=os.getenv("HF_TOKEN"),
            )

    def _unload(self):
        if self._pipeline or hasattr(self, "_model"):
            import torch
            if hasattr(self, "_model"):
                del self._model
                del self._tokenizer
            torch.cuda.empty_cache()
            print("[Mythologist] Model unloaded.")

    def channel(self, concept: str) -> str:
        if os.getenv("MOCK_MODE", "true").lower() == "true":
            for key, response in MOCK_RESPONSES.items():
                if key in concept.lower():
                    return response
            return MOCK_RESPONSES["default"]

        self._load()
        messages = [
            {"role": "system", "content": MYTHOLOGIST_PROMPT},
            {"role": "user", "content": f"Channel this concept: {concept}"},
        ]
        response = self._model.chat(
            self._tokenizer,
            msgs=messages,
            tokenize=False,
            sampling=True,
            temperature=0.8,
            max_new_tokens=80,
        )
        self._unload()
        return response.strip()
