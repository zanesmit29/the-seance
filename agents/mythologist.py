"""
The Mythologist — openbmb/MiniCPM3-4B
Ancient, folkloric, feeling-forward. Channels impossible concepts as oral tradition fragments.
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

MYTHOLOGIST_PROMPT = Path("prompts/mythologist.txt").read_text()

MOCK_RESPONSES = {
    "default": "Before the rivers had names, there was a word for this. The elder stones carried it. To speak it aloud was to leave something behind — not lost, but released into the roots of the oldest tree.",
    "color": "The weavers of the first sky made it on the last morning. Only the blind could see it. When light learned to end, this was the color it chose.",
    "sound": "A crow that remembers every silence knew this sound. It was the noise between heartbeats before hearts existed. The deep caves still hold an echo of it.",
}

class MythologistAgent:
    def __init__(self):
        self.model_id = "openbmb/MiniCPM3-4B"
        self._model: Any = None
        self._tokenizer: Any = None

    def _load(self):
        if self._model is None:
            import torch
            from transformers.models.auto.modeling_auto import AutoModelForCausalLM
            from transformers.models.auto.tokenization_auto import AutoTokenizer
            from transformers.utils.quantization_config import BitsAndBytesConfig

            print("[Mythologist] Loading MiniCPM3-4B (4-bit)...\n")
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_id, trust_remote_code=True, token=os.getenv("HF_TOKEN")
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                trust_remote_code=True,
                quantization_config=bnb_config,
                device_map="auto",
                token=os.getenv("HF_TOKEN"),
            )

    def _unload(self):
        if self._model is not None:
            import torch
            del self._model
            self._model = None
            if self._tokenizer is not None:
                del self._tokenizer
                self._tokenizer = None
            torch.cuda.empty_cache()
            print("[Mythologist] Model unloaded.")

    def channel(self, concept: str) -> str:
        if is_mock_mode():
            for key, response in MOCK_RESPONSES.items():
                if key in concept.lower():
                    return response
            return MOCK_RESPONSES["default"]

        self._load()
        messages = [
            {"role": "system", "content": MYTHOLOGIST_PROMPT},
            {"role": "user", "content": f"Channel this concept: {concept}"},
        ]

        tokenized_chat = self._tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        )

        tokenized_chat = {k: v.to("cuda:0") for k, v in tokenized_chat.items()}

        output = self._model.generate(
            **tokenized_chat,
            max_new_tokens=100,
            temperature=0.8,
            repetition_penalty=1.2,
            do_sample=True,
        )
        input_tokens = tokenized_chat["input_ids"].shape[-1]
        generated_tokens = output[0][input_tokens:]
        text = self._tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        self._unload()
        if "</think>" in text:
            text = text.split("</think>")[-1].strip()
        return text

if __name__ == "__main__":
    mythologist = MythologistAgent()
    concept = "the last color light ever made"
    print(f"Concept: {concept}")
    mythologist_output = mythologist.channel(concept)
    print(f"Mythologist Output:\n{mythologist_output}")