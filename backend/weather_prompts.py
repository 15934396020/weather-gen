# Weather effect prompt templates
# Each weather type maps to a set of keywords appended to the user's prompt

WEATHER_PROMPTS = {
    "sunny": {
        "name": "Sunny",
        "positive": "bright sunlight, clear blue sky, warm golden light, sharp shadows, vivid colors, sun rays",
        "negative": "rain, snow, fog, dark, overcast, clouds",
    },
    "rainy": {
        "name": "Rainy",
        "positive": "heavy rain, wet surfaces, water reflections, puddles, overcast sky, rain streaks, gloomy atmosphere, dark clouds",
        "negative": "sunny, clear sky, snow, dry",
    },
    "snowy": {
        "name": "Snowy",
        "positive": "snow covered, white snow on ground, frost, cold winter atmosphere, snowfall, icy surfaces, cold blue lighting, bare trees",
        "negative": "sunny, green leaves, rain, warm",
    },
    "foggy": {
        "name": "Foggy",
        "positive": "dense fog, misty atmosphere, low visibility, soft diffused light, hazy, mysterious mood, fog rolling in",
        "negative": "clear sky, sunny, sharp details, vivid colors",
    },
    "thunderstorm": {
        "name": "Thunderstorm",
        "positive": "thunderstorm, lightning bolts, dark dramatic sky, heavy rain, strong wind, ominous clouds, dramatic lighting, stormy weather",
        "negative": "sunny, calm, clear sky, peaceful",
    },
}

QUALITY_POSITIVE = "high quality, detailed, 8k, photorealistic, masterpiece"
QUALITY_NEGATIVE = "low quality, blurry, distorted, deformed, ugly, watermark, text"


def build_prompt(user_prompt: str, weather_type: str) -> tuple[str, str]:
    """Build full positive and negative prompts by combining user input with weather template."""
    weather = WEATHER_PROMPTS.get(weather_type, WEATHER_PROMPTS["sunny"])
    positive = f"{user_prompt}, {weather['positive']}, {QUALITY_POSITIVE}"
    negative = f"{weather['negative']}, {QUALITY_NEGATIVE}"
    return positive, negative


def get_weather_types() -> list[dict]:
    """Return list of supported weather types."""
    return [
        {"id": k, "name": v["name"]} for k, v in WEATHER_PROMPTS.items()
    ]
