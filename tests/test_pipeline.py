import os
import pytest
os.environ["MOCK_MODE"] = "true"

from pipeline.seance_pipeline import SeancePipeline
from prompts.flux_constructor import build_flux_prompt, extract_key_phrases, extract_mythic_image

@pytest.fixture
def pipeline():
    return SeancePipeline()

def test_summon_returns_all_fields(pipeline):
    result = pipeline.summon("the sound a shadow makes")
    assert result["scientist_text"] is not None
    assert result["mythologist_text"] is not None
    assert result["flux_prompt"] is not None
    assert len(result["scientist_text"]) > 10
    assert len(result["mythologist_text"]) > 10

def test_summon_different_concepts(pipeline):
    r1 = pipeline.summon("the weight of a forgotten name")
    r2 = pipeline.summon("the last color light ever made")
    assert r1["scientist_text"] != r2["scientist_text"] or r1["mythologist_text"] != r2["mythologist_text"]

def test_flux_prompt_not_empty(pipeline):
    result = pipeline.summon("the door before doors existed")
    assert len(result["flux_prompt"]) > 10
    assert len(result["flux_prompt"]) <= 210  # cap check with small buffer

def test_flux_constructor_chaining():
    sci = "Mass: 0.0g. Detectable only by absence. Classification: phantom datum."
    myth = "Before rivers had names, a crow remembered this. The elder stones carried it."
    params = build_flux_prompt(sci, myth, "test concept")
    assert "prompt" in params
    assert "negative_prompt" in params
    assert params["guidance_scale"] == 0.0  # FLUX.1-schnell requirement
    assert params["num_inference_steps"] == 4

def test_partial_failure_does_not_crash(pipeline):
    """Pipeline should return partial artifact even if one model fails."""
    result = pipeline.summon("a memory that belongs to no one")
    assert result["concept"] == "a memory that belongs to no one"
    # No uncaught exception — partial output is acceptable

def test_run_returns_required_fields(pipeline):
    """run() must return {scientist_text, mythologist_text, image_path}."""
    result = pipeline.run("the shape of a forgotten promise")
    assert set(result.keys()) == {"scientist_text", "mythologist_text", "image_path"}
    assert result["scientist_text"] is not None
    assert result["mythologist_text"] is not None
    assert result["image_path"] is not None
    assert len(result["scientist_text"]) > 10
    assert len(result["mythologist_text"]) > 10
