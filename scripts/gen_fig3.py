import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cv2
import os

outdir = '/Users/weidademiaoxiao/Desktop/毕业设计/figures'

# --- Create a base cityscape image ---
def make_city():
    img = Image.new('RGB', (512, 512), '#87CEEB')  # sky blue
    d = ImageDraw.Draw(img)
    # Sky gradient
    for y in range(250):
        r = int(135 + (200-135) * y/250)
        g = int(206 + (220-206) * y/250)
        b = int(235 + (255-235) * y/250)
        d.line([(0, y), (512, y)], fill=(r, g, b))
    # Ground
    d.rectangle([0, 350, 512, 512], fill='#808080')
    # Road
    d.rectangle([0, 380, 512, 512], fill='#555555')
    d.line([256, 380, 256, 512], fill='#FFFFFF', width=3)
    # Buildings
    buildings = [(40, 160, 130, 350, '#8B7355'), (150, 120, 250, 350, '#A0522D'),
                 (270, 180, 370, 350, '#696969'), (390, 140, 480, 350, '#8B8682')]
    for x1, y1, x2, y2, c in buildings:
        d.rectangle([x1, y1, x2, y2], fill=c, outline='#333', width=1)
        # Windows
        for wy in range(y1+15, y2-10, 30):
            for wx in range(x1+12, x2-12, 25):
                d.rectangle([wx, wy, wx+12, wy+18], fill='#FFE4B5', outline='#333')
    # Sidewalk
    d.rectangle([0, 350, 512, 380], fill='#A9A9A9')
    return img

base = make_city()
base_arr = np.array(base)

# --- Canny edge ---
gray = cv2.cvtColor(base_arr, cv2.COLOR_RGB2GRAY)
edges = cv2.Canny(gray, 80, 180)
canny_img = Image.fromarray(cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))

# --- Weather effects using OpenCV/PIL filters ---
def sunny_effect(img_arr):
    result = img_arr.copy().astype(np.float32)
    result[:, :, 0] = np.clip(result[:, :, 0] * 1.1 + 15, 0, 255)  # warm R
    result[:, :, 1] = np.clip(result[:, :, 1] * 1.05 + 10, 0, 255)  # warm G
    result = np.clip(result * 1.15, 0, 255).astype(np.uint8)  # brighter
    # Sun glow
    h, w = result.shape[:2]
    Y, X = np.ogrid[:h, :w]
    cx, cy = int(w*0.75), int(h*0.15)
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    glow = np.clip(1 - dist / 250, 0, 1) * 80
    for c in range(3):
        result[:, :, c] = np.clip(result[:, :, c] + glow, 0, 255).astype(np.uint8)
    return result

def rainy_effect(img_arr):
    result = img_arr.copy().astype(np.float32)
    result = (result * 0.6 + 30).astype(np.uint8)  # darken, blue tint
    result[:, :, 2] = np.clip(result[:, :, 2].astype(np.float32) + 20, 0, 255).astype(np.uint8)
    # Rain streaks
    rain = np.zeros_like(result)
    for _ in range(300):
        x = np.random.randint(0, 512)
        y = np.random.randint(0, 400)
        length = np.random.randint(15, 40)
        cv2.line(rain, (x, y), (x-3, y+length), (200, 200, 220), 1)
    result = np.clip(result.astype(np.float32) + rain * 0.5, 0, 255).astype(np.uint8)
    # Wet ground reflection
    result[370:, :] = np.clip(result[370:, :].astype(np.float32) * 0.7 + 40, 0, 255).astype(np.uint8)
    return result

def snowy_effect(img_arr):
    result = img_arr.copy().astype(np.float32)
    result = (result * 0.8 + 50).astype(np.uint8)  # brighten, whiten
    # Snow on ground
    result[340:, :] = np.clip(result[340:, :].astype(np.float32) * 0.3 + 200, 0, 255).astype(np.uint8)
    # Snow on building tops
    for x1, y1, x2, _ in [(40,160,130,350),(150,120,250,350),(270,180,370,350),(390,140,480,350)]:
        result[y1:y1+8, x1:x2] = [240, 240, 250]
    # Snowflakes
    for _ in range(500):
        x, y = np.random.randint(0, 512), np.random.randint(0, 512)
        s = np.random.randint(2, 5)
        cv2.circle(result, (x, y), s, (240, 240, 255), -1)
    return result

def foggy_effect(img_arr):
    result = img_arr.copy().astype(np.float32)
    fog = np.full_like(result, 220, dtype=np.float32)
    # Depth-based fog (stronger at distance/top)
    h = result.shape[0]
    for y in range(h):
        alpha = 0.3 + 0.45 * (1 - y / h)  # more fog at top
        result[y] = result[y] * (1 - alpha) + fog[y] * alpha
    return np.clip(result, 0, 255).astype(np.uint8)

def thunder_effect(img_arr):
    result = rainy_effect(img_arr)  # start with rain
    result = (result.astype(np.float32) * 0.75).astype(np.uint8)  # darker
    # Lightning bolt
    pts = [(280, 0)]
    x, y = 280, 0
    while y < 350:
        x += np.random.randint(-20, 20)
        y += np.random.randint(15, 35)
        pts.append((x, y))
    for i in range(len(pts)-1):
        cv2.line(result, pts[i], pts[i+1], (255, 255, 200), 3)
        cv2.line(result, pts[i], pts[i+1], (200, 200, 255), 7)
    # Flash glow
    glow_region = result[0:200, 200:360].astype(np.float32)
    result[0:200, 200:360] = np.clip(glow_region + 40, 0, 255).astype(np.uint8)
    return result

effects = [
    ('Original', base_arr),
    ('Canny Edge', np.array(canny_img)),
    ('Sunny', sunny_effect(base_arr)),
    ('Rainy', rainy_effect(base_arr)),
    ('Snowy', snowy_effect(base_arr)),
    ('Foggy', foggy_effect(base_arr)),
    ('Thunderstorm', thunder_effect(base_arr)),
]

# Save individual images
for name, arr in effects:
    Image.fromarray(arr).save(os.path.join(outdir, f'weather_{name.lower().replace(" ", "_")}.png'))

# Create comparison figure
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('Weather Effect Generation Results (Simulated)', fontsize=16, fontweight='bold', y=0.98)

for idx, (name, arr) in enumerate(effects):
    row, col = idx // 4, idx % 4
    axes[row][col].imshow(arr)
    axes[row][col].set_title(name, fontsize=12, fontweight='bold')
    axes[row][col].axis('off')

# Hide last empty subplot
axes[1][3].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(outdir, 'weather_comparison.png'), dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('Done: weather effects')
