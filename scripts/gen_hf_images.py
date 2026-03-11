"""Generate weather scene images using HF Inference API with FLUX.1-schnell"""
from huggingface_hub import InferenceClient
import os

client = InferenceClient(token=os.getenv("HF_TOKEN"))
outdir = "/Users/weidademiaoxiao/Desktop/毕业设计/figures/generated"
os.makedirs(outdir, exist_ok=True)

base = "a city street with tall buildings, cars and pedestrians"
quality = "photorealistic, highly detailed, 8k resolution, masterpiece"

weather_prompts = {
    "sunny": f"{base}, bright sunlight, clear blue sky, warm golden light, sharp shadows, vivid colors, sun rays, {quality}",
    "rainy": f"{base}, heavy rain, wet surfaces, water reflections, puddles, overcast sky, rain streaks, gloomy atmosphere, {quality}",
    "snowy": f"{base}, snow covered ground, snowfall, frost, cold winter atmosphere, icy surfaces, cold blue lighting, {quality}",
    "foggy": f"{base}, dense fog, misty atmosphere, low visibility, soft diffused light, hazy, mysterious mood, {quality}",
    "thunderstorm": f"{base}, thunderstorm, lightning bolts, dark dramatic sky, heavy rain, ominous clouds, dramatic lighting, {quality}",
}

model = "black-forest-labs/FLUX.1-schnell"

for name, prompt in weather_prompts.items():
    print(f"Generating {name}...")
    try:
        image = client.text_to_image(prompt, model=model)
        path = os.path.join(outdir, f"hf_{name}.png")
        image.save(path)
        print(f"  Saved: {path} ({image.size})")
    except Exception as e:
        print(f"  Failed: {e}")

print("Done!")
