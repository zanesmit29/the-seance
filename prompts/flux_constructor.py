"""
FLUX Prompt Constructor
Chains Scientist + Mythologist text outputs into a FLUX.1-schnell prompt.
The image must feel like a visual synthesis of both voices — not a literal illustration.
"""
import re

# Dynamic style suffixes based on mood/tone
STYLE_SUFFIXES = [
    "dreamlike atmospheric surreal dark watercolor ultra-detailed cinematic lighting",
    "ethereal luminous abstract oil painting textured moody cinematic atmosphere",
    "haunting impressionist fragments fading light soft focus mysterious ambient",
    "otherworldly geometric abstraction crystalline forms shifting luminescence",
    "spectral watercolor dissolving edges soft chiaroscuro profound stillness",
]

NEGATIVE_PROMPT = "realistic photographic text watermark blurry ugly low quality cartoon anime bright cheerful"

def extract_tone_words(text: str) -> list[str]:
    """Extract emotional/atmospheric words that hint at visual mood."""
    tone_map = {
        r"\b(ancient|old|elder|forgotten|lost|hidden|sealed|sacred)\b": "ethereal timeless",
        r"\b(cold|dark|black|void|absence|empty|silence|whisper)\b": "somber moody",
        r"\b(crystalline|geometric|sharp|precise|measurement|classification)\b": "abstract structured",
        r"\b(breath|dance|flow|rustle|echo|resonance)\b": "fluid dynamic",
        r"\b(shadow|twilight|dusk|threshold|boundary|edge)\b": "liminal transitional",
    }
    detected = []
    for pattern, mood in tone_map.items():
        if re.search(pattern, text.lower()):
            detected.append(mood)
    return detected[:2]  # Keep top 2 to avoid prompt bloat

def extract_key_phrases(text: str, max_phrases: int = 3) -> list[str]:
    """Extract noun-heavy phrases from Scientist output (phenomena, measurements, classifications)."""
    # Strip measurement patterns, keep conceptual nouns
    text = re.sub(r"\d+\.?\d*[a-zA-Z%]+", "", text)  # remove units like 0.0g, 120ms
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 10]
    # Take last word(s) of each sentence as conceptual anchors
    phrases = []
    for s in sentences[:max_phrases]:
        words = s.split()
        if words:
            phrases.append(" ".join(words[-3:]).lower().strip(".,;:"))
    return phrases

def extract_mythic_image(text: str) -> str:
    """Extract the dominant creature or image from Mythologist output."""
    # Look for nouns following: a, an, the, one
    matches = re.findall(r"\b(?:a|an|the|one)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)", text.lower())
    # Filter out common stop words
    stops = {"time", "word", "thing", "way", "place", "moment", "day", "night", "year"}
    candidates = [m for m in matches if m.split()[0] not in stops]
    return candidates[0] if candidates else "ancient form"

def build_flux_prompt(scientist_text: str, mythologist_text: str, concept: str) -> dict:
    """
    Build a FLUX.1-schnell prompt chained from both text outputs.
    Blends Scientist precision with Mythologist imagination in unexpected visual language.
    Returns dict with prompt and negative_prompt.
    """
    scientist_phrases = extract_key_phrases(scientist_text)
    mythic_image = extract_mythic_image(mythologist_text)
    tone_hints = extract_tone_words(scientist_text + " " + mythologist_text)
    
    # Choose style based on detected tone, or cycle through them
    style_idx = hash(concept) % len(STYLE_SUFFIXES)
    style_suffix = STYLE_SUFFIXES[style_idx]
    
    # Weave the elements together more poetically
    phenomena = ", ".join(scientist_phrases) if scientist_phrases else concept
    tone_layer = " ".join(tone_hints) if tone_hints else ""
    
    # Build prompt by fusing voices: mythic image + phenomena + mood + style
    if tone_layer:
        prompt = f"{mythic_image}, {phenomena}, rendered as {tone_layer}, {style_suffix}"
    else:
        prompt = f"{mythic_image}, {phenomena}, {style_suffix}"

    # Cap at 200 characters for optimal FLUX.1-schnell performance
    if len(prompt) > 200:
        prompt = prompt[:197] + "..."

    return {
        "prompt": prompt,
        "negative_prompt": NEGATIVE_PROMPT,
        "num_inference_steps": 4,  # schnell optimal: 1-4 steps
        "guidance_scale": 0.0,     # schnell: guidance_scale must be 0
        "width": 768,
        "height": 512,
    }

if __name__ == "__main__":
    # Test
    sci = "Mass: 0.0g. Detectable only by absence of referential load. Half-life: variable. Classification: phantom datum."
    myth = "Before the rivers had names, there was a word for this. The elder stones carried it."
    result = build_flux_prompt(sci, myth, "the weight of a forgotten name")
    print("FLUX prompt:", result["prompt"])
    print("Negative:", result["negative_prompt"])
