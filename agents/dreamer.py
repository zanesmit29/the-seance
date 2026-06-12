"""
The Dreamer — black-forest-labs/FLUX.1-schnell
Generates the visual form of a concept. Prompt chained from Scientist + Mythologist outputs.
301K downloads | Apache 2.0 | ~12B params
"""
import os
from pathlib import Path

MOCK_IMAGE_PATH = "assets/mock_artifact.png"

class DreamerAgent:
    def __init__(self):
        self.model_id = "black-forest-labs/FLUX.1-schnell"
        self._pipe = None

    def _load(self):
        if not self._pipe:
            from diffusers import FluxPipeline
            import torch
            print("[Dreamer] Loading FLUX.1-schnell...")
            self._pipe = FluxPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.bfloat16,
                token=os.getenv("HF_TOKEN"),
            )
            self._pipe.enable_model_cpu_offload()

    def _unload(self):
        if self._pipe:
            import torch
            del self._pipe
            self._pipe = None
            torch.cuda.empty_cache()
            print("[Dreamer] Model unloaded.")

    def dream(self, flux_params: dict, output_path: str = "output/artifact_image.png") -> str:
        if os.getenv("MOCK_MODE", "true").lower() == "true":
            # Return mock image if it exists, else generate a placeholder
            if Path(MOCK_IMAGE_PATH).exists():
                return MOCK_IMAGE_PATH
            return _generate_placeholder(output_path)

        self._load()
        import torch
        image = self._pipe(
            prompt=flux_params["prompt"],
            negative_prompt=flux_params.get("negative_prompt", ""),
            num_inference_steps=flux_params.get("num_inference_steps", 4),
            guidance_scale=flux_params.get("guidance_scale", 0.0),
            width=flux_params.get("width", 768),
            height=flux_params.get("height", 512),
            generator=torch.Generator().manual_seed(42),
        ).images[0]
        self._unload()

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
