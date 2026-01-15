import gradio as gr

def create_theme():
    """
    Creates a custom Tesserae theme with a 'Design Studio' aesthetic.
    Focus: Clean lines, high legibility, tile-like grouping, and subtle depth.
    """
    
    # Base theme configuration using Slate (neutral) and Indigo (tech/trust)
    theme = gr.themes.Soft(
        primary_hue=gr.themes.colors.indigo,
        secondary_hue=gr.themes.colors.slate,
        neutral_hue=gr.themes.colors.slate,
        text_size=gr.themes.sizes.text_lg,
        spacing_size=gr.themes.sizes.spacing_md,
        radius_size=gr.themes.sizes.radius_lg,
        font=[
            gr.themes.GoogleFont("Inter"), 
            "ui-sans-serif", 
            "system-ui", 
            "sans-serif"
        ],
        font_mono=[
            gr.themes.GoogleFont("JetBrains Mono"), 
            "ui-monospace", 
            "monospace"
        ],
    )

    # sophisticated overrides for a "pro tool" look
    theme = theme.set(
        # Body & Backgrounds
        body_background_fill="*neutral_50",
        body_text_color="*neutral_900",
        background_fill_primary="white",
        
        # Blocks (The "Tiles")
        block_background_fill="white",
        block_border_width="1px",
        block_border_color="*neutral_200",
        block_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
        block_title_text_weight="600",
        block_label_text_size="*text_sm",
        block_label_text_weight="500",
        
        # Inputs
        input_background_fill="*neutral_50",
        input_border_color="*neutral_200",
        input_shadow="none",
        input_shadow_focus="0 0 0 2px *primary_200",
        
        # Buttons
        button_primary_background_fill="*primary_600",
        button_primary_background_fill_hover="*primary_700",
        button_primary_text_color="white",
        button_primary_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        
        # Borders & Radius
        block_radius="12px",
        container_radius="12px",
    )
    
    return theme

# Custom CSS for non-standard elements (Swatches, Headers)
custom_css = """
/* Font adjustments */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Main Title styling */
h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    color: #1e293b;
}

/* Make the Color Swatches container look like a grid */
.swatch-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 16px;
    padding: 16px;
}

/* Markdown headers inside analysis */
.prose h2 {
    font-weight: 700;
    color: #334155;
    margin-top: 1.5em;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.5em;
}

/* Code blocks (JSON/CSS export) */
.code-wrap {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

/* Status alerts */
.success-status {
    border-left: 4px solid #10b981;
    background-color: #ecfdf5;
    padding: 10px;
}
"""