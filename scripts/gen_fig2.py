import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(16, 7))
ax.set_xlim(0, 16)
ax.set_ylim(0, 7)
ax.axis('off')
fig.patch.set_facecolor('white')

def box(ax, x, y, w, h, text, color, fontsize=9, textcolor='white'):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=textcolor, linespacing=1.4)

def arrow(ax, x1, y1, x2, y2, color='#555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5))

ax.text(8, 6.5, 'ControlNet Inference Pipeline', ha='center', fontsize=15, fontweight='bold', color='#333')

# Step 1: Inputs (top row)
box(ax, 0.2, 4.5, 2.2, 1.3, 'User Text\nPrompt', '#5C6BC0', 10)
box(ax, 0.2, 2.5, 2.2, 1.3, 'Control\nImage', '#5C6BC0', 10)
box(ax, 0.2, 0.5, 2.2, 1.3, 'Weather\nType', '#5C6BC0', 10)

# Step 2: Preprocessing
arrow(ax, 2.4, 3.15, 3.2, 3.15)
box(ax, 3.2, 2.5, 2, 1.3, 'Canny Edge\nExtraction\n(OpenCV)', '#26A69A', 9)

arrow(ax, 2.4, 1.15, 3.7, 2.5)  # weather -> prompt builder
arrow(ax, 2.4, 5.15, 3.7, 4.8)  # text -> prompt builder

box(ax, 3.2, 4.2, 2, 1.3, 'Prompt\nBuilder\n(merge text +\nweather keywords)', '#26A69A', 8)

# Step 3: Encoders
arrow(ax, 5.2, 4.85, 5.8, 4.85)
box(ax, 5.8, 4.2, 2, 1.3, 'CLIP\nText\nEncoder', '#FF7043', 10)

arrow(ax, 5.2, 3.15, 5.8, 3.15)
box(ax, 5.8, 2.5, 2, 1.3, 'ControlNet\nEncoder\n(Zero Conv)', '#FF7043', 9)

# Step 4: Noise + U-Net
box(ax, 5.8, 0.5, 2, 1.3, 'Random\nGaussian\nNoise z_T', '#78909C', 9)

arrow(ax, 7.8, 4.85, 8.5, 3.8)  # CLIP -> U-Net
arrow(ax, 7.8, 3.15, 8.5, 3.15)  # ControlNet -> U-Net
arrow(ax, 7.8, 1.15, 8.5, 2.5)  # Noise -> U-Net

box(ax, 8.5, 2.0, 2.5, 2.2, 'U-Net\nIterative\nDenoising\n(T steps)', '#EF5350', 10)

# Step 5: VAE Decoder
arrow(ax, 11, 3.1, 11.8, 3.1)
box(ax, 11.8, 2.3, 2, 1.6, 'VAE\nDecoder\nz → image', '#AB47BC', 10)

# Step 6: Output
arrow(ax, 13.8, 3.1, 14.3, 3.1)
box(ax, 14.3, 2.5, 1.5, 1.2, 'Output\nImage', '#2E7D32', 10)

# Labels
ax.text(1.3, 6.0, 'User Inputs', fontsize=10, fontweight='bold', color='#5C6BC0', ha='center')
ax.text(4.2, 5.8, 'Preprocessing', fontsize=10, fontweight='bold', color='#26A69A', ha='center')
ax.text(6.8, 5.8, 'Encoding', fontsize=10, fontweight='bold', color='#FF7043', ha='center')
ax.text(9.75, 5.8, 'Denoising', fontsize=10, fontweight='bold', color='#EF5350', ha='center')
ax.text(12.8, 5.8, 'Decoding', fontsize=10, fontweight='bold', color='#AB47BC', ha='center')

plt.tight_layout()
plt.savefig('/Users/weidademiaoxiao/Desktop/毕业设计/figures/model_pipeline.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('Done: model_pipeline.png')
