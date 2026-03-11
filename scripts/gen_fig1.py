import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

def box(ax, x, y, w, h, text, color, fontsize=10, textcolor='white'):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=textcolor)

def arrow(ax, x1, y1, x2, y2, text='', color='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))
    if text:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, text, fontsize=8, color='#666', style='italic')

# Title
ax.text(7, 8.5, 'System Architecture', ha='center', fontsize=16, fontweight='bold', color='#333')

# === Layer 1: Frontend ===
ax.add_patch(FancyBboxPatch((0.5, 6.2), 13, 1.8, boxstyle="round,pad=0.2", facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2, linestyle='--'))
ax.text(1.2, 7.7, 'Frontend (Browser)', fontsize=11, fontweight='bold', color='#1565C0')

box(ax, 1, 6.5, 2.2, 0.9, 'Text Input\n(Scene Prompt)', '#42A5F5', 9)
box(ax, 3.5, 6.5, 2.2, 0.9, 'Image Upload\n(Control Map)', '#42A5F5', 9)
box(ax, 6, 6.5, 2.2, 0.9, 'Weather\nSelector', '#42A5F5', 9)
box(ax, 8.5, 6.5, 2.2, 0.9, 'Parameter\nSliders', '#42A5F5', 9)
box(ax, 11, 6.5, 2.2, 0.9, 'Result\nDisplay', '#42A5F5', 9)

# === Layer 2: Backend ===
ax.add_patch(FancyBboxPatch((0.5, 3.2), 13, 2.5, boxstyle="round,pad=0.2", facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2, linestyle='--'))
ax.text(1.2, 5.4, 'Backend (FastAPI Server)', fontsize=11, fontweight='bold', color='#2E7D32')

box(ax, 1, 4.0, 2.5, 0.9, 'API Endpoints\n/api/generate', '#66BB6A', 9)
box(ax, 4, 4.0, 2.5, 0.9, 'Image\nPreprocessing\n(Canny Edge)', '#66BB6A', 8)
box(ax, 7, 4.0, 2.5, 0.9, 'Weather Prompt\nLibrary\n(5 types)', '#66BB6A', 8)
box(ax, 10, 4.0, 2.5, 0.9, 'Prompt\nBuilder', '#66BB6A', 9)

# === Layer 3: Model ===
ax.add_patch(FancyBboxPatch((0.5, 0.3), 13, 2.4, boxstyle="round,pad=0.2", facecolor='#FFF3E0', edgecolor='#E65100', linewidth=2, linestyle='--'))
ax.text(1.2, 2.4, 'AI Model Inference Engine', fontsize=11, fontweight='bold', color='#E65100')

box(ax, 1, 0.7, 2.5, 1.2, 'CLIP\nText Encoder', '#FF9800', 9)
box(ax, 4, 0.7, 2.5, 1.2, 'ControlNet\n(Canny)', '#FF9800', 9)
box(ax, 7, 0.7, 2.5, 1.2, 'U-Net\nDenoiser', '#FF9800', 9)
box(ax, 10, 0.7, 2.5, 1.2, 'VAE\nDecoder', '#FF9800', 9)

# Arrows between layers
arrow(ax, 7, 6.5, 7, 5.8, '')
ax.text(7.2, 6.1, 'HTTP Request\n(JSON + Image)', fontsize=8, color='#666', style='italic')

arrow(ax, 7, 3.2, 7, 2.8, '')
ax.text(7.2, 2.9, 'Model Invocation', fontsize=8, color='#666', style='italic')

# Arrows within backend
arrow(ax, 3.5, 4.45, 4, 4.45)
arrow(ax, 6.5, 4.45, 7, 4.45)
arrow(ax, 9.5, 4.45, 10, 4.45)

# Arrows within model
arrow(ax, 3.5, 1.3, 4, 1.3)
arrow(ax, 6.5, 1.3, 7, 1.3)
arrow(ax, 9.5, 1.3, 10, 1.3)

plt.tight_layout()
plt.savefig('/Users/weidademiaoxiao/Desktop/毕业设计/figures/system_architecture.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('Done: system_architecture.png')
