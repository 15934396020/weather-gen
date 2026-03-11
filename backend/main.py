import io
import base64
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from weather_prompts import build_prompt, get_weather_types
from inference import generate_image
from config import HOST, PORT, DEFAULT_STEPS, DEFAULT_CFG_SCALE

app = FastAPI(title="Weather Scene Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/weather-types")
def weather_types():
    return get_weather_types()


@app.post("/api/generate")
async def generate(
    prompt: str = Form(...),
    weather: str = Form("sunny"),
    steps: int = Form(DEFAULT_STEPS),
    cfg_scale: float = Form(DEFAULT_CFG_SCALE),
    seed: int = Form(-1),
    auto_canny: bool = Form(True),
    control_image: UploadFile = File(...),
):
    # Read uploaded image
    img_bytes = await control_image.read()
    pil_image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    # Build prompts
    positive, negative = build_prompt(prompt, weather)

    # Generate
    result = generate_image(
        prompt=positive,
        negative_prompt=negative,
        control_image=pil_image,
        num_steps=steps,
        cfg_scale=cfg_scale,
        seed=seed,
        auto_canny=auto_canny,
    )

    # Return as PNG
    buf = io.BytesIO()
    result.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


# Serve frontend static files
import os
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
