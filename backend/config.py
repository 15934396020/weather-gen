import os

# Device: "mps" for Mac, "cuda" for NVIDIA GPU, "cpu" as fallback
DEVICE = os.getenv("DEVICE", "mps")

# Model IDs (Hugging Face)
SD_MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"
CONTROLNET_CANNY_ID = "lllyasviel/sd-controlnet-canny"
CONTROLNET_SCRIBBLE_ID = "lllyasviel/sd-controlnet-scribble"
CONTROLNET_DEPTH_ID = "lllyasviel/sd-controlnet-depth"

# Default generation params
DEFAULT_STEPS = 20
DEFAULT_CFG_SCALE = 7.5
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512

# Server
HOST = "0.0.0.0"
PORT = 8000
