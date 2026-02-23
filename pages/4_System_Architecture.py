import streamlit as st

st.set_page_config(page_title="System Architecture", page_icon="🧠", layout="wide")

st.title("🧠 Multilevel AI Authenticity Engine")
st.markdown("Advanced hierarchical forensic detection architecture.")

st.markdown("---")

# ==========================
# SYSTEM OVERVIEW
# ==========================

st.header("📌 System Overview")

st.markdown("""
Our system uses a **multi-level expert architecture** to detect AI-generated
images and videos.  

Instead of relying on a single model, we combine multiple forensic experts
that analyze content from different perspectives:

• Frequency patterns  
• Facial integrity  
• Semantic consistency  
• Temporal coherence (video)  
• AI-assisted explanation layer  

This layered approach increases robustness and reduces false positives.
""")

st.markdown("---")

# ==========================
# LEVEL 1
# ==========================

st.header("🔬 Level 1 — Frequency Expert")

st.markdown("""
Detects high-frequency artifacts and pixel-level inconsistencies
common in GAN and diffusion-based image generation.

Analyzes:
• FFT patterns  
• Upscaling artifacts  
• Noise irregularities  
• Compression inconsistencies  

Purpose: Detect synthetic texture signals invisible to human eyes.
""")

st.markdown("---")

# ==========================
# LEVEL 2
# ==========================

st.header("👤 Level 2 — Face Integrity Expert")

st.markdown("""
Specialized deepfake detection module focused on human faces.

Analyzes:
• Facial blending artifacts  
• Identity inconsistencies  
• Skin texture mismatches  
• Multi-face manipulation detection  

If multiple faces are present, it evaluates each face separately
and aggregates the risk.
""")

st.markdown("---")

# ==========================
# LEVEL 3
# ==========================

st.header("🧠 Level 3 — Semantic Consistency Expert")

st.markdown("""
Vision Transformer-based structural analysis engine.

Analyzes:
• Lighting direction consistency  
• Shadow realism  
• Object coherence  
• Anatomical plausibility  
• Contextual realism  

This prevents the model from relying only on pixel noise
and forces structural reasoning.
""")

st.markdown("---")

# ==========================
# LEVEL 4
# ==========================

st.header("🎬 Level 4 — Video Frame Aggregation Expert")

st.markdown("""
Frame-based temporal evaluation for videos.

Process:
1. Extract multiple frames
2. Analyze each frame independently
3. Aggregate AI probabilities

Purpose:
Detect AI-generated video by evaluating frame-level inconsistencies.
""")

st.markdown("---")

# ==========================
# LEVEL 5
# ==========================

st.header("🧾 Level 5 — AI Explanation Layer")

st.markdown("""
Generates human-readable forensic reasoning
based on model outputs.

Instead of allowing external AI to decide the verdict,
it explains WHY the internal system reached its conclusion.

Ensures:
• Transparency  
• Interpretability  
• Trustworthiness  
""")

st.markdown("---")

# ==========================
# ENSEMBLE LOGIC
# ==========================

st.header("⚙️ Ensemble Decision Logic")

st.markdown("""
The final AI probability is computed using weighted fusion:

• If face manipulation confidence is very high → Face Override mode  
• Otherwise → Weighted blending of Level 1, Level 2, and Level 3  

Video decisions are computed using average AI probability across frames.

Final Verdict Threshold (Binary Mode):
• > 65% → AI Generated  
• ≤ 65% → Authentic  
""")

st.markdown("---")

# ==========================
# WHY MULTILEVEL?
# ==========================

st.header("🚀 Why Multilevel Architecture?")

st.markdown("""
Single-model detectors often fail when:

• Images are heavily compressed  
• AI models evolve  
• New generation techniques appear  

Our architecture ensures:
• Redundancy  
• Cross-validation between experts  
• Improved generalization  
• Reduced false positives  
""")

st.markdown("---")

st.success("System Architecture Loaded Successfully.")