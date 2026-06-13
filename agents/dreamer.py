"""
The Dreamer — black-forest-labs/FLUX.1-schnell
Generates the visual form of a concept. Prompt chained from Scientist + Mythologist outputs.
301K downloads | Apache 2.0 | ~12B params
"""
import os
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import is_mock_mode, load_env
from huggingface_hub import InferenceClient

load_env()

MOCK_IMAGE_PATH = "assets/mock_artifact.png"

class DreamerAgent:
    def __init__(self):
        self.model_id = "black-forest-labs/FLUX.1-schnell"
        self._client: Any = None

    def _client_or_raise(self) -> InferenceClient:
        if self._client is None:
            token = os.getenv("HF_TOKEN")
            if not token:
                raise RuntimeError("HF_TOKEN is required for Dreamer inference API usage.")
            self._client = InferenceClient(api_key=token)
        return self._client

    def dream(self, flux_params: dict, output_path: str = "output/artifact_image.png") -> str:
        if is_mock_mode():
            # Return mock image if it exists, else generate a placeholder
            if Path(MOCK_IMAGE_PATH).exists():
                return MOCK_IMAGE_PATH
            return _generate_placeholder(output_path)

        print("[Dreamer] Requesting FLUX.1-schnell via Hugging Face Inference API...")
        image = self._client_or_raise().text_to_image(
            prompt=flux_params["prompt"],
            negative_prompt=flux_params.get("negative_prompt", ""),
            model=self.model_id,
            width=flux_params.get("width", 768),
            height=flux_params.get("height", 512),
            guidance_scale=flux_params.get("guidance_scale", 0.0),
            num_inference_steps=flux_params.get("num_inference_steps", 4),
        )

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)
        return output_path

def _generate_placeholder(output_path: str) -> str:
    """Generate a simple dark placeholder image for mock mode."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (768, 512), color=(13, 13, 15))
    draw = ImageDraw.Draw(img)
    draw.text((384, 256), "~ The Dreamer ~", fill=(80, 80, 100), anchor="mm")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    agent = DreamerAgent()
    sample_params = {
        "prompt": "a faint silhouette dissolving into static, cinematic, dark watercolor",
        "negative_prompt": "blurry, text, watermark",
        "num_inference_steps": 4,
        "guidance_scale": 0.0,
        "width": 768,
        "height": 512,
    }
    print("Dreamer Output:", agent.dream(sample_params))
