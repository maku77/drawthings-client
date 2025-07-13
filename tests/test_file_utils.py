"""
Tests for file_utils.py module

This module contains comprehensive tests for the FilePathGenerator class,
including home directory expansion functionality.
"""

import os
import sys
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from drawthings_client.lib.file_utils import FilePathGenerator


class TestFilePathGenerator(unittest.TestCase):
    """Test cases for FilePathGenerator class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_timestamp = "20240101-120000"

    def tearDown(self):
        """Clean up after each test method."""
        # Clean up any created directories
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_empty_directory_initialization(self):
        """Test FilePathGenerator initialization with empty directory"""
        generator = FilePathGenerator("")

        # Should create basepath with timestamp only
        self.assertRegex(generator.basepath, r"\d{8}-\d{6}")

    def test_specific_directory_initialization(self):
        """Test FilePathGenerator initialization with specific directory"""
        test_dir = os.path.join(self.temp_dir, "test_output")
        generator = FilePathGenerator(test_dir)

        # Should create directory and include it in basepath
        self.assertTrue(os.path.exists(test_dir))
        self.assertTrue(generator.basepath.startswith(test_dir))
        self.assertRegex(generator.basepath, r"test_output[\\/]\d{8}-\d{6}")

    def test_home_directory_expansion(self):
        """Test home directory shortcut expansion"""
        # Test with ~ shortcut
        with (
            patch("os.path.expanduser") as mock_expand,
            patch("os.path.exists") as mock_exists,
            patch("os.makedirs") as mock_makedirs,
        ):
            # Setup mocks
            expanded_path = os.path.join(self.temp_dir, "expanded_path")
            mock_expand.return_value = expanded_path
            mock_exists.return_value = False

            generator = FilePathGenerator("~/test_output")

            # Verify expanduser was called
            mock_expand.assert_called_once_with("~/test_output")

            # Verify makedirs was called with expanded path
            mock_makedirs.assert_called_once_with(expanded_path)

            # Verify the expanded path is used
            self.assertTrue(generator.basepath.startswith(expanded_path))

    def test_home_directory_no_expansion_needed(self):
        """Test that non-home paths work correctly with expanduser"""
        test_dir = os.path.join(self.temp_dir, "regular_path")

        # expanduser should return the path unchanged for non-home paths
        with patch("os.path.expanduser") as mock_expand:
            mock_expand.return_value = test_dir
            generator = FilePathGenerator(test_dir)

            # expanduser should be called but return the same path
            mock_expand.assert_called_once_with(test_dir)

            # Path should be used as-is
            self.assertTrue(generator.basepath.startswith(test_dir))

    @patch("drawthings_client.lib.file_utils.datetime")
    def test_create_image_path_single(self, mock_datetime):
        """Test creating single image path"""
        mock_datetime.now.return_value.strftime.return_value = self.test_timestamp

        generator = FilePathGenerator("")
        image_path = generator.create_image_path(1)

        expected_path = f"{self.test_timestamp}.png"
        self.assertEqual(image_path, expected_path)

    @patch("drawthings_client.lib.file_utils.datetime")
    def test_create_image_path_multiple(self, mock_datetime):
        """Test creating multiple image paths with count"""
        mock_datetime.now.return_value.strftime.return_value = self.test_timestamp

        generator = FilePathGenerator("")

        # Test different counts
        for count in [2, 3, 10]:
            with self.subTest(count=count):
                image_path = generator.create_image_path(count)
                expected_path = f"{self.test_timestamp}_{count}.png"
                self.assertEqual(image_path, expected_path)

    @patch("drawthings_client.lib.file_utils.datetime")
    def test_create_config_path_single(self, mock_datetime):
        """Test creating single config path"""
        mock_datetime.now.return_value.strftime.return_value = self.test_timestamp

        generator = FilePathGenerator("")
        config_path = generator.create_config_path(1)

        expected_path = f"{self.test_timestamp}.json"
        self.assertEqual(config_path, expected_path)

    @patch("drawthings_client.lib.file_utils.datetime")
    def test_create_config_path_multiple(self, mock_datetime):
        """Test creating multiple config paths with count"""
        mock_datetime.now.return_value.strftime.return_value = self.test_timestamp

        generator = FilePathGenerator("")

        # Test different counts
        for count in [2, 3, 10]:
            with self.subTest(count=count):
                config_path = generator.create_config_path(count)
                expected_path = f"{self.test_timestamp}_{count}.json"
                self.assertEqual(config_path, expected_path)

    @patch("drawthings_client.lib.file_utils.datetime")
    def test_create_paths_with_directory(self, mock_datetime):
        """Test creating paths with specified directory"""
        mock_datetime.now.return_value.strftime.return_value = self.test_timestamp

        test_dir = os.path.join(self.temp_dir, "output_dir")
        generator = FilePathGenerator(test_dir)

        image_path = generator.create_image_path(1)
        config_path = generator.create_config_path(1)

        expected_base = os.path.join(test_dir, self.test_timestamp)
        expected_image = f"{expected_base}.png"
        expected_config = f"{expected_base}.json"

        self.assertEqual(image_path, expected_image)
        self.assertEqual(config_path, expected_config)

    def test_real_home_directory_expansion(self):
        """Integration test with real home directory expansion"""
        # This test uses actual os.path.expanduser to verify real behavior
        generator = FilePathGenerator("~/test_integration")

        # Get expected expanded path
        expected_base = os.path.expanduser("~/test_integration")

        # Verify the basepath starts with the expanded home directory
        self.assertTrue(generator.basepath.startswith(expected_base))

        # Verify timestamp format in path
        timestamp_part = generator.basepath.replace(expected_base + os.sep, "")
        self.assertRegex(timestamp_part, r"\d{8}-\d{6}")

    def test_directory_creation(self):
        """Test that directories are created when they don't exist"""
        non_existent_dir = os.path.join(self.temp_dir, "new_directory", "nested")

        # Ensure directory doesn't exist initially
        self.assertFalse(os.path.exists(non_existent_dir))

        # Create generator - should create the directory
        generator = FilePathGenerator(non_existent_dir)

        # Verify directory was created
        self.assertTrue(os.path.exists(non_existent_dir))
        self.assertTrue(generator.basepath.startswith(non_existent_dir))

    def test_timestamp_format(self):
        """Test that generated timestamps follow the expected format"""
        generator = FilePathGenerator("")

        # Extract timestamp from basepath
        timestamp = generator.basepath

        # Verify format: YYYYMMDD-HHMMSS
        self.assertRegex(timestamp, r"^\d{8}-\d{6}$")

        # Verify it's a valid datetime
        datetime.strptime(timestamp, "%Y%m%d-%H%M%S")


if __name__ == "__main__":
    unittest.main()
