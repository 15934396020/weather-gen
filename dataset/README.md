# Dataset

Test images for the weather scene generation system.

## Structure

```
dataset/
├── synthetic/          # Programmatically generated scene images (PIL + OpenCV)
│   └── cityscape_01.png
├── real/               # Real-world photographs
│   ├── urban/          # City streets, buildings, vehicles
│   ├── landscape/      # Parks, lakes, mountains
│   └── architecture/   # Individual buildings, campus structures
└── README.md
```

## Synthetic Images
- Generated using Python PIL library
- 512x512 pixels, clean geometric structures
- Used for controlled comparison experiments

## Real-world Images
- Sources: Unsplash, Pexels (open-license), author's own photography
- Preprocessed: resized to 512x512, Canny edge extraction (low=100, high=200)
- Used for robustness testing with complex inputs

## Usage
Place your test images in the corresponding category folder, then use them as control images in the system.
