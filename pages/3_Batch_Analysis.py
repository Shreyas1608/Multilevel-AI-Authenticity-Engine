import streamlit as st
import tempfile
import os
from PIL import Image

from src.core.ensemble_engine import EnsembleEngine


st.set_page_config(page_title="Batch Forensics", page_icon="📂", layout="wide")

st.title("📂 Multi-Image Authenticity Analysis")
st.markdown("Analyze multiple images simultaneously using the multilevel AI system.")

uploaded_files = st.file_uploader(
    "Upload multiple images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:

    if st.button("Run Batch Analysis"):

        engine = EnsembleEngine()

        results = []
        ai_count = 0
        real_count = 0
        uncertain_count = 0
        total_ai_percentage = 0

        with st.spinner("Running forensic analysis..."):

            for file in uploaded_files:

                image_bytes = file.read()
                image = Image.open(file)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(image_bytes)
                    temp_path = tmp.name

                result = engine.analyze(temp_path)

                os.remove(temp_path)

                results.append((file.name, image, result))

                total_ai_percentage += result["final_ai_percentage"]

                verdict = result["verdict"]

                if verdict == "AI Generated":
                    ai_count += 1
                elif verdict == "Authentic":
                    real_count += 1
                else:
                    uncertain_count += 1

        # ==============================
        # 📊 Batch Summary
        # ==============================

        st.markdown("---")
        st.subheader("📊 Batch Summary")

        avg_ai = total_ai_percentage / len(results)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Images", len(results))
        col2.metric("AI Generated", ai_count)
        col3.metric("Authentic", real_count)
        col4.metric("Uncertain", uncertain_count)

        st.metric("Average AI Probability", f"{avg_ai:.2f}%")
        st.progress(avg_ai / 100)

        # ==============================
        # 🔎 Individual Results
        # ==============================

        st.markdown("---")
        st.subheader("🔎 Individual Results")

        for name, image, result in results:

            with st.container():

                col_img, col_info = st.columns([1, 3])

                with col_img:
                    st.image(image, width=150)

                with col_info:
                    ai_pct = result["final_ai_percentage"]
                    verdict = result["verdict"]

                    confidence = 0
                    if result.get("level3_details"):
                        confidence = result["level3_details"].get("confidence", 0) * 100

                    st.markdown(f"### {name}")
                    st.write(f"AI Probability: **{ai_pct:.2f}%**")
                    st.write(f"Verdict: **{verdict}**")
                    st.write(f"Confidence Score: **{confidence:.2f}%**")

                    st.progress(ai_pct / 100)

                st.markdown("---")