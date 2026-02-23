import torch
import torch.nn as nn
import numpy as np
from torchvision import models, transforms
from PIL import Image
import cv2
import os


class Level2FaceExpert:

    def __init__(self, model_path="models/level2/level2_face_best.pth"):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # ----------------------------
        # Model Setup (MobileNetV2)
        # ----------------------------
        self.model = models.mobilenet_v2(weights=None)

        self.model.classifier[1] = nn.Sequential(
            nn.Linear(self.model.last_channel, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 2)
        )

        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        # Explicit class mapping (VERY IMPORTANT)
        # ImageFolder alphabetical order: fake=0, real=1
        self.class_names = ["fake", "real"]

        # ----------------------------
        # Transform (must match training)
        # ----------------------------
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225]
            )
        ])

        # Haar cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        print("✅ Level 2 Face Expert Loaded Successfully (multi-face enabled)")

    # --------------------------------------------------
    # Face Detection with 30% Margin
    # --------------------------------------------------
    def _detect_faces(self, image_np):

        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40)
        )

        cropped_faces = []

        for (x, y, w, h) in faces:

            margin = int(0.3 * w)

            x1 = max(0, x - margin)
            y1 = max(0, y - margin)
            x2 = min(image_np.shape[1], x + w + margin)
            y2 = min(image_np.shape[0], y + h + margin)

            face_crop = image_np[y1:y2, x1:x2]
            cropped_faces.append(face_crop)

        return cropped_faces

    # --------------------------------------------------
    # Prediction Logic
    # --------------------------------------------------
    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")
        image_np = np.array(image)

        faces = self._detect_faces(image_np)

        if len(faces) == 0:
            return {
                "faces_detected": 0,
                "ai_content_percentage": None,
                "forensic_decision": "No Face Detected",
                "note": "Level 2 skipped."
            }

        per_face_scores = []
        fake_probs = []

        for face_img in faces:

            face_pil = Image.fromarray(
                face_img.astype("uint8")
            ).convert("RGB")

            face_tensor = self.transform(face_pil).unsqueeze(0).to(self.device)

            with torch.no_grad():
                output = self.model(face_tensor)
                probs = torch.softmax(output, dim=1)

            # Explicit index mapping
            fake_prob = probs[0][0].item()  # index 0 = fake
            real_prob = probs[0][1].item()  # index 1 = real

            per_face_scores.append({
                "real_probability": real_prob,
                "fake_probability": fake_prob
            })

            fake_probs.append(fake_prob)

        max_fake = max(fake_probs)
        avg_fake = sum(fake_probs) / len(fake_probs)

        # ----------------------------
        # Conservative Forensic Threshold
        # ----------------------------
        if max_fake > 0.70:
            verdict = "AI Generated"
        elif max_fake < 0.20:
            verdict = "Authentic"
        else:
            verdict = "Uncertain"

        return {
            "faces_detected": len(faces),
            "per_face_scores": per_face_scores,
            "max_fake_probability": max_fake,
            "average_fake_probability": avg_fake,
            "ai_content_percentage": avg_fake * 100,
            "forensic_decision_score": max_fake,
            "forensic_decision": verdict
        }
