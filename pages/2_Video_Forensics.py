import streamlit as st
import tempfile
import os
import cv2
import shutil
import uuid

from src.core.ensemble_engine import EnsembleEngine
from src.core.explanation_engine import ExplanationEngine


st.set_page_config(page_title="Video Forensics", page_icon="🎬", layout="wide")

st.title("🎬 Video Authenticity Analysis")
st.markdown("Frame-based AI authenticity evaluation using multilevel forensic architecture.")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if uploaded_video:

    # Save uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_video.read())
        temp_video_path = tmp.name

    st.video(temp_video_path)

    if st.button("Run Video Analysis"):

        with st.spinner("Extracting frames and running forensic analysis..."):

            engine = EnsembleEngine()
            explainer = ExplanationEngine()

            cap = cv2.VideoCapture(temp_video_path)

            frame_results = []
            frame_count = 0
            max_frames = 20

            # Create temporary folder for frames
            temp_frame_dir = os.path.join(
                tempfile.gettempdir(),
                f"video_frames_{uuid.uuid4().hex}"
            )
            os.makedirs(temp_frame_dir, exist_ok=True)

            while cap.isOpened() and frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_path = os.path.join(
                    temp_frame_dir,
                    f"frame_{frame_count}.jpg"
                )

                cv2.imwrite(frame_path, frame)

                frame_result = engine.analyze(frame_path)
                frame_results.append(frame_result["final_ai_percentage"])

                frame_count += 1

            cap.release()

            # Clean up frame folder
            shutil.rmtree(temp_frame_dir)

        if not frame_results:
            st.error("No frames could be analyzed.")
        else:

            final_ai_pct = sum(frame_results) / len(frame_results)

            verdict = "AI Generated" if final_ai_pct > 65 else "Authentic"

            st.markdown("---")
            st.subheader("🔎 Final Video Verdict")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Average AI Probability", f"{final_ai_pct:.2f}%")
                st.progress(final_ai_pct / 100)

            with col2:
                st.metric("Verdict", verdict)

            st.caption(f"Frames analyzed: {len(frame_results)}")

            st.markdown("---")
            st.subheader("🧾 System Explanation")

            explanation = f"""
The video was analyzed using {len(frame_results)} extracted frames.

Average AI probability across frames: {final_ai_pct:.2f}%.

Based on multi-frame forensic evaluation, the video is classified as **{verdict.upper()}**.
"""
            st.write(explanation)

    # Cleanup uploaded video
    os.remove(temp_video_path)