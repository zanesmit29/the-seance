"""
The Séance — A Gradio app for HuggingFace BuildSmall Hackathon: Thousand Token Wood
Three AI entities channel the form of things that don't exist.
"""
import os
import gradio as gr
from pipeline.seance_pipeline import SeancePipeline

os.environ.setdefault("MOCK_MODE", "true")
pipeline = SeancePipeline()

# ---- Custom CSS: dark, atmospheric, three distinct entity styles ----
CUSTOM_CSS = """
* { box-sizing: border-box; }

body, .gradio-container {
    background-color: #0d0d0f !important;
    color: #c8c8d0 !important;
    font-family: 'Georgia', serif;
}

.gradio-container { max-width: 860px !important; margin: 0 auto !important; }

/* Hide all default Gradio chrome */
footer, .share-button, .duplicate-button, .built-with { display: none !important; }
.svelte-1ipelgc { display: none !important; }

/* Title */
#seance-title {
    text-align: center;
    padding: 40px 0 10px;
    font-size: 2.2em;
    letter-spacing: 0.12em;
    color: #e8e0d0;
    font-family: 'Georgia', serif;
}
#seance-subtitle {
    text-align: center;
    color: #666070;
    font-size: 0.95em;
    letter-spacing: 0.06em;
    margin-bottom: 36px;
    font-style: italic;
}

/* Input area */
#concept-input textarea {
    background: #141418 !important;
    border: 1px solid #2a2a35 !important;
    color: #e0ddd8 !important;
    font-family: 'Georgia', serif !important;
    font-size: 1.1em !important;
    text-align: center;
    border-radius: 4px;
}
#summon-btn {
    background: #1a1a22 !important;
    border: 1px solid #3a3a50 !important;
    color: #a090c0 !important;
    letter-spacing: 0.15em !important;
    font-family: 'Georgia', serif !important;
    font-size: 0.9em !important;
}
#summon-btn:hover { background: #22222e !important; border-color: #6050a0 !important; }

/* Scientist panel — monospace, terminal green tint */
#scientist-panel {
    background: #0c110e !important;
    border: 1px solid #1a2e1e !important;
    border-radius: 4px;
    padding: 20px;
    font-family: 'Courier New', monospace !important;
    color: #7abf8a !important;
    font-size: 0.88em;
    line-height: 1.7;
    min-height: 100px;
}
#scientist-label {
    color: #3a6640;
    font-family: 'Courier New', monospace;
    font-size: 0.75em;
    letter-spacing: 0.2em;
    margin-bottom: 8px;
    text-transform: uppercase;
}

/* Mythologist panel — serif, amber/parchment tint */
#mythologist-panel {
    background: #120f08 !important;
    border: 1px solid #2e2010 !important;
    border-radius: 4px;
    padding: 20px;
    font-family: 'Georgia', serif !important;
    color: #c8a96a !important;
    font-size: 0.95em;
    line-height: 1.8;
    font-style: italic;
    min-height: 100px;
}
#mythologist-label {
    color: #6a5020;
    font-family: 'Georgia', serif;
    font-size: 0.75em;
    letter-spacing: 0.2em;
    margin-bottom: 8px;
    text-transform: uppercase;
    font-style: normal;
}

/* Image panel */
#dreamer-image img {
    border-radius: 4px;
    border: 1px solid #1e1a28;
    width: 100%;
}
#dreamer-label {
    color: #4a3a6a;
    font-size: 0.75em;
    letter-spacing: 0.2em;
    margin-bottom: 8px;
    text-transform: uppercase;
}

/* Status message */
#status-msg { color: #504858; font-size: 0.8em; text-align: center; font-style: italic; }
"""

# ---- Build UI ----
with gr.Blocks(css=CUSTOM_CSS, title="The Séance") as demo:

    gr.HTML('<div id="seance-title">✦ The Séance ✦</div>')
    gr.HTML('<div id="seance-subtitle">Name something that doesn't exist. Three entities will channel its form.</div>')

    with gr.Row():
        concept_input = gr.Textbox(
            placeholder="the last color light ever made...",
            show_label=False,
            elem_id="concept-input",
            scale=4,
        )
        summon_btn = gr.Button("— SUMMON —", elem_id="summon-btn", scale=1)

    status_msg = gr.HTML('<div id="status-msg"></div>')

    # Scientist panel
    gr.HTML('<div id="scientist-label">✦ The Scientist</div>')
    scientist_out = gr.HTML('<div id="scientist-panel"></div>')

    # Mythologist panel
    gr.HTML('<div id="mythologist-label">✦ The Mythologist</div>')
    mythologist_out = gr.HTML('<div id="mythologist-panel"></div>')

    # Dreamer image
    gr.HTML('<div id="dreamer-label">✦ The Dreamer</div>')
    dreamer_out = gr.Image(show_label=False, elem_id="dreamer-image")

    # Download button
    download_btn = gr.DownloadButton("↓ Download Artifact Card", visible=False)

    def summon(concept):
        if not concept.strip():
            yield (
                '<div id="status-msg">Speak a concept to begin the summoning.</div>',
                '<div id="scientist-panel"></div>',
                '<div id="mythologist-panel"></div>',
                None,
                gr.update(visible=False),
            )
            return

        yield (
            '<div id="status-msg">The Scientist observes...</div>',
            '<div id="scientist-panel">...</div>',
            '<div id="mythologist-panel"></div>',
            None,
            gr.update(visible=False),
        )

        artifact = pipeline.summon(concept)

        yield (
            '<div id="status-msg">The Mythologist remembers...</div>',
            f'<div id="scientist-panel">{artifact["scientist_text"]}</div>',
            '<div id="mythologist-panel">...</div>',
            None,
            gr.update(visible=False),
        )

        yield (
            '<div id="status-msg">The Dreamer is forming the image...</div>',
            f'<div id="scientist-panel">{artifact["scientist_text"]}</div>',
            f'<div id="mythologist-panel">{artifact["mythologist_text"]}</div>',
            None,
            gr.update(visible=False),
        )

        yield (
            '<div id="status-msg">The summoning is complete.</div>',
            f'<div id="scientist-panel">{artifact["scientist_text"]}</div>',
            f'<div id="mythologist-panel">{artifact["mythologist_text"]}</div>',
            artifact.get("image_path"),
            gr.update(visible=True, value=artifact.get("image_path")),
        )

    summon_btn.click(
        fn=summon,
        inputs=[concept_input],
        outputs=[status_msg, scientist_out, mythologist_out, dreamer_out, download_btn],
    )
    concept_input.submit(
        fn=summon,
        inputs=[concept_input],
        outputs=[status_msg, scientist_out, mythologist_out, dreamer_out, download_btn],
    )

if __name__ == "__main__":
    demo.launch()
