import torch
import torch.nn as nn
from torchvision import models
from torchvision.transforms import v2
from PIL import Image

class Level3SemanticExpert:
    def __init__(self, model_path="models/level3/level3_semantic_best.pth"):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = self._load_model(model_path)
        self.model.eval()

        self.transform = v2.Compose([
            v2.Resize((224, 224)),
            v2.ToImage(),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        print("✅ Level 3 Semantic Expert Loaded Successfully")

    def _load_model(self, model_path):
        model = models.vit_b_16(
            weights=models.ViT_B_16_Weights.IMAGENET1K_V1
        )

        # Freeze all
        for param in model.parameters():
            param.requires_grad = False

        # Unfreeze last 4 blocks
        for block in model.encoder.layers[-4:]:
            for param in block.parameters():
                param.requires_grad = True

        # Replace head
        model.heads.head = nn.Linear(model.heads.head.in_features, 2)

        model.load_state_dict(torch.load(model_path, map_location=self.device))

        return model.to(self.device)

    def predict(self, image_path):

        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(image_tensor)
            probs = torch.softmax(outputs, dim=1)

        fake_prob = probs[0][0].item()
        real_prob = probs[0][1].item()

        return {
            "real_probability": real_prob,
            "fake_probability": fake_prob,
            "confidence": abs(fake_prob - real_prob)
        }