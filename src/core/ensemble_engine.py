import torch

from src.experts.level1_expert import Level1Expert
from src.experts.level2_expert import Level2FaceExpert
from src.experts.level3_expert import Level3SemanticExpert


class EnsembleEngine:

    def __init__(self):

        print("🔧 Initializing Ensemble Engine...")

        self.level1 = Level1Expert()
        self.level2 = Level2FaceExpert()
        self.level3 = Level3SemanticExpert()

        print("✅ Ensemble Engine Ready\n")

    # =========================================================
    # OPTION C LOGIC IMPLEMENTATION
    # =========================================================

    def analyze(self, image_path):

        # -----------------------
        # Level 1
        # -----------------------
        l1_result = self.level1.predict(image_path)
        l1_fake = l1_result["fake_probability"]

        # -----------------------
        # Level 2
        # -----------------------
        l2_result = self.level2.predict(image_path)

        face_detected = l2_result.get("faces_detected", 0) > 0

        if face_detected:
            l2_fake = l2_result["max_fake_probability"]
        else:
            l2_fake = None

        # -----------------------
        # Level 3
        # -----------------------
        l3_result = self.level3.predict(image_path)
        l3_fake = l3_result["fake_probability"]

        # =========================================================
        # AGGREGATION (OPTION C)
        # =========================================================

        if face_detected:

            # Strong facial manipulation override
            if l2_fake > 0.80:
                final_fake = l2_fake
                decision_mode = "Face Override"

            else:
                final_fake = (
                    0.2 * l1_fake +
                    0.5 * l2_fake +
                    0.3 * l3_fake
                )
                decision_mode = "Weighted Fusion (Face Present)"

        else:
            # No face → L1 + L3 only
            final_fake = (
                0.5 * l1_fake +
                0.5 * l3_fake
            )
            decision_mode = "Weighted Fusion (No Face)"

        # =========================================================
        # FINAL VERDICT
        # =========================================================

        if final_fake > 0.70:
            verdict = "AI Generated"
        elif final_fake < 0.35:
            verdict = "Authentic"
        else:
            verdict = "Uncertain"

        return {
            "final_fake_probability": final_fake,
            "final_ai_percentage": final_fake * 100,
            "verdict": verdict,
            "decision_mode": decision_mode,
            "experts_used": {
                "level1": True,
                "level2": face_detected,
                "level3": True
            },
            "level1_details": l1_result,
            "level2_details": l2_result,
            "level3_details": l3_result
        }