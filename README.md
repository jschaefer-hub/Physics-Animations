# ManimGL Animations

This repository contains the code for my manimgl animations, specifically developed for physics visualizations.

## Setup

To run these animations, you need to have **ManimGL** installed. This is the OpenGL version of Manim developed by 3Blue1Brown.

1.  **Install System Dependencies**:
    Ensure you have `ffmpeg` and local LaTeX installation (if you plan to use text/equations).

2.  **Install ManimGL**:
    You can install it via pip:
    ```bash
    pip install manimgl
    ```
    
    For identifying the correct version and troubleshooting, refer to the [official ManimGL repository](https://github.com/3b1b/manim).

## Usage

To run an animation, use the `manimgl` command followed by the file path and the scene name.

### Examples: Cherenkov Polarisation

To run the different scenarios from the `Cherenkov_polarisation.py` file:

1.  **Sublight Speed** (Particle slower than light in medium):
    ```bash
    manimgl Air_showers/Cherenkov_polarisation.py sublight
    ```

2.  **Lightspeed** (Particle at speed of light):
    ```bash
    manimgl Air_showers/Cherenkov_polarisation.py lightspeed
    ```

3.  **Superluminal Speed** (Particle faster than light - Cherenkov radiation):
    ```bash
    manimgl Air_showers/Cherenkov_polarisation.py superluminal
    ```

**Common flags:**
- `-o`: Write the interaction to a file.
- `-w`: Write the file to a video.
- `-ow`: Writes to a file and opens it automatically.
