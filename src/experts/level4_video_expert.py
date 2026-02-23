import cv2
import os
import tempfile
from src.core.ensemble_engine import EnsembleEngine


class Level4VideoExpert:

    def __init__(self):
        print("🎥 Initializing Level 4 Video Expert...")
        self.engine = EnsembleEngine()
        print("✅ Level 4 Video Expert Ready\n")

    def extract_frames(self, video_path, max_frames=15):
        cap = cv2.VideoCapture(video_path)

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if total_frames == 0:
            raise ValueError("Video contains no frames.")

        frame_indices = []

        if total_frames <= max_frames:
            frame_indices = list(range(total_frames))
        else:
            step = total_frames // max_frames
            frame_indices = [i * step for i in range(max_frames)]

        frames = []

        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()

            if ret:
                frames.append(frame)

        cap.release()
        return frames

    def analyze(self, video_path):

        print(f"📂 Processing Video: {video_path}\n")

        frames = self.extract_frames(video_path)

        frame_scores = []

        with tempfile.TemporaryDirectory() as temp_dir:

            for i, frame in enumerate(frames):
                frame_path = os.path.join(temp_dir, f"frame_{i}.jpg")
                cv2.imwrite(frame_path, frame)

                result = self.engine.analyze(frame_path)
                frame_scores.append(result["final_fake_probability"])

        if len(frame_scores) == 0:
            raise ValueError("No frames processed.")

        max_fake = max(frame_scores)
        avg_fake = sum(frame_scores) / len(frame_scores)

        # Final Video Verdict
        if max_fake > 0.75:
            verdict = "AI Generated"
        elif avg_fake > 0.60:
            verdict = "Likely AI"
        elif avg_fake < 0.35:
            verdict = "Authentic"
        else:
            verdict = "Uncertain"

        return {
            "frames_analyzed": len(frame_scores),
            "max_frame_fake_probability": max_fake,
            "average_frame_fake_probability": avg_fake,
            "video_ai_percentage": avg_fake * 100,
            "verdict": verdict
        }