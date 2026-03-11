"""Generate a weather comparison figure for the report"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os

figdir = "/Users/weidademiaoxiao/Desktop/毕业设计/figures"
gendir = os.path.join(figdir, "generated")

weather_types = ["sunny", "rainy", "snowy", "foggy", "thunderstorm"]
labels = ["Sunny", "Rainy", "Snowy", "Foggy", "Thunderstorm"]

fig, axes = plt.subplots(1, 5, figsize=(20, 4.5))
fig.suptitle('Weather Effect Prompt Engineering Validation (Text-to-Image)', fontsize=14, fontweight='bold', y=1.02)

for i, (wt, label) in enumerate(zip(weather_types, labels)):
    img = Image.open(os.path.join(gendir, f"hf_{wt}.png"))
    axes[i].imshow(img)
    axes[i].set_title(label, fontsize=12, fontweight='bold')
    axes[i].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(figdir, "weather_prompt_validation.png"), dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("Done: weather_prompt_validation.png")
