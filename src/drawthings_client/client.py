"""
Draw Things client for macOS
"""

import logging
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)


class DrawThingsError(Exception):
    """Draw Things API related errors"""

    pass


class ConnectionError(DrawThingsError):
    """Connection related errors"""

    pass


class ValidationError(DrawThingsError):
    """Parameter validation errors"""

    pass


class DrawThingsClient:
    """Draw Things app client"""

    def __init__(self, host: str = "localhost", port: int = 7860) -> None:
        """Initialize Draw Things client

        Args:
            host: Draw Things app host (default: localhost)
            port: Draw Things app port (default: 7860)

        Raises:
            ConnectionError: If cannot connect to Draw Things app
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        logger.info(f"DrawThings client initialized: {self.base_url}")

        # 接続確認
        if not self._check_connection():
            raise ConnectionError(
                f"Draw Thingsサーバーに接続できません: {self.base_url}"
            )

    def _check_connection(self):
        """
        サーバー接続確認（内部メソッド）
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
            ConnectionError: If cannot connect to Draw Things app
        """
        logger.info("Getting configuration from Draw Things app")

        try:
            url = f"{self.base_url}/sdapi/v1/options"
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DrawThingsError(f"設定取得エラー: {e}")

    def generate_image(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        guidance_scale: float = 7.5,
        seed: int | None = None,
        negative_prompt: Optional[str] = None,
    ) -> dict[str, Any]:
        """Generate image from text prompt

        Args:
            prompt: Text prompt for image generation
            width: Image width (default: 512)
            height: Image height (default: 512)
            steps: Number of inference steps (default: 20)
            guidance_scale: Guidance scale (default: 7.5)
            seed: Random seed for reproducible results
            negative_prompt: Negative prompt to avoid certain content

        Returns:
            Generation result with image data and metadata

        Raises:
            ConnectionError: If cannot connect to Draw Things app
            ValidationError: If parameters are invalid
        """
        # パラメータ検証
        if not prompt.strip():
            raise ValidationError("Prompt cannot be empty")

        if width <= 0 or height <= 0:
            raise ValidationError("Width and height must be positive integers")

        if steps <= 0:
            raise ValidationError("Steps must be positive integer")

        if guidance_scale < 0:
            raise ValidationError("Guidance scale must be non-negative")

        logger.info(f"Generating image: {prompt[:50]}...")
        logger.debug(
            f"Parameters: {width}x{height}, steps={steps}, guidance={guidance_scale}"
        )

        if seed is not None:
            logger.debug(f"Seed: {seed}")
        if negative_prompt:
            logger.debug(f"Negative prompt: {negative_prompt}")

        # TODO: 実際のDraw Things APIとの通信を実装
        result = {
            "success": False,
            "message": "Draw Things API integration not yet implemented",
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "negative_prompt": negative_prompt,
        }

        logger.warning("API integration not implemented - returning mock result")
        return result

    def __repr__(self) -> str:
        """String representation of the client"""
        return f"DrawThingsClient(host='{self.host}', port={self.port})"
