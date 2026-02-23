import streamlit as st
from PIL import Image
import tempfile
import os

from src.core.ensemble_engine import EnsembleEngine
from src.core.explanation_engine import ExplanationEngine


st.set_page_config(page_title="Image Forensics", page_icon="🛡️", layout="wide")

st.title("🛡️ Image Authenticity Analysis")
st.markdown("Advanced multi-level AI authenticity evaluation engine.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:

    image = Image.open(uploaded_file)

    col_img, col_result = st.columns([1, 2])

    with col_img:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        temp_path = tmp.name

    if st.button("Run Analysis"):

        with st.spinner("Running multi-level forensic evaluation..."):

            engine = EnsembleEngine()
            explainer = ExplanationEngine()

            result = engine.analyze(temp_path)

        final_ai_pct = result["final_ai_percentage"]
        verdict = result["verdict"]

        with col_result:

            st.subheader("🔎 Final Verdict")

            # =========================
            # AI Probability Metric
            # =========================
            st.metric("AI Probability", f"{final_ai_pct:.2f}%")

            # =========================
            # AI Probability Progress Bar
            # =========================
            st.progress(final_ai_pct / 100)

            # =========================
            # Confidence Badge
            # =========================
            confidence = result["level3_details"]["confidence"] * 100

            if confidence > 80:
                badge_color = "#16A34A"
                label = "HIGH CONFIDENCE"
            elif confidence > 50:
                badge_color = "#F59E0B"
                label = "MODERATE CONFIDENCE"
            else:
                badge_color = "#DC2626"
                label = "LOW CONFIDENCE"

            st.markdown(
                f"""
                <div style="margin-top:10px;">
                    <span style="
                        background:{badge_color};
                        padding:6px 14px;
                        border-radius:20px;
                        font-weight:600;
                        color:white;">
                        {label} • {confidence:.2f}%
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("")

            # =========================
            # Verdict Display
            # =========================
            verdict_color = "#EF4444" if verdict == "AI Generated" else "#22C55E"

            st.markdown(
                f"""
                <div style="
                    margin-top:15px;
                    font-size:28px;
                    font-weight:800;
                    color:{verdict_color};">
                    FINAL VERDICT: {verdict.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(f"Decision Mode: {result.get('decision_mode')}")

        st.markdown("---")

        # =========================
        # EXPLANATION ENGINE
        # =========================
        st.subheader("🧾 System Explanation")

        explanation = explainer.generate_explanation(result)
        st.write(explanation)

        st.markdown("---")

        # =========================
        # MULTI LEVEL BREAKDOWN
        # =========================
        st.subheader("📊 Multi-Level Expert Breakdown")

        # LEVEL 1
        if result.get("level1_details"):
            l1 = result["level1_details"]

            st.markdown("### 🔬 Level 1 — Frequency Expert")
            st.caption("Detects unnatural frequency artifacts and upscaling inconsistencies.")

            l1_fake = l1["fake_probability"] * 100
            l1_conf = l1["confidence"] * 100

            st.progress(l1_fake / 100)
            st.write(f"Fake Probability: {l1_fake:.2f}%")
            st.write(f"Confidence Score: {l1_conf:.2f}%")

            st.markdown("")

        # LEVEL 2
        if result.get("level2_details"):
            l2 = result["level2_details"]

            st.markdown("### 👤 Level 2 — Face Integrity Expert")
            st.caption("Analyzes faces for deepfake artifacts and blending inconsistencies.")

            st.write(f"Faces Detected: {l2['faces_detected']}")

            if l2["faces_detected"] > 0:
                max_fake = l2["max_fake_probability"] * 100
                avg_fake = l2["average_fake_probability"] * 100

                st.progress(max_fake / 100)
                st.write(f"Maximum Face Fake Probability: {max_fake:.2f}%")
                st.write(f"Average Face Fake Probability: {avg_fake:.2f}%")

            st.markdown("")

        # LEVEL 3
        if result.get("level3_details"):
            l3 = result["level3_details"]

            st.markdown("### 🧠 Level 3 — Semantic Consistency Expert")
            st.caption("Evaluates structural realism and contextual coherence.")

            l3_fake = l3["fake_probability"] * 100
            l3_conf = l3["confidence"] * 100

            st.progress(l3_fake / 100)
            st.write(f"Fake Probability: {l3_fake:.2f}%")
            st.write(f"Confidence Score: {l3_conf:.2f}%")

    os.remove(temp_path)