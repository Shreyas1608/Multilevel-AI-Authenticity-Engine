import os
import requests

MODEL_URLS = {
    "models/level1/level1_fft.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/untagged-9bc4c27c830e54b706fd/level1_fft.pth",
    "models/level1/level1_hybrid.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/untagged-9bc4c27c830e54b706fd/level1_hybrid.pth",
    "models/level2/level2_face_best.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/untagged-9bc4c27c830e54b706fd/level2_face_best.pth",
    "models/level2/level2_face_cropped_best.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/untagged-9bc4c27c830e54b706fd/level2_face_cropped_best.pth",
    "models/level3/level3_semantic_best.pth": "https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine/releases/download/untagged-9bc4c27c830e54b706fd/level3_semantic_best.pth",
}

def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"Downloading {dest_path}...")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"Saved to {dest_path}")

if __name__ == "__main__":
    for path, url in MODEL_URLS.items():
        if not os.path.exists(path):
            download_file(url, path)
        else:
            print(f"{path} already exists, skipping.")