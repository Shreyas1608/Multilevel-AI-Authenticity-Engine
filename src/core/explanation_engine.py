import os
from openai import OpenAI


class ExplanationEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None

    def generate_explanation(self, ensemble_result):

        # Try API first
        if self.client:
            try:
                return self._generate_api_explanation(ensemble_result)
            except Exception:
                # If quota or network fails → fallback
                return self._generate_local_explanation(ensemble_result)

        # If no API key → fallback directly
        return self._generate_local_explanation(ensemble_result)

    # -------------------------
    # API EXPLANATION
    # -------------------------
    def _generate_api_explanation(self, ensemble_result):

        prompt = f"""
You are an AI Forensic Analyst.

A multi-level AI detection system analyzed an image.

FINAL VERDICT: {ensemble_result['verdict']}
Final AI Probability: {ensemble_result['final_ai_percentage']}%

Level 1:
{ensemble_result.get('level1_details')}

Level 2:
{ensemble_result.get('level2_details')}

Level 3:
{ensemble_result.get('level3_details')}

Explain clearly WHY the system produced this verdict.
Do NOT re-classify.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        return response.choices[0].message.content

    # -------------------------
    # LOCAL FALLBACK EXPLANATION
    # -------------------------
    def _generate_local_explanation(self, ensemble_result):

        verdict = ensemble_result["verdict"]
        ai_percent = ensemble_result["final_ai_percentage"]

        explanation = "\n[LOCAL FORENSIC ANALYSIS]\n\n"

        explanation += f"Final Verdict: {verdict}\n"
        explanation += f"AI Probability: {ai_percent:.2f}%\n\n"

        # Level 1
        if ensemble_result.get("level1_details"):
            l1 = ensemble_result["level1_details"]
            explanation += (
                f"• Frequency Expert detected "
                f"{l1.get('fake_probability', 0)*100:.2f}% fake signal.\n"
            )

        # Level 2
        if ensemble_result.get("level2_details"):
            l2 = ensemble_result["level2_details"]
            faces = l2.get("faces_detected", 0)

            explanation += f"• Face Expert detected {faces} face(s).\n"

            if faces > 0:
                explanation += (
                    f"  Maximum fake probability among faces: "
                    f"{l2.get('max_fake_probability', 0)*100:.2f}%.\n"
                )

        # Level 3
        if ensemble_result.get("level3_details"):
            l3 = ensemble_result["level3_details"]
            explanation += (
                f"• Semantic Expert estimated "
                f"{l3.get('fake_probability', 0)*100:.2f}% structural inconsistency.\n"
            )

        explanation += "\nConclusion: "
        if verdict == "AI Generated":
            explanation += (
                "Multiple forensic indicators strongly suggest synthetic or manipulated content."
            )
        elif verdict == "Authentic":
            explanation += (
                "All forensic indicators remain within natural image distribution."
            )
        else:
            explanation += (
                "Conflicting expert signals detected. Further review recommended."
            )

        return explanation