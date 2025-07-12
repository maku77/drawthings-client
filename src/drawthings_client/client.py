"""
Draw Things client for macOS
"""

import base64
import logging
import random
from io import BytesIO
from typing import Any

import requests
from PIL import Image

logger = logging.getLogger(__name__)

# TODO: パラメーターとして何も指定していないことを示す値を定義する
# 例: NO_VALUE = object()


class Txt2ImgRequest:
    """
    txt2img API リクエスト用のデータクラス
    """

    prompt: str
    negative_prompt: str = "low quality, blurry, distorted"
    width: int | None = None
    height: int | None = None
    steps: int | None = None
    guidance_scale: float | None = None
    seed: int | None = None
    sampler_name: str = "DPM++ 2M Karras"
    batch_size: int | None = None
    n_iter: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary format (excluding None values)
        """
        # If seed is -1, generate a random int32 seed
        if self.seed == -1:
            self.seed = random.randint(0, 2**31 - 1)

        # Get all dataclass fields and include only non-None values in dictionary
        return {key: value for key, value in self.__dict__.items() if value is not None}


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

    def txt2img(self, request: Txt2ImgRequest):
        """
        Generate images from text using Draw Things txt2img API

        Args:
            request: Txt2ImgRequest object with parameters

        Yields:
            Tuple of (PIL.Image, dict) with generated image and configuration
        """
        url = f"{self.base_url}/sdapi/v1/txt2img"
        payload = request.to_dict()

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
                raise DrawThingsError(f"No image data returned. Response: {result}")

        except requests.exceptions.RequestException as e:
            raise DrawThingsError(f"API call error: {e}")
        except Exception as e:
            raise DrawThingsError(f"Image processing error: {e}")

    def __repr__(self) -> str:
        """String representation of the client"""
        return f"DrawThingsClient(host='{self.host}', port={self.port})"
