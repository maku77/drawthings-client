"""
Tests for Txt2ImgParams class

This module contains tests for the UNSET value handling and to_dict() method.
"""

import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from drawthings_client.client import Txt2ImgParams, INHERIT


class TestTxt2ImgParams(unittest.TestCase):
    """Test cases for Txt2ImgParams class"""

    def test_inherit_values_excluded_from_dict(self):
        """Test that INHERIT values are excluded from to_dict() output"""
        # Prompt, negative_prompt, and seed (which now have default values) should be in the result
        # Note: seed=-1 will be converted to a random value in to_dict()
        request = Txt2ImgParams(prompt="test prompt")
        
        # Mock the random generation to get predictable results
        with patch('drawthings_client.client.random.randint') as mock_randint:
            mock_randint.return_value = 12345
            result = request.to_dict()
        
        expected = {
            "prompt": "test prompt",
            "negative_prompt": Txt2ImgParams.DEFAULT_NEGATIVE_PROMPT,
            "seed": 12345
        }
        self.assertEqual(result, expected)
        
    def test_explicitly_set_values_included_in_dict(self):
        """Test that explicitly set values are included in to_dict() output"""
        request = Txt2ImgParams(
            prompt="test prompt",
            width=512,
            height=512,
            steps=20
        )
        
        # Mock the random generation for seed=-1
        with patch('drawthings_client.client.random.randint') as mock_randint:
            mock_randint.return_value = 54321
            result = request.to_dict()
        
        expected = {
            "prompt": "test prompt",
            "negative_prompt": Txt2ImgParams.DEFAULT_NEGATIVE_PROMPT,
            "seed": 54321,
            "width": 512,
            "height": 512,
            "steps": 20
        }
        self.assertEqual(result, expected)
        
    def test_string_and_numeric_values_included_in_dict(self):
        """Test that explicitly set string and numeric values are included in to_dict() output"""
        request = Txt2ImgParams(
            prompt="test prompt",
            negative_prompt="bad quality",
            width=512,
            height=768
        )
        
        # Mock random for seed=-1 default
        with patch('drawthings_client.client.random.randint') as mock_randint:
            mock_randint.return_value = 77777
            result = request.to_dict()
        
        expected = {
            "prompt": "test prompt",
            "negative_prompt": "bad quality",
            "seed": 77777,
            "width": 512,
            "height": 768
        }
        self.assertEqual(result, expected)
        
    def test_string_values_handled_correctly(self):
        """Test that string values are handled correctly"""
        request = Txt2ImgParams(
            prompt="test prompt",
            negative_prompt="bad quality",
            sampler="DDIM"
        )
        
        # Mock random for seed=-1 default
        with patch('drawthings_client.client.random.randint') as mock_randint:
            mock_randint.return_value = 88888
            result = request.to_dict()
        
        expected = {
            "prompt": "test prompt",
            "negative_prompt": "bad quality",
            "seed": 88888,
            "sampler": "DDIM"
        }
        self.assertEqual(result, expected)
        
    def test_inherit_vs_explicit_values(self):
        """Test that INHERIT and explicit values are handled differently"""
        # Test with defaults (negative_prompt and seed have default values)
        request1 = Txt2ImgParams(prompt="test")
        
        # Test with explicit string value
        request2 = Txt2ImgParams(prompt="test", negative_prompt="explicit value")
        
        # Mock random for both tests
        with patch('drawthings_client.client.random.randint') as mock_randint:
            mock_randint.return_value = 99999
            result1 = request1.to_dict()
            result2 = request2.to_dict()
        
        # Default values should be included, explicit values should override
        expected1 = {
            "prompt": "test",
            "negative_prompt": Txt2ImgParams.DEFAULT_NEGATIVE_PROMPT,
            "seed": 99999
        }
        expected2 = {
            "prompt": "test", 
            "negative_prompt": "explicit value",
            "seed": 99999
        }
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)
        
    @patch('drawthings_client.client.random.randint')
    def test_seed_random_generation(self, mock_randint):
        """Test that seed=-1 generates random seed"""
        mock_randint.return_value = 12345
        
        request = Txt2ImgParams(prompt="test", seed=-1)
        result = request.to_dict()
        
        # Seed should be replaced with random value
        self.assertEqual(result["seed"], 12345)
        mock_randint.assert_called_once_with(0, 2**31 - 1)
        
    def test_seed_specific_value_preserved(self):
        """Test that specific seed values are preserved"""
        request = Txt2ImgParams(prompt="test", seed=42)
        result = request.to_dict()
        
        # Specific seed should be preserved
        self.assertEqual(result["seed"], 42)
        
    def test_all_parameters_set(self):
        """Test with all parameters explicitly set"""
        request = Txt2ImgParams(
            prompt="beautiful landscape",
            negative_prompt="ugly, blurry",
            width=1024,
            height=768,
            steps=30,
            guidance_scale=7.5,
            seed=12345,
            sampler="Euler a",
            batch_size=2,
            batch_count=3
        )
        result = request.to_dict()
        
        expected = {
            "prompt": "beautiful landscape",
            "negative_prompt": "ugly, blurry",
            "width": 1024,
            "height": 768,
            "steps": 30,
            "guidance_scale": 7.5,
            "seed": 12345,
            "sampler": "Euler a",
            "batch_size": 2,
            "batch_count": 3
        }
        self.assertEqual(result, expected)
        
    def test_inherit_object_identity(self):
        """Test that INHERIT values maintain object identity"""
        request = Txt2ImgParams(prompt="test")
        
        # Check that inherit values are the same INHERIT object
        # Note: negative_prompt now has a string default, not INHERIT
        self.assertIs(request.width, INHERIT)
        self.assertIs(request.height, INHERIT)
        self.assertIs(request.sampler, INHERIT)


if __name__ == "__main__":
    unittest.main()