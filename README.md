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

### For Users

Install the `drawthings` command:

```bash
git clone https://github.com/maku77/drawthings-client.git
cd drawthings-client
uv pip install .  # Install package and dependencies to current environment
```

Or install directly from the repository:

```bash
uv pip install git+https://github.com/maku77/drawthings-client.git  # Install directly from GitHub
```

**After installation, you can:**
- Use the `drawthings` command from anywhere in your terminal
- Generate images using Draw Things app via command line
- Import and use the Python API in your scripts

### For Developers

Clone and set up the development environment:

```bash
git clone https://github.com/maku77/drawthings-client.git
cd drawthings-client
uv sync --group dev --group test  # Install all dependencies including dev and test tools
uv pip install -e .  # Install package in editable mode (changes reflect immediately)
```

**After setup, you can:**
- Use the `drawthings` command with live code changes
- Run tests with `uv run pytest tests/ -v`
- Use type checking and development tools
- Contribute to the project with proper testing environment

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
import os
import uuid
from drawthings_client import DrawThingsClient, Txt2ImgRequest

# Initialize client
client = DrawThingsClient()

# Generate image
request = Txt2ImgRequest(prompt="a beautiful landscape")
for image, config in client.txt2img(request):
    # Save image
    filename = f"image-{uuid.uuid4().hex[:4]}.png"
    image.save(filename)
    print(f"Saved: {filename}")
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

## Development

### Running Tests

Run all tests using uv:

```bash
# Install test dependencies
uv sync --group test

# Run tests with pytest
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=src/drawthings_client --cov-report=html

# Run specific test file
uv run pytest tests/test_file_utils.py -v
```

### Test Coverage

The test suite includes comprehensive tests for:

- FilePathGenerator class functionality
- Home directory path expansion (`~/path` support)
- File path generation for images and configurations
- Directory creation and timestamp formatting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**maku77** - [GitHub](https://github.com/maku77)
