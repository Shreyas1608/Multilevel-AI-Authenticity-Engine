import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import os


# -------------------------------------------------
# FFT Function (same as training)
# -------------------------------------------------
def compute_fft(batch):
    fft = torch.fft.fft2(batch)
    fft_shift = torch.fft.fftshift(fft)
    magnitude = torch.abs(fft_shift)
    return torch.log1p(magnitude)


# -------------------------------------------------
# Hybrid Level 1 Model (same architecture)
# -------------------------------------------------
class HybridLevel1(nn.Module):
    def __init__(self):
        super(HybridLevel1, self).__init__()

        self.spatial = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.frequency = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4 * 2, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )

    def forward(self, x):
        spatial_feat = self.spatial(x)
        fft_x = compute_fft(x)
        freq_feat = self.frequency(fft_x)
        combined = torch.cat((spatial_feat, freq_feat), dim=1)
        output = self.classifier(combined)
        return output


# -------------------------------------------------
# Level 1 Expert Class
# -------------------------------------------------
class Level1Expert:
    def __init__(self, model_path="models/level1/level1_hybrid.pth"):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = HybridLevel1().to(self.device)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        self.model.load_state_dict(
            torch.load(model_path, map_location=self.device)
        )

        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((32, 32)),
            transforms.ToTensor()
        ])

        print("✅ Level 1 Expert Loaded Successfully")

    # -------------------------------------------------
    # Predict method
    # -------------------------------------------------
    def predict(self, image_path):

        image = Image.open(image_path).convert("L")
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = F.softmax(output, dim=1)

        real_prob = probabilities[0][0].item()
        fake_prob = probabilities[0][1].item()
        confidence = abs(fake_prob - real_prob)

        return {
            "real_probability": real_prob,
            "fake_probability": fake_prob,
            "confidence": confidence
        }
