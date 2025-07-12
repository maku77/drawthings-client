# drawthings-client

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python client library and command-line tool for interacting with the Draw Things app on macOS.

## Features

- Simple Python API for Draw Things app
- Command-line tool for easy image generation
- Automatic file management for generated images and configurations

## Requirements

- Python 3.12+
- macOS with Draw Things app installed
- Draw Things app running with API server enabled

## Installation

```bash
git clone https://github.com/maku77/drawthings-client.git
cd drawthings-client
pip install -e .
```

## Usage

### Command Line

```bash
# Check configuration
drawthings config

# Generate image from text
drawthings txt2img "a beautiful landscape"
```

Generated images are saved to the `output/` folder with timestamp-based filenames.

### Python API

```python
from drawthings_client import DrawThingsClient, Txt2ImgRequest

# Initialize client
client = DrawThingsClient()

# Generate image
request = Txt2ImgRequest()
request.prompt = "a beautiful sunset over mountains"
request.width = 512
request.height = 512

for image, config in client.txt2img(request):
    image.save("generated_image.png")
```

## API Reference

### DrawThingsClient

Main client class for communicating with Draw Things app.

```python
DrawThingsClient(host="localhost", port=7860)
```

#### Methods

- `get_config()` - Get current configuration from Draw Things app
- `txt2img(request)` - Generate images from text prompt

### Txt2ImgRequest

Request parameters for image generation.

#### Properties

- `prompt` - Text prompt for image generation (required)
- `negative_prompt` - Negative prompt (default: "low quality, blurry, distorted")
- `width`, `height` - Image dimensions in pixels
- `steps` - Number of generation steps
- `guidance_scale` - Guidance scale value
- `seed` - Random seed (-1 for auto-generation)
- `sampler_name` - Sampler name (default: "DPM++ 2M Karras")

## Output Files

Generated images and their configurations are saved to the `output/` folder:

- `YYYYMMDD-HHMMSS.png` - Generated image
- `YYYYMMDD-HHMMSS.json` - Configuration file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**maku77** - [GitHub](https://github.com/maku77)
