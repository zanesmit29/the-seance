"""
The Séance Pipeline
Orchestrates: Scientist → Mythologist → FLUX (chained prompt)
Returns a complete artifact: scientist_text, mythologist_text, image_path
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents.scientist import ScientistAgent
from agents.mythologist import MythologistAgent
from agents.dreamer import DreamerAgent
from config import load_env
from prompts.flux_constructor import build_flux_prompt

load_env()

class SeancePipeline:
    def __init__(self):
        self.scientist = ScientistAgent()
        self.mythologist = MythologistAgent()
        self.dreamer = DreamerAgent()

    def run(self, concept: str) -> dict:
        """
        Public interface for the pipeline.
        Returns: {scientist_text, mythologist_text, image_path}
        """
        artifact = self.summon(concept)
        return {
            "scientist_text": artifact["scientist_text"],
            "mythologist_text": artifact["mythologist_text"],
            "image_path": artifact["image_path"],
        }

    def summon(self, concept: str) -> dict:
        """
        Summon the form of a concept that doesn't exist.
        Returns: {scientist_text, mythologist_text, flux_prompt, image_path, error}
        """
        artifact = {
            "concept": concept,
            "scientist_text": None,
            "mythologist_text": None,
            "flux_prompt": None,
            "image_path": None,
            "error": None,
        }

        # Step 1: The Scientist channels the concept
        print(f"[Pipeline] Scientist channeling: {concept}")
        try:
            artifact["scientist_text"] = self.scientist.channel(concept)
        except Exception as e:
            artifact["scientist_text"] = f"[Signal lost: {str(e)[:60]}]"
            artifact["error"] = str(e)

        # Step 2: The Mythologist channels the concept
        print(f"[Pipeline] Mythologist channeling: {concept}")
        try:
            artifact["mythologist_text"] = self.mythologist.channel(concept)
        except Exception as e:
            artifact["mythologist_text"] = f"[The old words failed: {str(e)[:60]}]"
            if not artifact["error"]:
                artifact["error"] = str(e)

        # Step 3: Build chained FLUX prompt from both text outputs
        flux_params = build_flux_prompt(
            artifact["scientist_text"] or "",
            artifact["mythologist_text"] or "",
            concept,
        )
        artifact["flux_prompt"] = flux_params["prompt"]

        # Step 4: The Dreamer generates the image
        print(f"[Pipeline] Dreamer visualising with prompt: {flux_params['prompt'][:80]}...")
        try:
            artifact["image_path"] = self.dreamer.dream(flux_params)
        except Exception as e:
            artifact["image_path"] = None
            if not artifact["error"]:
                artifact["error"] = str(e)

        return artifact

if __name__ == "__main__":
    pipeline = SeancePipeline()
    result = pipeline.summon("the sound a shadow makes")
    print("\nArtifact:")
    print("Scientist:", result["scientist_text"])
    print("Mythologist:", result["mythologist_text"])
    print("FLUX prompt:", result["flux_prompt"])
    print("Image:", result["image_path"])
