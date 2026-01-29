# ManimGL Animations

This repository contains the code for my manimgl animations, specifically developed for physics visualizations.

## Setup

To run these animations, you need to have **ManimGL** installed. This is the OpenGL version of Manim developed by 3Blue1Brown.

1.  **Install System Dependencies**:
    Ensure you have `ffmpeg` and local LaTeX installation (if you plan to use text/equations).


2.  **Install ManimGL**:

    If you are on Linux, first install the dependencies:
    ```bash
    mamba create -n manimgl python=3.12
    ```
    Then you clone the [original repository](https://github.com/3b1b/manim) and install with 

    ```bash
    pip install -e .
    ```

## Fixing Linux 
Especially on Linux, it can be that the package `dvisvgm` (commonly delivered with `texlive-dvisvgm`) is too old (current version is 3.6). This is happening specifically on Fedora installations with very old default latex packages.

If you have an older version installed, it is very likely that you will notice errors when using TeX inside of ManimGL.

to fix this please replace your version with the newest one 

```shell
# Add the repository with the newest version 
sudo dnf copr enable mgieseki/dvisvgm
sudo dnf install dvisvgm
```
This will replace the old install.

If you setup a custom cache in `/manimlib/default_config.yml` (specified in the `cache` variable), make sure to delete the old cache file in there after updating dvisvgm.


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
