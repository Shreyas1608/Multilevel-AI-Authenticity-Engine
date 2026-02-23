import os
import requests
from tqdm import tqdm

MODEL_URLS = {
    "models/level1/level1_fft.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/v1.0/level1_fft.pth",
    "models/level1/level1_hybrid.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/v1.0/level1_hybrid.pth",
    "models/level2/level2_face_best.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/v1.0/level2_face_best.pth",
    "models/level2/level2_face_cropped_best.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/v1.0/level2_face_cropped_best.pth",
    "models/level3/level3_semantic_best.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/v1.0/level3_semantic_best.pth",
}

def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"\nDownloading {dest_path}...")

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {dest_path}: {e}")
        return

    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with open(dest_path, "wb") as f, tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        desc=os.path.basename(dest_path),
    ) as progress_bar:
        for chunk in response.iter_content(block_size):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))

    print(f"Saved to {dest_path}")

if __name__ == "__main__":
    for path, url in MODEL_URLS.items():
        if not os.path.exists(path):
            download_file(url, path)
        else:
            print(f"{path} already exists, skipping.")