# Manim Video Scenes

This directory contains manim scenes for time series visualizations.

## Available Scenes

### 1. angular_frequency.py

**AngularFrequencyDemo**: Shows the relationship between angular frequency, circular motion, and sine waves.
- Displays unit circle and sine wave side-by-side
- Animates through ω = 1, 2, 3, 4
- Shows 2 complete rotations for each frequency

**AngularFrequencyCompare**: Shows all four frequencies simultaneously for comparison.

### 2. sine_wave_decomp.py

**SineWaveDecomp**: Demonstrates a sine wave with 2 periods.

## Rendering Videos

### High Quality (1080p60)
```bash
# Main angular frequency demo
uv run manim -pqh angular_frequency.py AngularFrequencyDemo

# Comparison version
uv run manim -pqh angular_frequency.py AngularFrequencyCompare

# Sine wave decomposition
uv run manim -pqh sine_wave_decomp.py SineWaveDecomp
```

### Preview Quality (faster)
```bash
uv run manim -pql angular_frequency.py AngularFrequencyDemo
```

### Options:
- `-p`: Preview (open video after rendering)
- `-q`: Quality level
  - `-ql`: Low (480p15)
  - `-qm`: Medium (720p30)
  - `-qh`: High (1080p60)
  - `-qk`: 4K (2160p60)

## Output Location

Videos are saved to:
- `media/videos/[script_name]/[quality]/[scene_name].mp4`

