---
title: The Séance
emoji: ✦
colorFrom: indigo
colorTo: black
sdk: gradio
sdk_version: 4.36.0
app_file: app.py
pinned: true
---

# ✦ The Séance — An Adventure in Thousand Token Wood

> *Name something that doesn't exist. Three entities will channel its form.*

**HuggingFace BuildSmall Hackathon · Thousand Token Wood theme**

---

## What It Is

You type a concept that should not exist — *"the last color light ever made"*, *"the sound a shadow makes"*, *"the weight of a forgotten name"* — and three distinct AI entities channel it back to you simultaneously.

The outputs compose a single artifact card: two text panels and one AI-generated image. Every summoning is unique and unrepeatable.

---

## The Three Entities

| Entity | Personality | Model | Inference | Visual Style |
|--------|------------|-------|-----------|-------------|
| **The Scientist** | Cold, precise, field-note voice | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` (→ Qwen2.5-3B fallback on Windows) | Local 4-bit GPU | Neon green monospace terminal |
| **The Mythologist** | Ancient, folkloric, feeling-forward | `openbmb/MiniCPM3-4B` | Local 4-bit GPU | Purple serif italic, breathing glow |
| **The Dreamer** | Generates the visual form of the concept | `black-forest-labs/FLUX.1-schnell` | HF Inference API | Desaturated, dimmed, animated fog overlay |

**Total: ~20B params. All HuggingFace-native. All within hackathon constraints.**

The FLUX image prompt is **chained from the text outputs** — not written independently. The image is a visual synthesis of both voices.

---

## Example Summoning

**Concept:** *"the sound a shadow makes"*

**The Scientist:**
> Frequency: 0hz. Waveform: flat. Detectable only at perception threshold when ambient noise reaches absolute zero. Duration: indefinite.

**The Mythologist:**
> A crow that remembers every silence knew this sound. It was the noise between heartbeats before hearts existed. The deep caves still hold an echo of it.

**The Dreamer:** *(generated image: a crow dissolving into flat waveform silence, dark watercolor, cinematic)*

---

## Quick Start

```bash
git clone https://github.com/zanesmit29/the-seance
cd the-seance
pip install -r requirements.txt

# Run in mock mode — no API keys needed (in PowerShell)
$env:MOCK_MODE="true"; python app.py
```

```bash
# Run with live models
cp .env.example .env
# Add your HF_TOKEN to .env
$env:MOCK_MODE="false"; python app.py
```

```bash
# Run tests (in PowerShell)
./.venv/Scripts/python.exe -m pytest tests -q
```

---

## Datasets Referenced

| Dataset | Downloads | Purpose |
|---------|-----------|---------|
| `poloclub/diffusiondb` | 18,792 | Image+prompt pairs for FLUX prompt quality evaluation |
| `Kazimir-ai/text-to-image-prompts` | 216,551 | Baseline for prompt style benchmarking |

---

## Badges Targeted

- ✅ **Off-Brand** — Full-screen custom dark UI. Gothic blackletter title (UnifrakturMaguntia). Violent flicker on the scene. Neon green Scientist terminal. Cloudy desaturated Dreamer image. Zero default Gradio chrome.
- ✅ **Field Notes** — Blog post about what was built and learned.
- ⬜ **Sharing is Caring** — Open agent trace if time allows.

---

## Repository Structure

```
the-seance/
├── agents/
│   ├── scientist.py        # Nemotron-Nano-4B — The Scientist
│   ├── mythologist.py      # MiniCPM3-4B — The Mythologist
│   └── dreamer.py          # FLUX.1-schnell — The Dreamer
├── pipeline/
│   └── seance_pipeline.py  # Main orchestration: chain all 3 models
├── prompts/
│   ├── scientist.txt       # System prompt: cold, clinical voice
│   ├── mythologist.txt     # System prompt: ancient, folkloric voice
│   └── flux_constructor.py # Chains text outputs → FLUX prompt; tone extraction; 5 dynamic style moods
├── tests/
│   └── test_pipeline.py    # 6 pytest unit tests
├── docs/
│   └── architecture.md     # Pipeline diagram + ZeroGPU strategy
├── app.py                  # Gradio UI — custom dark atmosphere
├── Dockerfile
├── requirements.txt
├── .env.example
└── PLAN.md                 # Full sprint plan + definition of done
```

---

*Built with BriefForge — Base44 Superagent · Clarify → Recommend → Execute → Deliver*
