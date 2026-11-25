# Wildfire Smoke Segmentation from Space (ADSP 2026/27 — Team 15)

Cross-sensor wildfire smoke segmentation: training on **GOES ABI (SmokeViz, USA)** and evaluating transferability to **Meteosat-12 MTG-FCI (Europe)**.

## Repository Structure

```text
├── LINKS_ADSP-Wildfire_Smoke_Segmentation.pdf   # Project overview & pitch
├── checkpoints/                                 # Course checkpoint deliverables
│   ├── checkpoint_1/
│   ├── checkpoint_2/
│   └── checkpoint_3/
├── docs/                                        # Reference papers & technical docs
├── configs/
│   └── paths.example.yaml                       # Template for local dataset paths
├── notebooks/
│   ├── Smoke in GOES Imagery.ipynb              # SmokeViz (GOES-16) EDA
│   └── Smoke Unet.ipynb                         # Warm-up U-Net binary baseline
├── src/
│   └── config.py                                # Portable path & config loader
└── requirements.txt
```

## Quick Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `configs/paths.example.yaml` to `configs/paths.local.yaml` and update the local dataset paths (or set `SMOKEVIZ_DATA_DIR`, `SMOKEVIZ_COORDS_DIR`, `SMOKEVIZ_METADATA_PATH`).
