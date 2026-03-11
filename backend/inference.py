import io
import os
import numpy as np
from PIL import Image
import cv2
import requests
import base64
import json

from config import DEFAULT_STEPS, DEFAULT_CFG_SCALE

HF_TOKEN = os.getenv("HF_TOKEN", "")

# Use HF Inference API for remote generation
HF_API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"

# For local mode (when on GPU machine), set USE_LOCAL=true
USE_LOCAL = os.getenv("USE_LOCAL", "false").lower() == "true"

_pipeline = None


def get_pipeline():
    """Lazy-load local pipeline (only used when USE_LOCAL=true)."""
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    import torch
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
    from config import DEVICE, SD_MODEL_ID, CONTROLNET_CANNY_ID

    print(f"Loading ControlNet model on device: {DEVICE}")
    dtype = torch.float16 if DEVICE == "cuda" else torch.float32

    controlnet = ControlNetModel.from_pretrained(CONTROLNET_CANNY_ID, torch_dtype=dtype)
    _pipeline = StableDiffusionControlNetPipeline.from_pretrained(
        SD_MODEL_ID, controlnet=controlnet, torch_dtype=dtype, safety_checker=None,
    )
    _pipeline.scheduler = UniPCMultistepScheduler.from_config(_pipeline.scheduler.config)

    if DEVICE == "cuda":
        _pipeline.enable_model_cpu_offload()
    elif DEVICE == "mps":
        _pipeline.to("mps")
        _pipeline.enable_attention_slicing()
    else:
        _pipeline.to("cpu")

    print("Model loaded successfully.")
    return _pipeline


def extract_canny(image: Image.Image, low: int = 100, high: int = 200) -> Image.Image:
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    edges = cv2.Canny(gray, low, high)
    return Image.fromarray(edges).convert("RGB")


def image_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def generate_image_remote(
    prompt: str,
    negative_prompt: str,
    control_image: Image.Image,
    num_steps: int = DEFAULT_STEPS,
    cfg_scale: float = DEFAULT_CFG_SCALE,
    seed: int = -1,
    auto_canny: bool = True,
) -> Image.Image:
    """Generate via HF Inference API (text-to-image, no ControlNet conditioning)."""
    # For the remote API, we use text-to-image with the weather prompt
    # ControlNet is not directly supported via free API, so we embed scene structure in prompt
    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "num_inference_steps": min(num_steps, 30),
            "guidance_scale": cfg_scale,
        }
    }
    if seed >= 0:
        payload["parameters"]["seed"] = seed

    resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"HF API error {resp.status_code}: {resp.text[:200]}")

    return Image.open(io.BytesIO(resp.content))


def generate_image_local(
    prompt: str,
    negative_prompt: str,
    control_image: Image.Image,
    num_steps: int = DEFAULT_STEPS,
    cfg_scale: float = DEFAULT_CFG_SCALE,
    seed: int = -1,
    auto_canny: bool = True,
) -> Image.Image:
    """Generate locally with ControlNet pipeline."""
    import torch
    pipe = get_pipeline()
    control_image = control_image.resize((512, 512))
    if auto_canny:
        control_image = extract_canny(control_image)

    generator = None
    if seed >= 0:
        generator = torch.Generator(device="cpu").manual_seed(seed)

    result = pipe(
        prompt=prompt, negative_prompt=negative_prompt,
        image=control_image, num_inference_steps=num_steps,
        guidance_scale=cfg_scale, generator=generator,
    )
    return result.images[0]


def generate_image(
    prompt: str,
    negative_prompt: str,
    control_image: Image.Image,
    num_steps: int = DEFAULT_STEPS,
    cfg_scale: float = DEFAULT_CFG_SCALE,
    seed: int = -1,
    auto_canny: bool = True,
) -> Image.Image:
    if USE_LOCAL:
        return generate_image_local(prompt, negative_prompt, control_image, num_steps, cfg_scale, seed, auto_canny)
    return generate_image_remote(prompt, negative_prompt, control_image, num_steps, cfg_scale, seed, auto_canny)
