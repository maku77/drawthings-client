"""
Draw Things client for macOS
"""

import base64
import json
import logging
import random
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Iterator

import requests  # type: ignore
from PIL import Image

logger = logging.getLogger(__name__)


# Sentinel value to inherit server's current configuration (different from None)
class _InheritType:
    """Sentinel type for parameters that should inherit server's current settings"""

    def __repr__(self) -> str:
        return "INHERIT"


"""This is a singleton instance of the inherit type

It is used to distinguish between parameters that are explicitly set to None and those that should inherit the server's current configuration."""
INHERIT = _InheritType()


@dataclass
class Lora:
    """
    Represents a LoRA (Low-Rank Adaptation) configuration for Draw Things app.
    """

    file: str
    weight: float
    enabled: bool

    def __init__(self, file: str, weight: float = 1.0, enabled: bool = True):
        """
        Initialize a Lora instance.

        Args:
            file: Path to the LoRA file.
            weight: Weight of the LoRA (default: 1.0).
            enabled: Whether the LoRA is enabled (default: True).
        """
        self.file = file
        self.weight = weight
        self.enabled = enabled

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary format
        """
        result = {"file": self.file, "weight": self.weight}

        # Only include enabled key when it's False
        if not self.enabled:
            result["enabled"] = False

        return result

    def to_json(self) -> str:
        """
        Convert to JSON string format
        """
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True)


@dataclass
class Txt2ImgParams:
    """
    Represents a request for the txt2img API of Draw Things app.
    """

    # Default values for parameters
    DEFAULT_NEGATIVE_PROMPT = "worst quality, low quality, normal quality, blurry, distorted, bad anatomy, bad hands, error, missing fingers, cropped"
    DEFAULT_SEED = -1  # -1 means generate random seed

    prompt: str
    model: str | _InheritType = INHERIT
    negative_prompt: str | _InheritType = DEFAULT_NEGATIVE_PROMPT
    width: int | _InheritType = INHERIT
    height: int | _InheritType = INHERIT
    steps: int | _InheritType = INHERIT
    guidance_scale: float | _InheritType = INHERIT
    seed: int | _InheritType = DEFAULT_SEED
    sampler: str | _InheritType = INHERIT  # "DPM++ 2M Karras"
    clip_skip: int | _InheritType = INHERIT  # Clip skip value
    shift: float | _InheritType = INHERIT  # Shift value for the sampler
    batch_count: int | _InheritType = INHERIT  # Number of iterations
    batch_size: int | _InheritType = INHERIT  # Number of images generated at once
    loras: list[Lora] | _InheritType = INHERIT

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary format (excluding INHERIT values)
        """
        result = {}

        for key, value in self.__dict__.items():
            # Skip INHERIT values (parameters that should inherit server's current settings)
            if value is INHERIT:
                continue

            # Skip loras field here as it's handled specially below
            if key == "loras":
                if value is INHERIT:
                    continue
                else:
                    value = [lora.to_dict() for lora in value]

            # If seed is -1, generate a random int32 seed
            if key == "seed" and value == Txt2ImgParams.DEFAULT_SEED:
                value = random.randint(0, 2**31 - 1)

            result[key] = value

        return result

    def to_json(self) -> str:
        """
        Convert to JSON string format
        """

        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True)


class DrawThingsError(Exception):
    """Draw Things API related errors"""

    pass


class DrawThingsClient:
    """Draw Things app client"""

    def __init__(self, host: str = "localhost", port: int = 7860) -> None:
        """Initialize Draw Things client

        Args:
            host: Draw Things app host (default: localhost)
            port: Draw Things app port (default: 7860)

        Raises:
            DrawThingsError: If cannot connect to Draw Things app
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        logger.info(f"DrawThings client initialized: {self.base_url}")

        # 接続確認
        if not self._check_connection():
            raise DrawThingsError(
                f"Cannot connect to Draw Things server: {self.base_url}"
            )

    def _check_connection(self):
        """
        Check connection to Draw Things app (internal method)

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            url = f"{self.base_url}/sdapi/v1/options"
            response = requests.get(url, timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_config(self) -> dict[str, Any]:
        """Get configuration from Draw Things app

        Returns:
            Configuration dictionary

        Raises:
            DrawThingsError: If cannot connect to Draw Things app
        """
        logger.info("Getting configuration from Draw Things app")

        try:
            url = f"{self.base_url}/sdapi/v1/options"
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DrawThingsError(f"Configuration retrieval error: {e}")

    def txt2img(
        self, request: Txt2ImgParams
    ) -> Iterator[tuple[Image.Image, dict[str, Any]]]:
        """
        Generate images from text using Draw Things txt2img API

        Args:
            request: Txt2ImgParams object with parameters

        Yields:
            Tuple of (PIL.Image, dict) with generated image and configuration
        """
        url = f"{self.base_url}/sdapi/v1/txt2img"
        payload = request.to_dict()
        # logger.debug(f"txt2img options: {payload}")

        try:
            # This merges the server configuration with the request parameters
            server_config = self.get_config()
            merged_config = {**server_config, **payload}

            # Call the API
            response = requests.post(url, json=payload, timeout=600)
            response.raise_for_status()
            result = response.json()

            if "images" in result and result["images"]:
                # Yield each image in the response
                for image_base64 in result["images"]:
                    image_data = base64.b64decode(image_base64)
                    image = Image.open(BytesIO(image_data))
                    yield image, merged_config
            else:
                raise DrawThingsError(f"No images returned in response: {result}")

        except requests.exceptions.RequestException as e:
            raise DrawThingsError(f"API call error: {e}")
        except Exception as e:
            raise DrawThingsError(f"Image processing error: {e}")

    def __repr__(self) -> str:
        """String representation of the client"""
        return f"DrawThingsClient(host='{self.host}', port={self.port})"


def validate_dict_keys(dict1: dict, dict2: dict) -> None:
    """
    Validate that all keys in dict1 are present in dict2."""
    invalid_keys = [key for key in dict1 if key not in dict2]
    if invalid_keys:
        logger.error(f"Invalid keys found: {invalid_keys}")
        raise DrawThingsError(
            f"Invalid keys in request: {', '.join(invalid_keys)}. "
            "Please check the Draw Things API documentation for valid parameters."
        )
