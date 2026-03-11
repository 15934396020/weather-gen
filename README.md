# Weather Scene Generator

Design and Implementation of a Controllable Scenario Weather Image Generation and Display System Based on ControlNet.

## Project Structure

```
weather-gen/
├── backend/                  # Backend service (FastAPI + model inference)
│   ├── config.py             # Device config (mps/cuda/cpu), model IDs, defaults
│   ├── inference.py          # Model loading, Canny extraction, image generation
│   ├── main.py               # FastAPI app, API endpoints, static file serving
│   ├── weather_prompts.py    # Weather prompt library (5 types)
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Frontend web interface
│   └── index.html            # Single-page application
├── scripts/                  # Utility scripts (report generation, figure generation)
├── tests/                    # Test images and test scripts
├── docs/                     # Documentation and report figures
│   └── figures/              # Generated figures for the report
├── start.sh                  # Quick start script
├── .gitignore
└── README.md
```

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Start the server
bash start.sh

# 4. Open browser
# http://localhost:8000
```

## Configuration

Edit `backend/config.py` to switch device:
- `DEVICE = "mps"` — Apple Silicon (Mac)
- `DEVICE = "cuda"` — NVIDIA GPU
- `DEVICE = "cpu"` — CPU fallback

## Tech Stack

- **Model**: Stable Diffusion v1.5 + ControlNet (Canny)
- **Backend**: Python, FastAPI, PyTorch, Diffusers, OpenCV
- **Frontend**: HTML/CSS/JavaScript (single-page app)
