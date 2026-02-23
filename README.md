# Multilevel AI Authenticity Engine

A hierarchical AI forensic system designed to detect AI-generated images and videos using multiple independent expert models and an ensemble-based authenticity scoring mechanism.

---

## Overview

The Multilevel AI Authenticity Engine is built to analyze digital media and determine whether it is:

- Authentic (real)
- AI-generated (synthetic)

The system uses a layered expert architecture, where each level specializes in a different forensic domain:

- Level 1 – Frequency-based artifact detection
- Level 2 – Facial region analysis
- Level 3 – High-level semantic inconsistencies
- Level 4 – Video-based temporal inconsistencies

All expert outputs are aggregated through an ensemble engine to produce a final Authenticity Score.

---

## Repository Structure

```
Multilevel-AI-Authenticity-Engine/
│
├── app.py
├── download_models.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_Image_Forensics.py
│   ├── 2_Video_Forensics.py
│   ├── 3_Batch_Analysis.py
│   └── 4_System_Architecture.py
│
└── src/
    ├── core/
    │   ├── ensemble_engine.py
    │   └── explanation_engine.py
    │
    └── experts/
        ├── level1_expert.py
        ├── level2_expert.py
        ├── level3_expert.py
        └── level4_video_expert.py
```

Note: Model weights are not stored in this repository. They must be downloaded separately using the provided script.

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Shreyas1608/Multilevel-AI-Authenticity-Engine.git
cd Multilevel-AI-Authenticity-Engine
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Download Model Weights

Model files are hosted separately to keep the repository lightweight.

Run:

```bash
python download_models.py
```

This will automatically download all required model weights into the correct directory structure.

---

### 4. Run the Application

```bash
streamlit run app.py
```

The system interface will open in your browser.

---

## How It Works

### Level 1 – Frequency Expert
Detects periodic noise and upscaling artifacts using frequency-domain analysis.

### Level 2 – Face Expert
Analyzes facial regions to identify GAN and diffusion inconsistencies.

### Level 3 – Semantic Expert
Detects high-level structural and contextual anomalies in images.

### Level 4 – Video Expert
Analyzes temporal consistency and frame-level irregularities in video inputs.

### Ensemble Engine
Combines outputs from all experts to compute a final Authenticity Score.

### Explanation Engine
Provides interpretable reasoning behind the model's decision.

---

## Important Notes

- Ensure all models are downloaded before running the application.
- If a model file is missing, the system will prompt you to run:
  
  ```
  python download_models.py
  ```

- Large models may take several minutes to download depending on internet speed.

---

## Intended Users

Digital forensic analysts, law enforcement agencies, media verification and fact-checking organizations, cybersecurity teams, government intelligence units, academic researchers, and digital content authentication platforms.

---

## License

This project is provided for academic and research purposes.