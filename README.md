---
title: The Séance
emoji: ✦
colorFrom: indigo
colorTo: black
sdk: gradio
sdk_version: 5.50.0
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
| **The Dreamer** | Generates the visual form of the concept | `black-forest-labs/FLUX.1-schnell` | HF Inference API | Clean image frame with concurrent loading panel |

**Total: ~20B params. All HuggingFace-native. All within hackathon constraints.**

The FLUX image prompt is **chained from the text outputs** — not written independently. The image is a visual synthesis of both voices.

The UI now renders all three entity loading states at once, then resolves all outputs together when generation completes.

## Validated Requirements

These are the package versions currently validated in the Windows `.venv` for this repo:

```text
transformers==4.48.3
torch==2.7.1
torchvision==0.22.1
huggingface_hub==0.36.2
gradio==5.50.0
attrs==25.4.0
accelerate>=0.30.0
bitsandbytes>=0.46.0
spaces>=0.30.0
Pillow>=10.0.0
sentencepiece>=0.2.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

The Scientist model still has an optional Nemotron/Mamba backend. That backend requires `mamba-ssm` and `causal-conv1d`, which are currently Linux/WSL-only builds. On Windows, the app falls back to the alternate Scientist model automatically.

---

## Ambient Audio

- Background ambiance is served from `audio/ambiance.MP3`.
- The app attempts autoplay once on load.
- If autoplay is blocked by browser policy, users can click **Enable Sound**.
- **Mute/Unmute** is always available once audio starts.

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

If your browser blocks autoplay, click **Enable Sound** in the bottom-right controls.

```bash
# Run with live models
cp .env.example .env
# Add your HF_TOKEN to .env
$env:MOCK_MODE="false"; python app.py
```

If you want the full Nemotron Scientist backend instead of the fallback, use Linux or WSL and install the optional packages below:

```bash
pip install mamba-ssm causal-conv1d --no-build-isolation
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

- ✅ **Off-Brand** — Full-screen custom dark UI. Gothic blackletter title (UnifrakturMaguntia). Violent flicker on the scene. Neon green Scientist terminal. Concurrent entity loading states. Ambient audio controls. Zero default Gradio chrome.
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
├── audio/
│   └── ambiance.MP3        # Background ambient loop for the UI
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
